import ast

import matplotlib.pyplot as plt
import numpy as np
from brian2 import *
from Event_detection_Toellke import *
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


def extract_sim_parameters(folder_path):
    file_path = f'{folder_path}/parameters.txt'

    with open(file_path, 'r') as file:
        file_lines = file.readlines()

        parameters = {}

        for line in file_lines:
            stripped_line = line.strip()
            param_name, value = stripped_line.split(": ")

            parameters[param_name] = value

    # Format parameters
    parameters["runtime"] = parameters["runtime"].replace(". ", "")

    return parameters


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
    plt.figure(figsize=(10, 4))
    plt.plot(time_points, recordings, label='Local Field Potentials')
    plt.xlabel('Time (ms)')
    plt.ylabel('Potential (V)')
    plt.title(f'{sim_label}')
    plt.grid(True)

    # Set y-axis tick labels at multiples of 1e-6 from -1e-6 to 5e-6
    tick_values = [-1e-4, 0, 1e-4, 2e-4, 3e-4]
    tick_labels = ['-1', '0', '1', '2', '3']
    plt.yticks(tick_values, tick_labels)

    # Add scaling factor above y-axis
    plt.text(0.01, 1.02, '1e-4', transform=plt.gca().transAxes, ha='left', va='bottom')

    plt.show()



def plot_full_length_lfp(file_path):
    recordings = create_list_from_timeSeries(file_path)

    recordings_per_second = 1024
    lfp_frame_length = 10 * recordings_per_second
    lfp_frames_in_recording = len(recordings) // lfp_frame_length

    for i in range(lfp_frames_in_recording):
        lfp_frame = recordings[(0 + i) * lfp_frame_length: (1 + i) * lfp_frame_length]
        plot_lfp(lfp_frame, f"Frame nr. {i + 1}")


def plot_line_diagram(label_value_list, x_label, y_label, title="", comp_values=[]):
    # peak_frequencies of form [("parameter_value, [d,a,t,a]"), ...]

    if len(comp_values) == 0:
        for x in label_value_list:
            comp_values.append(("", np.nan))


    categories = [x[0] for x in label_value_list]
    values = [mean(x[1]) for x in label_value_list]
    standard_deviations = [np.std(x[1]) for x in label_value_list]
    comp_mean_values = [mean(x[1]) for x in comp_values]
    comp_std_values = [np.std(x[1]) for x in comp_values]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(3, 4))  # Adjust figure size to ensure everything fits well

    # Plotting the line diagram
    ax.plot(categories, values, marker='o', linestyle='-')  # Line with markers
    ax.plot(categories, comp_mean_values, marker='o', linestyle='-', color="green")  # comp values
    # ax.errorbar(categories, values, yerr=standard_deviations, fmt='o', capsize=7)


    # Setting labels and title
    if title != "":
        ax.set_title(f'Event Peak Frequencies')
    ax.set_ylabel(f"{y_label}")
    ax.set_xlabel(f"{x_label}")
    ax.set_xticks(range(len(categories)))  # Ensure ticks are set correctly before setting labels
    ax.set_xticklabels(categories)  # Rotate labels to prevent overlap

    ax.set_xlim(-0.5, len(categories)-0.5)  # Modify these values to compress or expand the x-axis

    # Adjust layout to make sure nothing gets cut off
    plt.tight_layout()
    plt.show()


def plot_occurrence_frequencies(occurrence_frequencies, parameter_label, title="", comp_frequencies=[]):
    # peak_frequencies of form [("parameter_value, [d,a,t,a]"), ...]

    if len(comp_frequencies) == 0:
        for x in occurrence_frequencies:
            comp_frequencies.append(("", np.nan))


    categories = [x[0] for x in occurrence_frequencies]
    means = [np.mean(x[1]) for x in occurrence_frequencies]
    std_devs = [np.std(x[1]) for x in occurrence_frequencies]

    comp_means = [np.mean(x[1]) for x in comp_frequencies]
    comp_std_devs = [np.std(x[1]) for x in comp_frequencies]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(3, 4))  # Adjust figure size to ensure everything fits well

    # Plotting the error bars
    ax.errorbar(categories, means, yerr=std_devs, fmt='o', capsize=7)
    ax.errorbar(categories, comp_means, yerr=comp_std_devs, fmt='o', capsize=7, color='green')
    # ax.errorbar(categories, comp_means, fmt='o', color='green')

    # Setting labels and title
    if title != "":
        ax.set_title(f'{title}')
    ax.set_ylabel('Frequency of Occurrence (Hz)')
    ax.set_xlabel(f"{parameter_label}")
    ax.set_xticks(range(len(categories)))  # Ensure ticks are set correctly before setting labels
    ax.set_xticklabels(categories)  # Rotate labels to prevent overlap

    ax.set_xlim(-0.5, len(categories)-0.5)  # Modify these values to compress or expand the x-axis

    # Adjust layout to make sure nothing gets cut off
    plt.tight_layout()
    plt.show()


def plot_frequency_distribution(frequencies, label):
    # Define the bins for 20 Hz intervals from 20 Hz to 300 Hz
    bins = np.arange(20, 251, 10)

    # Count the occurrences of frequencies in each bin
    counts, _ = np.histogram(frequencies, bins=bins)

    # Create bar positions (the center of each bin)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    # Create a color array for the bars
    colors = ['green' if (100 <= center <= 250) else 'grey' for center in bin_centers]

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.bar(bin_centers, counts, width=7.5, color=colors, edgecolor='black')

    # Setting the labels and title
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Peak Frequency Occurrences')
    plt.title(f'Event Peak Frequencies in: {label}')
    plt.xticks(bins)  # Set x-ticks to be at the edges of the bins
    #plt.ylim(0, 5)  # Set y-axis limit from 0 to 5

    # Show grid for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Show the plot
    plt.show()


def plot_peak_frequencies(peak_frequencies, parameter_label, title="", comp_frequencies=[]):
    # peak_frequencies of form [("parameter_value, [d,a,t,a]"), ...]

    if len(comp_frequencies) == 0:
        for x in peak_frequencies:
            comp_frequencies.append(("", np.nan))


    categories = [x[0] for x in peak_frequencies]
    means = [np.mean(x[1]) for x in peak_frequencies]
    std_devs = [np.std(x[1]) for x in peak_frequencies]
    comp_means = [np.mean(x[1]) for x in comp_frequencies]
    comp_std_devs = [np.std(x[1]) for x in comp_frequencies]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(3, 4))  # or (4, 4) Adjust figure size to ensure everything fits well

    # Plotting the error bars
    ax.errorbar(categories, means, yerr=std_devs, fmt='o', capsize=7)
    #ax.errorbar(categories, comp_means, yerr=comp_std_devs, fmt='o', capsize=7, color='green')
    ax.errorbar(categories, comp_means, fmt='o-', color='green')


    # Setting labels and title
    if title != "":
        ax.set_title(f'{title}')
    ax.set_ylabel('Peak Frequency (Hz)')
    ax.set_xlabel(f"{parameter_label}")
    ax.set_xticks(range(len(categories)))  # Ensure ticks are set correctly before setting labels
    ax.set_xticklabels(categories)  # Rotate labels to prevent overlap

    ax.set_xlim(-0.5, len(categories) - 0.5)  # Modify these values to compress or expand the x-axis
    ax.set_ylim(0, 200)
    ax.set_yticks(np.arange(0, 176, 25))
    # Adjust layout to make sure nothing gets cut off
    plt.tight_layout()
    plt.show()


def plot_power_spectral_density_bands(psd_bands, label, title=""):
    #psd_bands of from: [(parameter_value, [[theta_band], [gamma_band], [ripple_band]]), ...]

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
    bar_width = 0.14 # for 1: 0.075
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

    if title != "":
        ax.set_title(f'{title}')
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


def plot_power_spectral_density(frequencies, power_densities):
    plt.figure(figsize=(10, 5))
    plt.plot(frequencies, power_densities)  # Log scale for better visibility of peaks
    plt.title('Power Spectral Density')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD [V/Hz]')
    plt.show()


def single_sim_analysis(file_path, showLFP, showEventLFP):
    sim_label, research_param = file_path.split("/")[-3:-1]

    # extract and analyse data
    recordings = create_list_from_timeSeries(file_path)
    [events, filtered_events, all_spectrum_peaks, all_duration], [sharp_wave_ripples, sharp_wave_ripple_peaks, sharp_wave_ripple_durations], band_spectra = event_detection(recordings)

    #sharp_wave_ripples = Event_detection_Aussel.event_identification_analysis(recordings, sim_label, 1024 * Hz)

    # prepare plotting parameters
    # General LFP

    if len(recordings) > 40960:
        lfp_recording_sample = recordings[20480:30720]  # 10s recording, starting at 30s
    elif len(recordings) < 6144:
        lfp_recording_sample = recordings  # if shorter than 6s, plot all
    else:
        lfp_recording_sample = recordings[1024:6144]  # 5s recording, starting at 1s


    # generate plots
    if showLFP:
        plot_lfp(lfp_recording_sample, f"{sim_label} = {research_param}")

    if showEventLFP:
        for event in sharp_wave_ripples[:2]:
            plot_lfp(event, "Sharp wave ripple")
        for x in [x for x in events if x not in sharp_wave_ripples][:2]:
            plot_lfp(x, "No SWR")

    plot_frequency_distribution(all_spectrum_peaks, sim_label)
    # plot_peak_frequencies([(research_param, all_spectrum_peaks),], sim_label)
    # plot_power_spectral_density_bands([(research_param, band_spectra),], sim_label)



def sim_collection_analysis(collection_folder_path, chat_output, do_plots):
    # Facilitates analysis of a single simulation configuration

    research_parameter, parameter_value = collection_folder_path.split("/")[-2:]
    parameter_value = parameter_value.lstrip("0")
    sim_label = f'{research_parameter} = {parameter_value}'

    all_num = []
    all_occ_freq = []
    all_peaks = []
    all_dur = []

    swr_num = []
    swr_occ_freq = []
    swr_peaks = []
    swr_dur = []

    band_powers = [[], [], []] # theta, gamma, ripple

    # aggregate data from collection
    for entity in os.listdir(collection_folder_path)[:8]:

        file_path = f'{collection_folder_path}/{entity}'
        recordings = create_list_from_timeSeries(file_path)
        [events, filtered_events, all_spectrum_peaks, all_duration], [sharp_wave_ripples, sharp_wave_ripple_peaks, sharp_wave_ripple_durations], band_spectra = event_detection(recordings)

        num_all = len(events)
        all_num.append(num_all)
        all_occ_freq.append(num_all/60)
        all_peaks.extend(all_spectrum_peaks)
        all_dur.extend(all_duration)

        num_swrs = len(sharp_wave_ripples)
        swr_num.append(num_swrs)
        swr_occ_freq.append(num_swrs/60)
        swr_peaks.extend(sharp_wave_ripple_peaks)
        swr_dur.extend(sharp_wave_ripple_durations)

        for i, x in enumerate(band_spectra):
            band_powers[i].extend(x)


    # display data
    if chat_output:
        print(f'\n___ {sim_label} ___\n')
        print(f"Average Events per minute : {mean(all_num)}")
        print(f"Average peak frequency : {mean(all_peaks)}")
        print(f"Average Event duration : {mean(all_dur)} ms")
        print("--------------------------------------------")
        print(f"Average Sharp Wave Ripples per minute : {mean(swr_num)}")
        print(f"Average Sharp Wave Ripple peak frequency : {mean(swr_peaks)}")
        print(f"Average Sharp Wave Ripple duration : {mean(swr_dur)} ms")

    if do_plots:
        plot_frequency_distribution(all_peaks, sim_label)


    all_data = [all_num, all_occ_freq, all_peaks, all_dur]
    swr_data = [swr_num, swr_occ_freq, swr_peaks, swr_dur]

    return all_data, swr_data, band_powers


def parameter_comparison(main_folder_path, reverse_analysis, do_chat, do_plots):
    parameter_label = main_folder_path.split("/")[-1]

    all_peak_lists = []
    all_occ_freq_lists = []
    swr_peak_lists = []
    swr_occ_freq_lists = []
    swr_dur_lists = []
    band_power_lists = []


    [all_num, all_occ_freq, all_peaks, all_dur], [swr_num, swr_occ_freq, swr_peaks, swr_dur], band_powers = sim_collection_analysis("sorted_results/sleep/healthy", do_chat, do_plots)
    all_peak_lists.append(("healthy", all_peaks))
    all_occ_freq_lists.append(("healthy", all_occ_freq))
    swr_peak_lists.append(("healthy", swr_peaks))
    swr_occ_freq_lists.append(("healthy", swr_occ_freq))
    swr_dur_lists.append(("healthy", swr_dur))
    band_power_lists.append(("healthy", band_powers))


    parameter_values = sorted(os.listdir(main_folder_path), reverse=reverse_analysis)

    for parameter in parameter_values:
        parameter_folder_path = f"{main_folder_path}/{parameter}"
        clean_param_string = parameter.lstrip("0")

        [all_num, all_occ_freq, all_peaks, all_dur], [swr_num, swr_occ_freq, swr_peaks, swr_dur], band_powers = sim_collection_analysis(parameter_folder_path, do_chat, do_plots)
        all_peak_lists.append((clean_param_string, all_peaks))
        all_occ_freq_lists.append((clean_param_string, all_occ_freq))
        swr_peak_lists.append((clean_param_string, swr_peaks))
        swr_occ_freq_lists.append((clean_param_string, swr_occ_freq))
        swr_dur_lists.append((clean_param_string, swr_dur))
        band_power_lists.append((clean_param_string, band_powers))


    # Peak Frequencies
    plot_peak_frequencies(all_peak_lists, parameter_label, title="Comparison", comp_frequencies=swr_peak_lists)
    # plot_peak_frequencies(all_peak_lists, parameter_label, title="All Events")
    # plot_peak_frequencies(swr_peak_lists, parameter_label, title="Sharp Wave Ripples")

    # Event Occurrence
    plot_occurrence_frequencies(all_occ_freq_lists, parameter_label, title="Comparison", comp_frequencies=swr_occ_freq_lists)
    # plot_occurrence_frequencies(swr_occ_freq_lists, parameter_label, title="Sharp Wave Ripples")

    # Durations
    plot_line_diagram(swr_dur_lists, parameter_label, "Mean SWR Duration (ms)")

    # Power in Oscillation bands
    plot_power_spectral_density_bands(band_power_lists, parameter_label)

    # More
    # plot_line_diagram(swr_occ_freq_lists, parameter_label, "Occurrence Frequency (Hz)", 1, [mean(x[1]) for x in all_occ_freq_lists])


if __name__ == '__main__':

    doChat = 1
    doPlots = 1
    reversed_analysis = 0

    parameter_comparison("sorted_results/sleep/gCAN", reversed_analysis, doChat, doPlots)

    # single_sim_analysis("sorted_results/sleep/healthy/LFP_08-11_[0].txt", 1, 0)
