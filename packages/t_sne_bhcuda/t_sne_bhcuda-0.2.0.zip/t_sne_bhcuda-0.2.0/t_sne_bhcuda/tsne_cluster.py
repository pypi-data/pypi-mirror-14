
from bokeh.client import push_session
from bokeh.models import BoxSelectTool, LassoSelectTool, ColumnDataSource, TextInput, Paragraph, VBox, HBox
from bokeh.plotting import curdoc, figure, hplot, vplot
from bokeh.models.widgets import DataTable, TableColumn, Button, Select, Toggle, CheckboxGroup
import numpy as np
import pandas as pd
from t_sne_bhcuda import spike_heatmap

# globals
currently_selected_spike_indices = []
update_spike_corr_heatmap_figs = True
tsne_clusters_scatter_plot = None
checkbox_show_clusters_with_colors = None

def gui_manual_cluster_tsne_spikes(tsne_array_or_filename, spike_times_list_or_filename, raw_extracellular_data,
                                   num_of_points_for_baseline, cut_extracellular_data_or_filename,
                                   shape_of_cut_extracellular_data, cube_type,
                                   sampling_freq, autocor_bin_number,
                                   cluster_info_file, use_existing_cluster=False, time_samples_h5_dir=None,
                                   spike_indices_to_use=None, prb_file=None, k4=False,
                                   verbose=False):
    """
    Creates a GUI that shows the t-sne data and allows selection of them, showing the average spikes forms, the
    autocorrelogram and the heatmap of the selected spikes. It also allows putting the selected spikes in clusters.
    Either the raw extracellular data or the cut extracellular data cube must have the same number of spikes as the
    provided t-sne data set. A sub-selection of spikes to be shown on the t-sne gui can be done by providing the
    spike_indices_to_use array. But the provided data (voltage and t-sne) must have the same number of spikes
    to begin with and their indices must correspond since this is not checked in this method.
    If the number of spikes in the t-sne data and the length of the spike_indices_to_use array do not match then the
    cut extracellular data cube will be recreated even if the cut_extracellular_data_or_filename parameters points to
    an existing file.

    ATTENTION:
    FOR THE GUI TO WORK A BOKEH SERVER MUST BE RUNNING!!

    To start a bokeh server (assuming the bokeh.exe is in your path) do bokeh serve in a command promt (or check the
    bokeh manual).

    Parameters
    ----------
    tsne_array_or_filename: filename of t-sne data or t-sne data array (2 x spike number)
    spike_times_list_or_filename: the .kwik filename where the spike times are saved or an array with the spike times
    raw_extracellular_data: the raw array (electrodes x time points) of the recording
    num_of_points_for_baseline: number of time points to use to baseline the spike traces (no filtering is used so some
    baselining helps).
    cut_extracellular_data_or_filename: instead of the raw_extracellular_data one can pass either the .npy filename
    holding an electrodes x time points x spikes already cut data cube or the data cube itself. The function will use
    (or create) the .npy file to memmap (thus not loading the full cut data on RAM).
    shape_of_cut_extracellular_data: the number of electrodes x number of time points in a spike x number of spikes
    cube_type: the data type of the cut cube data
    sampling_freq: the sampling frequency of the recording
    autocor_bin_number: the amount of bins that the autocorellogram will be split into
    cluster_info_file: the file name to hold the cluster info (a .pkl file since this is a pickle of a pandas dataframe)
    use_existing_cluster: if False then any .pkl file with the same name will be overwritten and there will be no
    cluster info at the beginning of the GUI. If True then the existing .pkl file will be expanded (and its clusters
    will appear at the beginning of the GUI).
    time_samples_h5_dir: the directory structure within the .kwik file where the spike times are saved
    spike_indices_to_use: A sub-sample of the spikes passed by the t-sne data and the raw or cut extracellular data
    prb_file: the probe geometry file defining the probe as used in the phy module
    k4: if True the screen is 4k (defines the size of the gui). Otherwise it is assumed to be HD
    verbose: if True then the GUI will print info on the interpreter

    Returns
    -------

    """

    if type(tsne_array_or_filename) is str:
        tsne_array_or_filename = get_tsne_from_filename(tsne_array_or_filename)

    # Select the tsne samples to use
    num_of_initial_spikes = tsne_array_or_filename.shape[1]
    if spike_indices_to_use is None:
        spike_indices_to_use = np.arange(num_of_initial_spikes)
    tsne_array_or_filename = tsne_array_or_filename[:, spike_indices_to_use]

    if type(spike_times_list_or_filename) is str and time_samples_h5_dir is not None:
        used_extra_spike_times = get_spike_times_from_kwik_file(spike_times_list_or_filename, time_samples_h5_dir,
                                                                verbose=verbose)
    elif type(spike_times_list_or_filename) is str and time_samples_h5_dir is None:
        print('If the .kwik filename is given, the hdf5 file internal directory where the spike times are, ' +
              'must also be given')
        return
    else:
        used_extra_spike_times = spike_times_list_or_filename

    used_extra_spike_times = used_extra_spike_times[spike_indices_to_use]
    num_of_spikes_used = len(used_extra_spike_times)

    if num_of_spikes_used != shape_of_cut_extracellular_data[2]:
        print('The number of chosen spikes in spike_indices_to_use and the number of spikes in ' +
              'shape_of_cut_extracellular_data[2] must be equal')
        return

    num_of_points_in_spike_trig = shape_of_cut_extracellular_data[1]

    # Generate a new data cube file if raw data are provided and the user passes a filename to save the memmap
    # of the cut cube in
    # If a new data cube is not generated then load the existing one (with the given filename). Warn the user that the
    # loaded data cube needs to have a number of spikes equal to the selected ones (if there is subselection of spikes)
    if raw_extracellular_data is not None and type(cut_extracellular_data_or_filename) is str:
        print('Recreating the channels x time x spikes data cube')
        num_ivm_channels = raw_extracellular_data.shape[0]
        if num_ivm_channels != shape_of_cut_extracellular_data[0]:
            print('The number of channels in the raw_extracellular_data and the number of channels in ' +
                  'shape_of_cut_extracellular_data[0] must be equal')
            return
        cut_extracellular_data = create_data_cube_from_raw_extra_data(raw_extracellular_data,
                                                                      cut_extracellular_data_or_filename,
                                                                      num_ivm_channels, num_of_points_in_spike_trig,
                                                                      cube_type, used_extra_spike_times,
                                                                      num_of_points_for_baseline=
                                                                      num_of_points_for_baseline)
    else:
        if num_of_spikes_used != num_of_initial_spikes:
            print('Warning! If the cut_extracellular_data_or_filename does not point to a cut data cube with a number' +
                  'of spikes equal to the selected ones the gui will fail!')
        import os.path as path
        if type(cut_extracellular_data_or_filename) is str and path.isfile(cut_extracellular_data_or_filename):
            print('Loading an existing channels x time x spikes data cube')
            cut_extracellular_data = load_extracellular_data_cube(cut_extracellular_data_or_filename, cube_type,
                                                                  shape_of_cut_extracellular_data)
        else:
            print("If no extracellular raw or cut data are provided then a filename pointing to the " +
                  "cut extra data cube should be given")
            return

    if type(cluster_info_file) is str:
        import os.path as path
        if not path.isfile(cluster_info_file):
            create_new_cluster_info_file(cluster_info_file)

    time_axis = generate_time_axis(num_of_points_in_spike_trig, sampling_freq)

    generate_gui(tsne_array_or_filename, cut_extracellular_data, used_extra_spike_times, time_axis,
                 cluster_info_file, use_existing_cluster, autocor_bin_number, sampling_freq, prb_file, k4, verbose)


# Data generation and manipulation functions
def get_tsne_from_filename(tsne_filename):
    return np.load(tsne_filename)


def get_spike_times_from_kwik_file(kwik_filename, time_samples_h5_dir, verbose=False):
    import h5py as h5
    h5file = h5.File(kwik_filename, mode='r')
    all_extra_spike_times = np.array(list(h5file[time_samples_h5_dir]))
    h5file.close()
    if verbose:
        print('All extra spikes = {}'.format(len(all_extra_spike_times)))
    return all_extra_spike_times


def create_data_cube_from_raw_extra_data(raw_extracellular_data, data_cube_filename, num_ivm_channels,
                                         num_of_points_in_spike_trig, cube_type, extra_spike_times,
                                         num_of_points_for_baseline=None):
    import os.path as path
    if path.isfile(data_cube_filename):
        import os
        os.remove(data_cube_filename)

    num_of_spikes = len(extra_spike_times)
    shape_of_spike_trig_avg = ((num_ivm_channels,
                                num_of_points_in_spike_trig,
                                num_of_spikes))

    data_cube = np.memmap(data_cube_filename,
                          dtype=cube_type,
                          mode='w+',
                          shape=shape_of_spike_trig_avg)
    for spike in np.arange(0, num_of_spikes):
        trigger_point = extra_spike_times[spike]
        start_point = int(trigger_point - num_of_points_in_spike_trig / 2)
        if start_point < 0:
            break
        end_point = int(trigger_point + num_of_points_in_spike_trig / 2)
        if end_point > raw_extracellular_data.shape[1]:
            break
        temp = raw_extracellular_data[:, start_point:end_point]
        if num_of_points_for_baseline is not None:
            baseline = np.mean(temp[:, [0, num_of_points_for_baseline]], 1)
            temp = (temp.T - baseline.T).T
        data_cube[:, :, spike] = temp.astype(cube_type)
    del raw_extracellular_data
    del temp
    del baseline
    del data_cube

    cut_extracellular_data = load_extracellular_data_cube(data_cube_filename, cube_type, shape_of_spike_trig_avg)

    return cut_extracellular_data


def load_extracellular_data_cube(data_cube_filename, cube_type,
                                 shape_of_spike_trig_avg):
    cut_extracellular_data = np.memmap(data_cube_filename,
                                       dtype=cube_type,
                                       mode='r',
                                       shape=shape_of_spike_trig_avg)
    return cut_extracellular_data


def generate_time_axis(num_of_points_in_spike_trig, sampling_freq):
    time_axis = np.arange(-num_of_points_in_spike_trig/(2*sampling_freq),
                          num_of_points_in_spike_trig/(2*sampling_freq),
                          1/sampling_freq)
    return time_axis


# Spike train autocorelogram
def crosscorrelate_spike_trains(spike_times_train_1, spike_times_train_2, lag=None):
    if spike_times_train_1.size < spike_times_train_2.size:
        if lag is None:
            lag = np.ceil(10 * np.mean(np.diff(spike_times_train_1)))
        reverse = False
    else:
        if lag is None:
            lag = np.ceil(20 * np.mean(np.diff(spike_times_train_2)))
        spike_times_train_1, spike_times_train_2 = spike_times_train_2, spike_times_train_1
        reverse = True

    # calculate cross differences in spike times
    differences = np.array([])
    for k in np.arange(0, spike_times_train_1.size):
        differences = np.append(differences, spike_times_train_1[k] - spike_times_train_2[np.nonzero(
            (spike_times_train_2 > spike_times_train_1[k] - lag)
             & (spike_times_train_2 < spike_times_train_1[k] + lag)
             & (spike_times_train_2 != spike_times_train_1[k]))])
    if reverse is True:
        differences = -differences
    norm = np.sqrt(spike_times_train_1.size * spike_times_train_2.size)
    return differences, norm


# Cluster info file and pandas series functions
def create_new_cluster_info_file(filename):
    cluster_info = pd.DataFrame(columns=['Cluster', 'Num_of_Spikes', 'Spike_Indices'])
    cluster_info = cluster_info.set_index('Cluster')
    cluster_info['Spike_Indices'] = cluster_info['Spike_Indices'].astype(list)
    cluster_info.to_pickle(filename)
    return cluster_info


def load_cluster_info(filename):
    cluster_info = pd.read_pickle(filename)
    return cluster_info


def add_cluster_to_cluster_info(filename, cluster_name, spike_indices):
    cluster_info = load_cluster_info(filename)
    cluster_info.set_value(cluster_name, 'Num_of_Spikes', len(spike_indices))
    cluster_info.set_value(cluster_name, 'Spike_Indices', spike_indices)
    cluster_info.to_pickle(filename)
    return cluster_info


def remove_cluster_from_cluster_info(filename, cluster_name):
    cluster_info = load_cluster_info(filename)
    cluster_info = cluster_info.drop([cluster_name])
    cluster_info.to_pickle(filename)
    return cluster_info


def add_spikes_to_cluster(filename, cluster_name, spike_indices):
    cluster_info = load_cluster_info(filename)
    new_indices = np.append(cluster_info['Spike_Indices'][cluster_name], spike_indices)
    cluster_info.set_value(cluster_name, 'Spike_Indices', new_indices)
    cluster_info.set_value(cluster_name, 'Num_of_Spikes', len(new_indices))
    cluster_info.to_pickle(filename)
    return cluster_info


def remove_spikes_from_cluster(filename, cluster_name, spike_indices):
    cluster_info = load_cluster_info(filename)
    mask = np.in1d(cluster_info['Spike_Indices'][cluster_name], spike_indices)
    new_indices = cluster_info['Spike_Indices'][cluster_name][~mask]
    add_cluster_to_cluster_info(filename, cluster_name, new_indices)


# Gui generator
def generate_gui(tsne, cut_extracellular_data, all_extra_spike_times, time_axis, cluster_info_file,
                 use_existing_cluster, autocor_bin_number, sampling_freq, prb_file=None, k4=False, verbose=False):

    if k4:
        tsne_figure_size = [1000, 800]
        tsne_min_border_left = 50
        spike_figure_size = [500, 500]
        hist_figure_size = [500, 500]
        heatmap_plot_size = [200, 800]
        clusters_table_size = [400, 300]
        layout_size = [1500, 1400]
    else:
        tsne_figure_size = [600, 500]
        tsne_min_border_left = 10
        spike_figure_size = [300, 300]
        hist_figure_size = [300, 300]
        heatmap_plot_size = [200, 800]
        clusters_table_size = [300, 400]
        layout_size = [1200, 800]

    # Plots ------------------------------
    # scatter plot
    tsne_fig_tools = "pan,wheel_zoom,box_zoom,box_select,lasso_select,resize,reset,save"
    tsne_figure = figure(tools=tsne_fig_tools, plot_width=tsne_figure_size[0], plot_height=tsne_figure_size[1],
                         title=None, min_border=10, min_border_left=tsne_min_border_left, webgl=True)
    tsne_scatter_plot = tsne_figure.scatter(tsne[0], tsne[1], size=1, color="#3A5785", alpha=0.6)

    tsne_figure.select(BoxSelectTool).select_every_mousemove = False
    tsne_figure.select(LassoSelectTool).select_every_mousemove = False

    def update(attr, old, new):
        global currently_selected_spike_indices
        global update_spike_corr_heatmap_figs
        currently_selected_spike_indices = np.array(new['1d']['indices'])
        num_of_selected_spikes = len(currently_selected_spike_indices)
        if verbose:
            print('Num of selected spikes = '+str(num_of_selected_spikes))

        if num_of_selected_spikes > 0 and update_spike_corr_heatmap_figs:
            # update spike plot
            avg_x = np.mean(cut_extracellular_data[:, :, currently_selected_spike_indices], axis=2)
            spike_mline_plot.data_source.data['ys'] = avg_x.tolist()

            # update autocorelogram
            diffs, norm = crosscorrelate_spike_trains(all_extra_spike_times[currently_selected_spike_indices].astype(np.int64),
                                                      all_extra_spike_times[currently_selected_spike_indices].astype(np.int64), lag=1500)
            hist, edges = np.histogram(diffs, bins=autocor_bin_number)
            hist_plot.data_source.data["top"] = hist
            hist_plot.data_source.data["left"] = edges[:-1] / sampling_freq
            hist_plot.data_source.data["right"] = edges[1:] / sampling_freq

            # update heatmap
            if prb_file is not None:
                data = cut_extracellular_data[:, :, currently_selected_spike_indices]
                final_image, (x_size, y_size) = spike_heatmap.create_heatmap(data, prb_file, rotate_90=True,
                                                                             flip_ud=True, flip_lr=False)
                new_image_data = dict(image=[final_image], x=[0], y=[0], dw=[x_size], dh=[y_size])
                heatmap_data_source.data.update(new_image_data)

    tsne_scatter_plot.data_source.on_change('selected', update)

    # spike plot
    spike_fig_tools = 'pan,wheel_zoom,box_zoom,reset,save'
    spike_figure = figure(toolbar_location='below', plot_width=spike_figure_size[0], plot_height=spike_figure_size[1],
                          tools=spike_fig_tools, title='Spike', min_border=10, webgl=True)

    num_of_channels = cut_extracellular_data.shape[0]
    num_of_time_points = cut_extracellular_data.shape[1]
    xs = np.repeat(np.expand_dims(time_axis, axis=0), repeats=num_of_channels, axis=0).tolist()
    ys = np.ones((num_of_channels, num_of_time_points)).tolist()
    spike_mline_plot = spike_figure.multi_line(xs=xs, ys=ys)

    # autocorelogram plot
    hist, edges = np.histogram([], bins=autocor_bin_number)
    hist_fig_tools = 'pan,wheel_zoom,box_zoom,save,reset'

    hist_figure = figure(toolbar_location='below', plot_width=hist_figure_size[0], plot_height=hist_figure_size[1],
                         tools=hist_fig_tools, title='Autocorrelogram', min_border=10, webgl=True)
    hist_plot = hist_figure.quad(bottom=0, left=edges[:-1], right=edges[1:], top=hist, color="#3A5785", alpha=0.5,
                                 line_color="#3A5785")
    # heatmap plot
    if prb_file is not None:
        data = np.zeros(cut_extracellular_data.shape)
        final_image, (x_size, y_size) = spike_heatmap.create_heatmap(data, prb_file, rotate_90=True,
                                                                     flip_ud=True, flip_lr=False)
        final_image[:, :, ] = 4294967295  # The int32 for the int8 255 (white)
        plot_width = max(heatmap_plot_size[0], int(heatmap_plot_size[1] * y_size / x_size))
        heatmap_plot = figure(toolbar_location='right', plot_width=plot_width, plot_height=heatmap_plot_size[1],
                              x_range=(0, x_size), y_range=(0, y_size))

        heatmap_data_source = ColumnDataSource(data=dict(image=[final_image], x=[0], y=[0], dw=[x_size], dh=[y_size]))
        heatmap_renderer = heatmap_plot.image_rgba(source=heatmap_data_source, image='image', x='x', y='y',
                                                   dw='dw', dh='dh', dilate=False)
        heatmap_plot.axis.visible = None
        heatmap_plot.xgrid.grid_line_color = None
        heatmap_plot.ygrid.grid_line_color = None
    # ---------------------------------------

    # Buttons and controls ------------------
    # the clusters DataTable
    if use_existing_cluster:
        cluster_info = load_cluster_info(cluster_info_file)
    else:
        cluster_info = create_new_cluster_info_file(cluster_info_file)
    cluster_info_data_source = ColumnDataSource(cluster_info)
    clusters_columns = [TableColumn(field='Cluster', title='Clusters'),
                        TableColumn(field='Num_of_Spikes', title='Number of Spikes')]
    clusters_table = DataTable(source=cluster_info_data_source, columns=clusters_columns,selectable=True,
                               editable=False, width=clusters_table_size[0], height=clusters_table_size[1])

    # cluster TextBox that adds cluster to the DataTable
    new_cluster_name_edit = TextInput(value='new cluster', title='Add Cluster')

    def set_new_cluster_name(attr, old, new):
        global currently_selected_spike_indices
        new_cluster_name = new_cluster_name_edit.value
        select_current_cluster_name.options = np.append(select_current_cluster_name.options,
                                                        new_cluster_name).tolist()
        select_current_cluster_name.value = new_cluster_name
        add_cluster_to_cluster_info(cluster_info_file, new_cluster_name, currently_selected_spike_indices)
        clusters_table.source = ColumnDataSource(load_cluster_info(cluster_info_file))

    new_cluster_name_edit.on_change('value', set_new_cluster_name)

    # show cluster Button
    button_show_cluster = Button(label='Show selected cluster')

    def show_cluster():
        cluster_info = load_cluster_info(cluster_info_file)
        indices = cluster_info['Spike_Indices'][select_current_cluster_name.value]
        old = new = tsne_scatter_plot.data_source.selected
        tsne_scatter_plot.data_source.selected['1d']['indices'] = indices
        tsne_scatter_plot.data_source.trigger('selected', old, new)

    button_show_cluster.on_click(show_cluster)

    # show all clusters Button
    button_show_all_clusters = Toggle(label='Show all clusters', type='primary')

    def show_all_clusters(state, *args):
        global update_spike_corr_heatmap_figs
        global tsne_clusters_scatter_plot
        global checkbox_show_clusters_with_colors

        if state:
            cluster_info = load_cluster_info(cluster_info_file)
            num_of_clusters = cluster_info.shape[0]
            indices_list_of_lists = cluster_info['Spike_Indices'].tolist()
            indices = [item for sublist in indices_list_of_lists for item in sublist]
            cluster_indices = np.arange(num_of_clusters)
            if not checkbox_show_clusters_with_colors.active:
                update_spike_corr_heatmap_figs = False
                if verbose:
                    print('Showing all clusters in blue')
                old = new = tsne_scatter_plot.data_source.selected
                tsne_scatter_plot.data_source.selected['1d']['indices'] = indices
                tsne_scatter_plot.data_source.trigger('selected', old, new)
            else:
                if verbose:
                    print('Showing all clusters in colors... wait for it...')
                colors = []
                update_spike_corr_heatmap_figs = False
                for c in cluster_indices:
                    r = np.random.random(size=1) * 255
                    g = np.random.random(size=1) * 255
                    for i in np.arange(len(indices_list_of_lists[c])):
                        colors.append("#%02x%02x%02x" % (int(r), int(g), 50))
                tsne_clusters_scatter_plot = tsne_figure.scatter(tsne[0][indices], tsne[1][indices], size=1,
                                                                 color=colors, alpha=1)
                if verbose:
                    print('Done creating colored clusters')
        else:
            if verbose:
                print('Hiding clusters')
            button_show_all_clusters.update()
            if not checkbox_show_clusters_with_colors.active:
                update_spike_corr_heatmap_figs = False
                old = new = tsne_scatter_plot.data_source.selected
                tsne_scatter_plot.data_source.selected['1d']['indices'] = np.arange(tsne.shape[1])
                tsne_scatter_plot.data_source.trigger('selected', old, new)
            else:
                update_spike_corr_heatmap_figs = False
                tsne_clusters_scatter_plot.data_source.data = {'x': [], 'y': []}

        update_spike_corr_heatmap_figs = True

    button_show_all_clusters.on_click(show_all_clusters)

    # switch between colored and not-colored view of all clusters Checkbox
    global checkbox_show_clusters_with_colors
    checkbox_show_clusters_with_colors = CheckboxGroup(labels=["use colors to show all clusters (slow)"],
                                                       active=[0, 1])

    # delete cluster Button
    button_delete_cluster = Button(label='Delete selected cluster')

    def delete_cluster():
        cluster_info = load_cluster_info(cluster_info_file).drop(select_current_cluster_name.value)
        cluster_info_data_source = ColumnDataSource(cluster_info)
        clusters_table.source = cluster_info_data_source
        select_current_cluster_name.options = cluster_info.index.tolist()

    button_delete_cluster.on_click(delete_cluster)

    # which cluster to show DropDown menu
    select_current_cluster_name = Select(title='Pick cluster to Show or Delete')
    if use_existing_cluster:
        cluster_info = load_cluster_info(cluster_info_file)
        select_current_cluster_name.options = cluster_info.index.tolist()
        select_current_cluster_name.value = cluster_info.index.tolist()[0]

    # -------------------------------------------

    # Layout and session setup ------------------
    # align and make layout
    spike_figure.min_border_top = 50
    spike_figure.min_border_right = 10
    hist_figure.min_border_top = 50
    hist_figure.min_border_left = 10

    if k4:
        layout = hplot(vplot(tsne_figure,
                             hplot(spike_figure,
                                   hist_figure)),
                       vplot(Paragraph(height=10),
                             clusters_table,
                             new_cluster_name_edit,
                             select_current_cluster_name,
                             Paragraph(height=1),
                             vplot(HBox(button_show_cluster, width=50, height=30),
                                   Paragraph(height=1),
                                   HBox(button_delete_cluster, width=50, height=30),
                                   Paragraph(height=1),
                                   hplot(button_show_all_clusters,
                                         checkbox_show_clusters_with_colors)),
                             heatmap_plot),
                       width=layout_size[0], height=layout_size[1])
    else:
        layout = hplot(vplot(tsne_figure,
                             hplot(spike_figure,
                                   hist_figure)),
                       heatmap_plot,
                       vplot(Paragraph(height=2),
                             clusters_table,
                             new_cluster_name_edit,
                             select_current_cluster_name,
                             Paragraph(height=1),
                             vplot(HBox(button_show_cluster, width=50, height=30),
                                   Paragraph(height=1),
                                   HBox(button_delete_cluster, width=50, height=30),
                                   Paragraph(height=1),
                                   hplot(button_show_all_clusters,
                                         checkbox_show_clusters_with_colors))),
                       width=layout_size[0], height=layout_size[1])

    session = push_session(curdoc())
    session.show(layout)  # open the document in a browser
    session.loop_until_closed()  # run forever, requires stopping the interpreter in order to stop :)


