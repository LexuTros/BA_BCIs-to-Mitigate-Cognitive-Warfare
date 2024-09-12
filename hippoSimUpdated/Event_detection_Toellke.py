#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from brian2 import *
import scipy
from scipy import signal
import ast


def window_rms(a, window_size):
    """
        Computes the root mean square (RMS) of a signal over a specified window size.

        Parameters:
            a (array): The input array of floats for which the RMS is to be calculated.
            window_size (int): The size of the moving window to compute the RMS.

        Returns:
            array: An array of floats representing the RMS values computed over the specified window.
    """
    a2 = numpy.power(a, 2)
    window = ones(window_size) / float(window_size)
    return sqrt(convolve(a2, window, 'valid'))


def band_filter(unfiltered_signal, low, high, samp_freq,):
    """
        Applies a bandpass filter to an unfiltered signal using a Butterworth filter.

        Parameters:
            unfiltered_signal (array-like): The input signal to be filtered.
            low (float): The lower cutoff frequency of the bandpass filter.
            high (float): The upper cutoff frequency of the bandpass filter.
            samp_freq (float): The sampling frequency of the input signal.

        Returns:
            array: The filtered signal as an array of floats, or an empty list if filtering fails.
    """
    order = 2
    nyq = 0.5 * samp_freq
    b, a = signal.butter(order, [low/nyq, high/nyq], btype='band')
    try:
        filtered_signal = signal.filtfilt(b, a, unfiltered_signal)

        return filtered_signal
    except:
        return []


def frequency_band_analysis(event, low, high, samp_freq):
    """
        Analyzes the frequency band of a given event by applying a bandpass filter and computing the power spectrum.

        Parameters:
            event (array-like): The input signal or event data to analyze.
            low (float): The lower cutoff frequency of the bandpass filter.
            high (float): The upper cutoff frequency of the bandpass filter.
            samp_freq (float): The sampling frequency of the input signal.

        Returns:
            tuple: A tuple containing:
                - array: The frequencies corresponding to the power spectrum.
                - array: The power spectrum of the filtered signal.
                - array: The filtered signal after applying the bandpass filter, or empty lists if analysis fails.
    """
    try:
        filtered_sig = band_filter(event, low, high, samp_freq)
        frequencies, power_spectrum = signal.periodogram(filtered_sig, samp_freq / Hz, 'flattop', scaling='spectrum')

        return frequencies, power_spectrum, filtered_sig
    except:
        return [], [], []


def sharp_wave_detection(sig, boundary_condition, peak_condition, record_dt):
    """
        Detects sharp waves in a signal based on specified boundary and peak conditions.

        Parameters:
            sig (array-like): The input signal from which sharp waves are to be detected.
            boundary_condition (float): The multiplier for standard deviation to define the boundary for detection.
            peak_condition (float): The multiplier for standard deviation to define the peak condition for detection.
            record_dt (float): The time step of the recorded signal, used for RMS calculation.

        Returns:
            list: A list of arrays, each containing the segments of the signal that correspond to detected sharp waves.
    """
    # calculation of root-mean-square
    start_plot_time = 50 * msecond
    start_ind = int(start_plot_time / record_dt)
    sig_rms = window_rms(sig[start_ind:] - mean(sig[start_ind:]), int(10 * ms / record_dt))
    sig_std = std(sig_rms)

    boundary_value = boundary_condition * sig_std
    peak_value = peak_condition * sig_std

    # detection of sharp waves
    begin = 0
    peak = False
    all_sharp_waves = []

    for ind in range(len(sig_rms)):
        rms = sig_rms[ind]
        if rms > boundary_value and begin == 0:
            # event start
            begin = ind
        if rms > peak_value and not peak:
            # event fulfills peak condition
            peak = True
        elif rms < boundary_value and peak:
            # sharp wave detected
            sharp_wave_signal = sig[begin + start_ind:ind + start_ind]
            all_sharp_waves.append(sharp_wave_signal)
            begin = 0
            peak = False
        elif rms < boundary_value and not peak:
            # event without sufficient peak
            begin = 0
            peak = False

    return all_sharp_waves


def event_detection(sig):
    """
        Detects events in a signal and performs frequency analysis on the detected events.

        Parameters:
            sig (array-like): The input signal from which events are to be detected.

        Returns:
            tuple: A tuple containing:
                - list: A list of detected event signals.
                - list: A list of filtered events.
                - list: A list of peak frequencies corresponding to each event.
                - list: A list of durations for each detected event.
                - list: A list of sharp wave ripples identified in the signal.
                - list: A list of peak frequencies of sharp wave ripples.
                - list: A list of durations for each sharp wave ripple.
                - list: A list of power spectra for theta band (5-10 Hz).
                - list: A list of power spectra for gamma band (30-100 Hz).
                - list: A list of power spectra for ripple band (100-250 Hz).
    """
    # model specific signal properties
    sample_frequency = 1024 * Hz
    record_dt = 1 / sample_frequency

    event_signals = sharp_wave_detection(sig, 3, 4.5, record_dt)

    # frequency analysis
    filtered_events = []
    all_spectrum_peaks = []
    all_durations = []

    sharp_wave_ripples = []
    sharp_wave_ripple_peaks = []
    sharp_wave_ripple_durations = []

    theta_spectrum = []
    gamma_spectrum = []
    ripple_spectrum = []

    for event in event_signals:
        # filter in broad frequency range
        frequencies, power_spectrum, filtered_event = frequency_band_analysis(event, 30, 400, sample_frequency)
        if len(frequencies) != 0 and len(power_spectrum) != 0:
            # collect general event data
            filtered_events.append(filtered_event)
            duration = len(event) * record_dt * 1000
            all_durations.append(duration)
            peak_frequency = frequencies[argmax(power_spectrum)]
            all_spectrum_peaks.append(peak_frequency)

            # identify sharp wave ripples
            if 100 <= peak_frequency <= 250:
                sharp_wave_ripples.append(event)
                sharp_wave_ripple_peaks.append(peak_frequency)
                sharp_wave_ripple_durations.append(duration)

        # collect power of frequency bands
        theta_spectrum.extend(frequency_band_analysis(event, 5, 10, sample_frequency)[1])
        gamma_spectrum.extend(frequency_band_analysis(event, 30, 100, sample_frequency)[1])
        ripple_spectrum.extend(frequency_band_analysis(event, 100, 250, sample_frequency)[1])

    # structure result data
    all_event_data = [event_signals, filtered_events, all_spectrum_peaks, all_durations]
    swr_data = [sharp_wave_ripples, sharp_wave_ripple_peaks, sharp_wave_ripple_durations]
    band_spectra = [theta_spectrum, gamma_spectrum, ripple_spectrum]

    return all_event_data, swr_data, band_spectra



# Alternative approach - less accurate:

# def event_identification_analysis(sig, sigstr, fs):
#     record_dt = 1 / fs
#     start_plot_time = 50 * msecond
#     start_ind = int(start_plot_time / record_dt)
#
#     N = 2
#     nyq = 0.5 * fs
#
#     low_signal = band_filter(N, sig, 10/nyq, 80/nyq)
#     mid_signal = band_filter(N, sig, 120/nyq, 200/nyq)
#     high_signal = band_filter(N, sig, 200/nyq, 500/nyq)
#
#     low_sig_rms = window_rms(low_signal[start_ind:] - mean(low_signal[start_ind:]), int(10 * ms / record_dt))
#     mid_sig_rms = window_rms(mid_signal[start_ind:] - mean(mid_signal[start_ind:]), int(10 * ms / record_dt))
#     high_sig_rms = window_rms(high_signal[start_ind:] - mean(high_signal[start_ind:]), int(10 * ms / record_dt))
#
#     low_sig_std = std(low_sig_rms)
#     mid_sig_std = std(mid_sig_rms)
#     high_sig_std = std(high_sig_rms)
#
#     #detection des events
#     all_begin = []
#     all_end = []
#     interictal_spikes = []
#     sharp_wave_ripples = []
#     fast_ripples = []
#
#     begin = 0
#     peaks = [False, False, False]
#
#     low_mean_cond = mean(low_sig_rms)
#     mid_mean_cond = mean(mid_sig_rms)
#     high_mean_cond = mean(high_sig_rms)
#
#     low_peak_cond = 4 * low_sig_std
#     mid_peak_cond = 4 * mid_sig_std
#     high_peak_cond = 4 * high_sig_std
#
#
#     for ind in range(len(low_sig_rms)):
#
#         low_rms = low_sig_rms[ind]
#         mid_rms = mid_sig_rms[ind]
#         high_rms = high_sig_rms[ind]
#
#         if low_rms > low_mean_cond or mid_rms > mid_mean_cond or high_rms > high_mean_cond:
#             if begin == 0:
#                 begin = ind
#             if low_rms > low_mean_cond and low_rms > low_peak_cond and not peaks[0]:
#                 peaks[0] = True
#             if mid_rms > mid_mean_cond and mid_rms > mid_peak_cond and not peaks[1]:
#                 peaks[1] = True
#             if high_rms > high_mean_cond and high_rms > high_peak_cond and not peaks[2]:
#                 peaks[2] = True
#
#         elif True in peaks:
#             all_begin.append(begin)
#             all_end.append(ind)
#
#             if peaks[2]:
#                 fast_ripples.append((begin, ind))
#             elif peaks[1]:
#                 sharp_wave_ripples.append((begin, ind))
#             else:
#                 interictal_spikes.append((begin, ind))
#
#             begin = 0
#             peaks = [False, False, False]
#
#         else:
#             begin = 0
#
#
#     all_duration = []
#     for i in range(len(all_begin)):
#         # signal of event
#         event = sig[all_begin[i] + start_ind:all_end[i] + start_ind]
#         duration = len(event) * record_dt
#
#         all_duration.append(duration)
#
#     swr_signals = []
#     swr_duration = []
#     for i in range(len(sharp_wave_ripples)):
#         sharp_wave_ripple = sig[sharp_wave_ripples[i][0] + start_ind:sharp_wave_ripples[i][1] + start_ind]
#         duration = len(sharp_wave_ripple) * record_dt
#
#         swr_signals.append(sharp_wave_ripple)
#         swr_duration.append(duration)
#
#
#     print(f'Event types of {sigstr} Simulation:\n')
#
#     print(f'Number of all events: {len(all_begin)}')
#     print(f'Mean duration of events: {mean(all_duration) * 1000} ms\n')
#
#     print(f'Nuber of Sharp Wave Ripple events: {len(sharp_wave_ripples)}')
#     print(f'Mean duration Sharp Wave Ripples: {mean(swr_duration) * 1000} ms\n')
#
#     print(f'Nuber of Interictal spike events: {len(interictal_spikes)}')
#     print(f'Nuber of Fast Ripple events: {len(fast_ripples)}')
#
#     return swr_signals
