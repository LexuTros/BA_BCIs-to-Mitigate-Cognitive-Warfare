import ast

import matplotlib.pyplot as plt
import numpy as np
from brian2 import *
import Event_detection_Aussel


def create_list_from_timeSeries(file_path):
    """
        Reads a file containing a single line list of floats in scientific notation and returns it as a list of floats.

        Args:
        filename (str): The name of the file to read from.

        Returns:
        list: A list of floats contained in the file.
        """
    with open(file_path, 'r') as file:
        # Read the single line from the file
        data_line = file.readline().strip()

        # Evaluate the line to convert it into a list
        # ast.literal_eval safely evaluates an expression node or a string containing a Python expression
        data_list = ast.literal_eval(data_line)

        return data_list


def plot_lfp(recordings, sim_label):
    """
    Plots local field potentials over time and saves the plot as a PNG file.

    Parameters:
        recordings (list of float): The local field potential data.
        sim_label (str): Specific name to include in the file name and plot title.
    """

    timestep_ms = 0.9765625
    # Generate time points starting from 0, incrementing by the specified timestep for each data point
    time_points = [i * timestep_ms for i in range(len(recordings))]

    # Create a plot
    plt.figure(figsize=(10, 5))
    plt.plot(time_points, recordings, label='Local Field Potentials')
    plt.xlabel('Time (ms)')
    plt.ylabel('Potential (V)')
    #plt.ylim(top=5e-6, bottom=-1e-6)
    plt.title(f'Local Field Potential Over Time: {sim_label}')
    plt.grid(True)
    plt.show()

    # Save the figure
    #timestamp = (str(datetime.datetime.now().date()) + '_'
    #             + str(datetime.datetime.now().time().strftime("%H:%M")).replace(':', '.'))
    #filename = f"Out/LFPs/LFP_{sim_label.replace(' ', '_')}_{timestamp}.png"
    #plt.savefig(filename)
    #plt.close()  # Close the plotting window after saving to free up resources


def plot_peak_frequencies(peak_frequencies, sim_time_str):
    # parameter of form [[sleep_sleep_off], [sleep_sleep_on], [wake_sleep_off], [wake_sleep_on],
    #                           [sleep_wake_off], [sleep_wake_on], [wake_wake_off], [wake_wake_on]]

    # Prepare data
    categories = ['input:    \nconnectivity:    \nCAN current:    ', 'sleep\nsleep\noff', 'sleep\nsleep\non',
                  'wake\nsleep\noff', 'wake\nsleep\non', 'sleep\nwake\noff',
                  'sleep\nwake\non', 'wake\nwake\noff', 'wake\nwake\non']

    emptyLabelInput = [np.nan, np.nan]
    peak_frequencies.insert(0, emptyLabelInput)

    means = [np.mean(x) for x in peak_frequencies]
    std_devs = [np.std(x) for x in peak_frequencies]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(6, 5))  # Adjust figure size to ensure everything fits well

    # Plotting the error bars
    ax.errorbar(categories, means, yerr=std_devs, fmt='o', color='blue', ecolor='blue', capsize=5)

    # Setting labels and title
    ax.set_title(f'Frequencies with highest power - {sim_time_str} simulation')
    ax.set_ylabel('Peak Frequency (Hz)')
    ax.set_xticks(range(len(categories)))  # Ensure ticks are set correctly before setting labels
    ax.set_xticklabels(categories)  # Rotate labels to prevent overlap

    ax.set_xlim(left=0)  # Set the left boundary of the x-axis slightly less than the index of the first category
    ax.set_ylim(0, 200)
    ax.set_yticks(np.arange(0, 176, 25))
    # Adjust layout to make sure nothing gets cut off
    plt.tight_layout()
    plt.show()

    # Save plot as PNG file
    timestamp = (str(datetime.datetime.now().date()) + '_'
                 + str(datetime.datetime.now().time().strftime("%H:%M")).replace(':', '.'))
    #plt.savefig('Out/Events/eventParameters_after_' + str(int(runtime)) + 's__' + timestamp + '.png')


def plot_power_spectral_density_bands(psd_bands, sim_time_str):
    # parameter of form [[sleep_sleep_off], [sleep_sleep_on], [wake_sleep_off], [wake_sleep_on],
    #                           [sleep_wake_off], [sleep_wake_on], [wake_wake_off], [wake_wake_on]]
    #       with [sleep_sleep_off] = [[theta_band], [gamma_band], [ripple_band]]

    categories = ['input:    \nconnectivity:    \nCAN current:    ', 'sleep\nsleep\noff',
                  'sleep\nsleep\non', 'wake\nsleep\noff', 'wake\nsleep\non', 'sleep\nwake\noff',
                  'sleep\nwake\non', 'wake\nwake\noff', 'wake\nwake\non']

    emptyLabelInput = [[np.nan, np.nan], [np.nan, np.nan], [np.nan, np.nan]]
    psd_bands.insert(0, emptyLabelInput)

    # Extract means and standard deviations for Theta (0), Gamma (1), Ripple (2) bands
    theta_means = [np.mean(x[0]) for x in psd_bands]
    theta_stds = [np.std(x[0]) for x in psd_bands]

    gamma_means = [np.mean(x[1]) for x in psd_bands]
    gamma_stds = [np.std(x[1]) for x in psd_bands]

    ripple_means = [np.mean(x[2]) for x in psd_bands]
    ripple_stds = [np.std(x[2]) for x in psd_bands]

    # Number of groups
    n_groups = len(categories)
    fig, ax = plt.subplots()

    # Set position of bar on X axis
    index = np.arange(n_groups)
    bar_width = 0.19
    cap_size = 3.5

    rects1 = ax.bar(index - bar_width, ripple_means, bar_width, yerr=ripple_stds,
                    color='orange', label='Ripple band', capsize=cap_size,
                    error_kw={'zorder': 2}, zorder=3)

    rects2 = ax.bar(index, gamma_means, bar_width, yerr=gamma_stds,
                    color='green', label='Gamma band', capsize=cap_size,
                    error_kw={'zorder': 2}, zorder=3)

    rects3 = ax.bar(index + bar_width, theta_means, bar_width, yerr=theta_stds,
                    color='blue', label='Theta band', capsize=cap_size,
                    error_kw={'zorder': 2}, zorder=3)

    # Axis labels etc.
    ax.set_ylabel('Power (V^2)')
    ax.set_title(f'Power in oscillation bands - {sim_time_str} simulation')
    ax.set_xticks(index)  # Ensure ticks are set correctly before setting labels
    ax.set_xticklabels(categories)  # Rotate labels to prevent overlap
    ax.set_xlim(left=0)  # Set the left boundary of the x-axis slightly less than the index of the first category
    ax.legend()

    # Set Y-axis to log scale to match the original plot scale
    ax.set_yscale('log')

    # Set limits and ticks on y-axis to match original plot
    ax.set_ylim(1e-18, 1e-8)  # Adjust as necessary based on your data range
    ax.yaxis.set_tick_params(which='both', labelleft=True)

    fig.tight_layout()
    plt.show()


def plot_power_spectral_density(frequencies, power_densities):
    plt.figure(figsize=(10, 5))
    plt.plot(frequencies, power_densities)  # Log scale for better visibility of peaks
    plt.title('Power Spectral Density')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD [V/Hz]')
    plt.show()


def single_file_analysis(file_path, showLFP, showEventLFP):
    # Extract strings from path
    sim_type, file_name = file_path.split("/")[-2:]
    sim_label = file_name.split("__")[0]
    sim_time = sim_label.split("_")[-1]
    research_param = file_name.split("__")[1]

    # extract and analyse data
    recordings = create_list_from_timeSeries(file_path)
    spectrum_peaks, band_spectra, all_events = Event_detection_Aussel.event_detection_and_analysis(recordings, sim_label, 1024 * Hz)
    events, filtered_events = all_events

    # prepare plotting parameters
    # General LFP
    lfp_recording_samples = []

    if len(recordings) >= 30720:
        lfp_recording_samples.append(recordings[20480:30721]) # 10s recording, starting at 20s
    elif len(recordings) < 6144:
        lfp_recording_samples.append(recordings) # if shorter than 6s, plot all
    else:
        lfp_recording_samples.append(recordings[1024:6144]) # 5s recording, starting at 1s

    # Event LFPs
    sample_event_idxs = []

    num_events = len(events)
    if num_events:
        if num_events < 4:
            sample_event_idxs = [0]
        else:
            sample_event_idxs = [num_events // 4, num_events // 2 + num_events // 4]

    # Spectra analysis
    spectrum_peaks_parameter = [[np.nan, np.nan] for x in range(8)]
    band_spectra_parameter = [[[np.nan, np.nan], [np.nan, np.nan], [np.nan, np.nan]] for x in range(8)]

    plotting_parameter_order = ['S_S', 'S_S_CAN', 'W_S', 'W_S_CAN', 'S_W_noCAN', 'S_W', 'W_W_noCAN', 'W_W',]
    sim_type_idx = plotting_parameter_order.index(sim_type)

    spectrum_peaks_parameter[sim_type_idx] = spectrum_peaks
    band_spectra_parameter[sim_type_idx] = band_spectra

    # generate plots
    if showLFP:
        for recording_sample in lfp_recording_samples:
            plot_lfp(recording_sample, f"{research_param}")

    if showEventLFP:
        for idx in sample_event_idxs:
            plot_lfp(events[idx], f"Event {str(idx)} in {sim_label} - raw")
            plot_lfp(filtered_events[idx], f"Event {str(idx)} in {sim_label} - filtered")

    #plot_peak_frequencies(spectrum_peaks_parameter, sim_time)
    plot_power_spectral_density_bands(band_spectra_parameter, sim_time)

    print("\n")


if __name__ == '__main__':

    # single_file_analysis("Out/Timeseries/S_S/S_S_60s__RP6__2024-08-07_05.07.50.txt", 0, 0)
    # single_file_analysis("Out/Timeseries/S_S/S_S_60s__RP9__2024-08-07_05.38.16.txt", 0, 0)
    # single_file_analysis("Out/Timeseries/S_S/S_S_60s__RP12__2024-08-07_05.34.49.txt", 0, 0)

    single_file_analysis("Out/Timeseries/S_S/S_S_60s__RP4__2024-08-08_12.28.19.txt", 1, 0)
    single_file_analysis("Out/Timeseries/S_S/S_S_60s__RP6__2024-08-08_10.55.23.txt", 1, 0)
    single_file_analysis("Out/Timeseries/S_S/S_S_60s__RP8__2024-08-08_11.26.48.txt", 1, 0)


