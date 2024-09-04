#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from brian2 import *
import scipy
from scipy import signal
import ast


def window_rms(a, window_size):
    a2 = numpy.power(a, 2)
    window = ones(window_size) / float(window_size)
    return sqrt(convolve(a2, window, 'valid'))


def band_filter(unfiltered_signal, low, high, samp_freq,):
    order = 2
    nyq = 0.5 * samp_freq
    b, a = signal.butter(order, [low/nyq, high/nyq], btype='band')
    try:
        filtered_signal = signal.filtfilt(b, a, unfiltered_signal)

        return filtered_signal
    except:
        return []


def frequency_band_analysis(event, low, high, samp_freq):
    try:
        filtered_sig = band_filter(event, low, high, samp_freq)
        frequencies, power_spectrum = signal.periodogram(filtered_sig, samp_freq / Hz, 'flattop', scaling='spectrum')

        return frequencies, power_spectrum, filtered_sig
    except:
        return [], [], []


def sharp_wave_detection(sig, boundary_condition, peak_condition, record_dt):
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


# print('Analysis of the simulation ' + sigstr + ' :')
# print("Number of studied events : " + str(test_ind))
#
# mean_peak = mean(all_spectrum_peak)
# print('Mean peak frequency of the events = ' + str(mean_peak) + ' Hz')
# std_peak = std(all_spectrum_peak)
# print('Standard deviation of the peak frequency of the events = ' + str(std_peak) + ' Hz')
# min_peak = min(all_spectrum_peak)
# print('Minimum peak frequency of the events = ' + str(min_peak) + ' Hz')
# max_peak = max(all_spectrum_peak)
# print('Maximum peak frequency of the events = ' + str(max_peak) + ' Hz')
# print(' ')
#
# mean_dur = mean(all_duration)
# print('Mean duration of the events = ' + str(mean_dur * 1000) + ' ms')
# min_dur = min(all_duration)
# print('Minimum duration of the events = ' + str(min_dur))
# max_dur = max(all_duration)
# print('Maximum duration of the events = ' + str(max_dur))
# print(' ')
#
# print("Sharp Wave Ripples")
# print("Number : " + str(len(sharp_wave_ripples)))
# print('Mean peak frequency = ' + str(mean(sharp_wave_ripple_peaks)) + ' Hz')
# print('Mean duration = ' + str(mean(sharp_wave_ripple_durations) * 1000) + ' ms')
# print(" ")
#


def event_identification_analysis(sig, sigstr, fs):
    record_dt = 1 / fs
    start_plot_time = 50 * msecond
    start_ind = int(start_plot_time / record_dt)

    N = 2
    nyq = 0.5 * fs

    low_signal = band_filter(N, sig, 10/nyq, 80/nyq)
    mid_signal = band_filter(N, sig, 120/nyq, 200/nyq)
    high_signal = band_filter(N, sig, 200/nyq, 500/nyq)

    low_sig_rms = window_rms(low_signal[start_ind:] - mean(low_signal[start_ind:]), int(10 * ms / record_dt))
    mid_sig_rms = window_rms(mid_signal[start_ind:] - mean(mid_signal[start_ind:]), int(10 * ms / record_dt))
    high_sig_rms = window_rms(high_signal[start_ind:] - mean(high_signal[start_ind:]), int(10 * ms / record_dt))

    low_sig_std = std(low_sig_rms)
    mid_sig_std = std(mid_sig_rms)
    high_sig_std = std(high_sig_rms)

    #detection des events
    all_begin = []
    all_end = []
    interictal_spikes = []
    sharp_wave_ripples = []
    fast_ripples = []

    begin = 0
    peaks = [False, False, False]

    low_mean_cond = mean(low_sig_rms)
    mid_mean_cond = mean(mid_sig_rms)
    high_mean_cond = mean(high_sig_rms)

    low_peak_cond = 4 * low_sig_std
    mid_peak_cond = 4 * mid_sig_std
    high_peak_cond = 4 * high_sig_std


    for ind in range(len(low_sig_rms)):

        low_rms = low_sig_rms[ind]
        mid_rms = mid_sig_rms[ind]
        high_rms = high_sig_rms[ind]

        if low_rms > low_mean_cond or mid_rms > mid_mean_cond or high_rms > high_mean_cond:
            if begin == 0:
                begin = ind
            if low_rms > low_mean_cond and low_rms > low_peak_cond and not peaks[0]:
                peaks[0] = True
            if mid_rms > mid_mean_cond and mid_rms > mid_peak_cond and not peaks[1]:
                peaks[1] = True
            if high_rms > high_mean_cond and high_rms > high_peak_cond and not peaks[2]:
                peaks[2] = True

        elif True in peaks:
            all_begin.append(begin)
            all_end.append(ind)

            if peaks[2]:
                fast_ripples.append((begin, ind))
            elif peaks[1]:
                sharp_wave_ripples.append((begin, ind))
            else:
                interictal_spikes.append((begin, ind))

            begin = 0
            peaks = [False, False, False]

        else:
            begin = 0


    all_duration = []
    for i in range(len(all_begin)):
        # signal of event
        event = sig[all_begin[i] + start_ind:all_end[i] + start_ind]
        duration = len(event) * record_dt

        all_duration.append(duration)

    swr_signals = []
    swr_duration = []
    for i in range(len(sharp_wave_ripples)):
        sharp_wave_ripple = sig[sharp_wave_ripples[i][0] + start_ind:sharp_wave_ripples[i][1] + start_ind]
        duration = len(sharp_wave_ripple) * record_dt

        swr_signals.append(sharp_wave_ripple)
        swr_duration.append(duration)


    print(f'Event types of {sigstr} Simulation:\n')

    print(f'Number of all events: {len(all_begin)}')
    print(f'Mean duration of events: {mean(all_duration) * 1000} ms\n')

    print(f'Nuber of Sharp Wave Ripple events: {len(sharp_wave_ripples)}')
    print(f'Mean duration Sharp Wave Ripples: {mean(swr_duration) * 1000} ms\n')

    print(f'Nuber of Interictal spike events: {len(interictal_spikes)}')
    print(f'Nuber of Fast Ripple events: {len(fast_ripples)}')

    return swr_signals
