import matplotlib.pyplot as plt
import numpy as np
from brian2 import *


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

    # Save the figure
    filename = f"Out/LFPs/LFP_{name.replace(' ', '_')}_{str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')}.png"
    plt.savefig(filename)
    plt.close()  # Close the plotting window after saving to free up resources


def plot_peak_frequencies(sleep_sleep_off, sleep_sleep_on, wake_sleep_off, wake_sleep_on,
                          sleep_wake_off, sleep_wake_on, wake_wake_off, wake_wake_on):
    print("plotting frequencies")
    # each parameter of form [mean peak frequency, standard deviation of peak frequencies]

    emptyLableInput = [np.nan, np.nan]
    # Prepare data
    categories = ['input:    \nconnectivity:    \nCAN current:    ', 'sleep\nsleep\noff', 'sleep\nsleep\non', 'wake\nsleep\noff', 'wake\nsleep\non',
                  'sleep\nwake\noff', 'sleep\nwake\non', 'wake\nwake\noff', 'wake\nwake\non']
    means = [x[0] for x in [emptyLableInput, sleep_sleep_off, sleep_sleep_on, wake_sleep_off, wake_sleep_on,
                            sleep_wake_off, sleep_wake_on, wake_wake_off, wake_wake_on]]
    std_devs = [x[1] for x in [emptyLableInput, sleep_sleep_off, sleep_sleep_on, wake_sleep_off, wake_sleep_on,
                               sleep_wake_off, sleep_wake_on, wake_wake_off, wake_wake_on]]

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

    # Save plot as PNG file
    uniq_filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')
    plt.savefig('Out/Events/eventParameters_'+uniq_filename+'.png')


plot_peak_frequencies([100, 10], [150, 15], [80, 8], [130, 13],
                      [70, 7], [120, 12], [60, 6], [110, 11])
