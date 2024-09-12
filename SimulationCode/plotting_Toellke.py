import ast

import matplotlib.pyplot as plt
import numpy as np
from brian2 import *
from Event_detection_Aussel import *
import os


def create_list_from_timeSeries(file_path):
    """
    Reads a file containing a single line list of floats in scientific notation and returns it as a list of floats.

    Parameters:
        file_path (str): The root path of the file to read from.

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


def plot_power_spectral_density(frequencies, power_densities):
    """
        Plots the power spectral density (PSD) against frequency.

        Parameters:
            frequencies (array-like): A list or array of frequency values (in Hz).
            power_densities (array-like): A list or array of power spectral density values corresponding to the frequencies.

        Returns:
            None: This function does not return a value; it directly creates and displays a line plot of the PSD.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(frequencies, power_densities)  # Log scale for better visibility of peaks
    plt.title('Power Spectral Density')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD [V/Hz]')
    plt.show()


def plot_lfp(recordings, sim_label):
    """
    Plots local field potentials over time.

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

    # # Set y-axis tick labels at multiples of 1e-6 from -1e-6 to 5e-6
    # tick_values = [-1.5e-4, -1e-4, 0, 1e-4, 2e-4, 3e-4, 4e-4, 5e-4, 6e-4, 7e-4]
    # tick_labels = ['', '-1', '0', '1', '2', '3', '4', '5', '6', '7']
    # plt.yticks(tick_values, tick_labels)
    #
    # # Add scaling factor above y-axis
    # plt.text(0.01, 1.02, '1e-4', transform=plt.gca().transAxes, ha='left', va='bottom')

    plt.show()


def plot_full_length_lfp(file_path):
    """
        Plots the full-length local field potential (LFP) data from a specified file in 10-second frames.

        Parameters:
            file_path (str): The path to the file containing the LFP time series data.

        Returns:
            None: This function does not return a value; it directly creates and displays plots for each LFP frame.
    """
    recordings = create_list_from_timeSeries(file_path)

    recordings_per_second = 1024
    lfp_frame_length = 10 * recordings_per_second
    lfp_frames_in_recording = len(recordings) // lfp_frame_length

    for i in range(lfp_frames_in_recording):
        lfp_frame = recordings[(0 + i) * lfp_frame_length: (1 + i) * lfp_frame_length]
        plot_lfp(lfp_frame, f"Frame nr. {i + 1}")


def plot_line_diagram(label_value_list, x_label, y_label):
    """
        Plots a line diagram with given categories and values, including comparison values for reference.

        Parameters:
            label_value_list (list of tuples): A list where each tuple contains a category label and its corresponding value
                                                (e.g., [("label1", value1), ("label2", value2), ...]).
            x_label (str): The label for the x-axis.
            y_label (str): The label for the y-axis.

        Returns:
            None: This function does not return a value; it directly creates and displays a line plot.
    """

    categories = [x[0] for x in label_value_list]
    values = [x[1] for x in label_value_list]

    comp_values = [1, 1/2, 1/3, 1/4]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(3, 4))  # Adjust figure size to ensure everything fits well

    # Plotting the line diagram
    ax.plot(categories, comp_values, marker='o', linestyle='-', color="orange")  # comp values
    ax.plot(categories, values, marker='o', linestyle='-')  # Line with markers

    # Setting labels and title
    #ax.set_title(f'Event Peak Frequencies')
    ax.set_ylabel(f"{y_label}")
    ax.set_xlabel(f"{x_label}")
    ax.set_xticks(range(len(categories)))  # Ensure ticks are set correctly before setting labels
    ax.set_xticklabels(categories)  # Rotate labels to prevent overlap

    ax.set_xlim(-0.5, len(categories)-0.5)  # Modify these values to compress or expand the x-axis

    # Adjust layout to make sure nothing gets cut off
    plt.tight_layout()
    plt.show()


def plot_occurrence_frequencies(occurrence_frequencies, parameter_label):
    """
        Plots the occurrence frequencies with error bars representing standard deviations.

        Parameters:
            occurrence_frequencies (list of tuples): A list where each tuple contains a category label and a list of frequency values
                                                      (e.g., [("label1", [value1, value2, ...]), ...]).
            parameter_label (str): The label for the x-axis, indicating the parameter being analyzed.

        Returns:
            None: This function does not return a value; it directly creates and displays a plot with error bars.
    """

    categories = [x[0] for x in occurrence_frequencies]
    means = [np.mean(x[1]) for x in occurrence_frequencies]
    std_devs = [np.std(x[1]) for x in occurrence_frequencies]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(3, 4))  # Adjust figure size to ensure everything fits well

    # Plotting the error bars
    ax.errorbar(categories, means, yerr=std_devs, fmt='o', capsize=8)

    # Setting labels and title
    #ax.set_title(f'Event Peak Frequencies')
    ax.set_ylabel('Frequency of Occurrence (Hz)')
    ax.set_xlabel(f"{parameter_label}")
    ax.set_xticks(range(len(categories)))  # Ensure ticks are set correctly before setting labels
    ax.set_xticklabels(categories)  # Rotate labels to prevent overlap

    ax.set_xlim(-0.5, len(categories)-0.5)  # Modify these values to compress or expand the x-axis

    # Adjust layout to make sure nothing gets cut off
    plt.tight_layout()
    plt.show()


def plot_peak_frequencies(peak_frequencies, parameter_label):
    """
        Plots peak frequencies with error bars representing standard deviations.

        Parameters:
            peak_frequencies (list of tuples): A list where each tuple contains a category label and a list of peak frequency values
                                                (e.g., [("label1", [value1, value2, ...]), ...]).
            parameter_label (str): The label for the x-axis, indicating the parameter being analyzed.

        Returns:
            None: This function does not return a value; it directly creates and displays a plot with error bars for peak frequencies.
    """

    categories = [x[0] for x in peak_frequencies]
    means = [np.mean(x[1]) for x in peak_frequencies]
    std_devs = [np.std(x[1]) for x in peak_frequencies]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(3, 4))  # Adjust figure size to ensure everything fits well

    # Plotting the error bars
    ax.errorbar(categories, means, yerr=std_devs, fmt='o', capsize=8)

    # Setting labels and title
    #ax.set_title(f'Event Peak Frequencies')
    ax.set_ylabel('Peak Frequency (Hz)')
    ax.set_xlabel(f"{parameter_label}")
    ax.set_xticks(range(len(categories)))  # Ensure ticks are set correctly before setting labels
    ax.set_xticklabels(categories)  # Rotate labels to prevent overlap

    ax.set_xlim(-0.5, len(categories)-0.5)  # Modify these values to compress or expand the x-axis
    ax.set_ylim(0, 200)
    ax.set_yticks(np.arange(0, 176, 25))
    # Adjust layout to make sure nothing gets cut off
    plt.tight_layout()
    plt.show()


def plot_power_spectral_density_bands(psd_bands, label):
    """
        Plots the power spectral density (PSD) for different frequency bands (Theta, Gamma, Ripple) with error bars.

        Parameters:
            psd_bands (list of tuples): A list where each tuple contains a parameter label and a list of lists representing
                                         the power values for different bands (e.g., [("label1", [[theta_band], [gamma_band], [ripple_band]]), ...]).
            label (str): The label for the x-axis, indicating the parameter being analyzed.

        Returns:
            None: This function does not return a value; it directly creates and displays a bar plot with error bars for each frequency band.
    """

    categories = [x[0] for x in psd_bands]
    # Extract means and standard deviations for Theta (0), Gamma (1), Ripple (2) bands
    theta_means = [np.mean(x[1][0]) for x in psd_bands]
    theta_stds = [np.std(x[1][0]) for x in psd_bands]

    gamma_means = [np.mean(x[1][1]) for x in psd_bands]
    gamma_stds = [np.std(x[1][1]) for x in psd_bands]

    ripple_means = [np.mean(x[1][2]) for x in psd_bands]
    ripple_stds = [np.std(x[1][2]) for x in psd_bands]

    # Number of groups
    n_groups = len(categories)
    fig, ax = plt.subplots(figsize=(4, 4)) # for 1: (3, 4)

    # Set position of bar on X axis
    index = np.arange(n_groups)
    bar_width = 0.13 # for 1: 0.075
    cap_size = 3

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
    ax.set_ylabel('Power ($V^2$)')
    #ax.set_title(f'Power in Oscillation Bands')
    ax.set_xlabel(f"{label}")
    ax.set_xticks(index)  # Ensure ticks are set correctly before setting labels
    ax.set_xticklabels(categories)  # Rotate labels to prevent overlap
    ax.legend()

    # Set Y-axis to log scale to match the original plot scale
    ax.set_yscale('log')

    # Set limits and ticks on y-axis to match original plot
    ax.set_xlim(-0.5, len(categories) - 0.5)
    ax.set_ylim(1e-18, 1e-8)  # Adjust as necessary based on your data range
    ax.yaxis.set_tick_params(which='both', labelleft=True)

    fig.tight_layout()
    plt.show()


def single_file_lfp_analysis(file_path, showLFP, showEventLFP, label):
    """
        Analyzes a single local field potential (LFP) file by extracting data, detecting events, and generating plots.

        Parameters:
            file_path (str): The path to the file containing the LFP time series data.
            showLFP (bool): A flag indicating whether to plot the general LFP recording.
            showEventLFP (bool): A flag indicating whether to plot individual event LFPs.
            label (str): A label for the plots, typically indicating the simulation or experiment context.

        Returns:
            None: This function does not return a value; it directly creates and displays plots based on the analysis.
    """
    # extract and analyse data
    recordings = create_list_from_timeSeries(file_path)
    spectrum_peaks, band_spectra, all_events = event_detection_and_analysis(recordings, label, 1024 * Hz)
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
    # lfp_recording_samples.append(recordings[1824:12064]) # 5s recording, starting at 1s

    # Event LFPs
    sample_event_idxs = []

    num_events = len(events)
    if num_events:
        if num_events < 4:
            sample_event_idxs = [0]
        else:
            sample_event_idxs = [num_events // 4, num_events // 2 + num_events // 4]

    # generate plots
    if showLFP:
        for recording_sample in lfp_recording_samples:
            plot_lfp(recording_sample, f"{label}")

    if showEventLFP:
        for idx in sample_event_idxs:
            plot_lfp(events[idx], f"Event {str(idx)} in {label} - raw")
            plot_lfp(filtered_events[idx], f"Event {str(idx)} in {label} - filtered")


def sim_collection_analysis(collection_folder_path, chat_output, do_plots):
    """
        Analyzes a collection of simulation configurations by aggregating data from multiple files and generating summary statistics and plots.

        Parameters:
            collection_folder_path (str): The path to the folder containing simulation data files.
            chat_output (bool): A flag indicating whether to print summary statistics to the console.
            do_plots (bool): A flag indicating whether to generate and display plots based on the aggregated data.

        Returns:
            list: A list containing the number of events detected in each simulation configuration.
    """
    research_parameter, parameter_value = collection_folder_path.split("/")[-2:]
    parameter_value = parameter_value.lstrip("0")
    sim_label = f'{research_parameter} = {parameter_value}'

    all_num = []
    all_peaks = []
    all_bands = []
    all_occ_freq = []

    # aggregate data from collection
    for entity in os.listdir(collection_folder_path)[:9]:

        file_path = f'{collection_folder_path}/{entity}'
        recordings = create_list_from_timeSeries(file_path)
        spectrum_peaks, band_spectra, all_events = event_detection_and_analysis(recordings, sim_label, 1024 * Hz)
        events, filtered_events = all_events

        value_w = entity.split('_')[0][1]
        sim_time_int = int(entity.split('_')[1][:2])
        num_events = len(events)
        occ_freq = num_events/sim_time_int

        all_num.append(num_events)
        all_peaks.append((f"{value_w}", spectrum_peaks))
        all_bands.append((f"{value_w}", band_spectra))
        all_occ_freq.append((f"{value_w}", occ_freq))


    # display data
    if chat_output:
        print(f'\n___ {sim_label} ___\n')
        print(f"Average Events per minute : {mean(all_num)}")
        print(f"Average peak frequency: {mean([mean(x[1]) for x in all_peaks])}")


    if do_plots:
        plot_power_spectral_density_bands(all_bands, "Wave Realization Interval (w)")
        plot_peak_frequencies(all_peaks, "Wave Realization Interval (w)")
        plot_line_diagram(all_occ_freq, "Wave Realization Interval (w)", "Frequency of Occurrence (Hz)")


    return all_num


if __name__ == '__main__':
    # final vs eeg
    single_file_lfp_analysis("Out/Timeseries/S_S/S_S_15s__RP3__2024-09-02_22.37.41.txt", 1, 1, "f1.5-w4")
    single_file_lfp_analysis("Out/Timeseries/S_S/S_S_60s__EEG__2024-08-28_23.17.52.txt", 1, 1, "EEG")


    sim_collection_analysis("sorted_output/w_analysis", 1, 1)
