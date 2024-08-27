import brian2
from brian2 import *
import scipy
from scipy import signal
import time
import numpy as np


def generate_input(A1, f1, wave_realization_interval, noise_scaling_factor, sim_time):
    """
    Generates a synthetic square wave input signal for simulations based on specific parameters, including frequency modulation and noise addition.

    Parameters:
        A1 (float): Amplitude of the input signal.
        f1 (float): Base frequency of the input signal in Hz.
        wave_realization_interval (int): Controls the frequency of wave realization by specifying how often (in terms of number of cycles) the wave amplitude is set to A1.
        noise_scaling_factor (float): Factor that determines the level of random noise added to the signal. It scales the noise to a fraction of the maximum amplitude.
        sim_time (int * second): Total duration for which the input signal is generated, specified as an integer multiplied by the 'second' unit from the brian2 library.

    Returns:
        TimedArray: A brian2 TimedArray object containing the scaled and noisy input signal as frequency values, sampled at 1024Hz.
    """

    record_dt = 1. / 1024 * second  # Sampling interval for TimedArray
    t0 = 0.250  # Start time of input

    # Time array
    times = np.arange(0 * second, sim_time, record_dt)

    # Generate square wave
    input_values = np.zeros_like(times)

    def is_in_correct_cycle(input_frequency, current_time, wave_realization_int):
        ms_per_cycle = 1 / input_frequency
        wave_number = int((current_time - t0) / ms_per_cycle)
        return wave_number % wave_realization_int == 0

    for i, t in enumerate(times):
        if t >= t0 and np.sin(2 * np.pi * f1 * (t - t0)) >= 0:
            if is_in_correct_cycle(f1, t, wave_realization_interval):
                input_values[i] = A1


    # Normalize values to range [0, 1]
    input_normalized = (input_values - min(input_values)) / (max(input_values) - min(input_values))

    # Add variability: scale down by 5/6 and add random noise up to 1/6 of max value
    input_noisy = (6 - noise_scaling_factor) / 6 * input_normalized + (
                noise_scaling_factor / 6) * np.random.rand(len(input_normalized))

    # Scale to a maximum of 200 Hz (based on previous scaling)
    max_rate = 200 * Hz
    input_scaled = input_noisy * max_rate

    # Create TimedArray from scaled data
    input_timed = TimedArray(input_scaled, dt=record_dt)

    return input_timed


