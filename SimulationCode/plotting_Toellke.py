import ast

import matplotlib.pyplot as plt
import numpy as np
from brian2 import *
import Event_detection_Aussel


def create_list_from_timeSeries(file_name):
    """
        Reads a file containing a single line list of floats in scientific notation and returns it as a list of floats.

        Args:
        filename (str): The name of the file to read from.

        Returns:
        list: A list of floats contained in the file.
        """
    with open(file_name, 'r') as file:
        # Read the single line from the file
        data_line = file.readline().strip()

        # Evaluate the line to convert it into a list
        # ast.literal_eval safely evaluates an expression node or a string containing a Python expression
        data_list = ast.literal_eval(data_line)

        return data_list


def plot_lfp(data, name, timestep_ms):
    """
    Plots local field potentials over time and saves the plot as a PNG file.

    Parameters:
        data (list of float): The local field potential data.
        name (str): Specific name to include in the file name and plot title.
        timestep_ms (float): The time interval in milliseconds between each data point.
    """

    print("plotting LFP")
    # Generate time points starting from 0, incrementing by the specified timestep for each data point
    time_points = [i * timestep_ms for i in range(len(data))]

    # Create a plot
    plt.figure(figsize=(10, 5))
    plt.plot(time_points, data, label='Local Field Potentials')
    plt.xlabel('Time (ms)')
    plt.ylabel('Potential (V)')
    plt.title(f'Local Field Potential Over Time: {name}')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Save the figure
    timestamp = (str(datetime.datetime.now().date()) + '_'
                 + str(datetime.datetime.now().time().strftime("%H:%M")).replace(':', '.'))
    filename = f"Out/LFPs/LFP_{name.replace(' ', '_')}_{timestamp}.png"
    #plt.savefig(filename)
    #plt.close()  # Close the plotting window after saving to free up resources


def plot_peak_frequencies(sleep_sleep_off, sleep_sleep_on, wake_sleep_off, wake_sleep_on,
                          sleep_wake_off, sleep_wake_on, wake_wake_off, wake_wake_on):
    # each parameter of form [peak frequency values]

    # Prepare data
    categories = ['input:    \nconnectivity:    \nCAN current:    ', 'sleep\nsleep\noff', 'sleep\nsleep\non',
                  'wake\nsleep\noff', 'wake\nsleep\non', 'sleep\nwake\noff',
                  'sleep\nwake\non', 'wake\nwake\noff', 'wake\nwake\non']

    emptyLableInput = [np.nan, np.nan]
    data = [emptyLableInput, sleep_sleep_off, sleep_sleep_on, wake_sleep_off, wake_sleep_on,
            sleep_wake_off, sleep_wake_on, wake_wake_off, wake_wake_on]

    means = [np.mean(x) for x in data]
    std_devs = [np.std(x) for x in data]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(6, 5))  # Adjust figure size to ensure everything fits well

    # Plotting the error bars
    ax.errorbar(categories, means, yerr=std_devs, fmt='o', color='blue', ecolor='blue', capsize=5)

    # Setting labels and title
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


def plot_power_spectral_density_bands(sleep_sleep_off, sleep_sleep_on, wake_sleep_off, wake_sleep_on,
                                      sleep_wake_off, sleep_wake_on, wake_wake_off, wake_wake_on):
    categories = ['input:    \nconnectivity:    \nCAN current:    ', 'sleep\nsleep\noff',
                  'sleep\nsleep\non', 'wake\nsleep\noff', 'wake\nsleep\non', 'sleep\nwake\noff',
                  'sleep\nwake\non', 'wake\nwake\noff', 'wake\nwake\non']

    emptyLableInput = [[np.nan, np.nan], [np.nan, np.nan], [np.nan, np.nan]]
    data = [emptyLableInput, sleep_sleep_off, sleep_sleep_on, wake_sleep_off, wake_sleep_on,
            sleep_wake_off, sleep_wake_on, wake_wake_off, wake_wake_on]

    # Extract means and standard deviations for Theta (0), Gamma (1), Ripple (2) bands
    theta_means = [np.mean(x[0]) for x in data]
    theta_stds = [np.std(x[0]) for x in data]

    gamma_means = [np.mean(x[1]) for x in data]
    gamma_stds = [np.std(x[1]) for x in data]

    ripple_means = [np.mean(x[2]) for x in data]
    ripple_stds = [np.std(x[2]) for x in data]

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
    ax.set_title('Power in oscillation bands')
    ax.set_xticks(index)  # Ensure ticks are set correctly before setting labels
    ax.set_xticklabels(categories)  # Rotate labels to prevent overlap
    ax.set_xlim(left=0)  # Set the left boundary of the x-axis slightly less than the index of the first category
    ax.legend()

    # Set Y-axis to log scale to match the original plot scale
    ax.set_yscale('log')

    # Set limits and ticks on y-axis to match original plot
    #ax.set_ylim(1e-15, 1e-8)  # Adjust as necessary based on your data range
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


if __name__ == '__main__':

    filename = "Out/Timeseries/time_series_W_S_1A.txt"
    data = create_list_from_timeSeries(filename)
    #plot_lfp(data, "manual_S_S_CAN", 0.9765625)
    spectrum_peaks, band_spectra = Event_detection_Aussel.event_detection_and_analysis(data, "manual_W_S", 1024 * Hz)

    plot_peak_frequencies(spectrum_peaks, spectrum_peaks, spectrum_peaks, spectrum_peaks, spectrum_peaks,
                          spectrum_peaks, spectrum_peaks, spectrum_peaks)
    plot_power_spectral_density_bands(band_spectra, band_spectra, band_spectra, band_spectra, band_spectra,
                                      band_spectra, band_spectra, band_spectra)
