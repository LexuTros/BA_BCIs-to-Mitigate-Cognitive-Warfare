#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from brian2 import *
import scipy
from scipy import signal
import ast
import plotting_Toellke


def window_rms(a, window_size):
    a2 = numpy.power(a, 2)
    window = ones(window_size) / float(window_size)
    return sqrt(convolve(a2, window, 'valid'))


def band_filter(N, unfiltered_signal, low, high):

    b, a = scipy.signal.butter(N, [low, high], btype='band')
    try:
        filtered_signal = scipy.signal.filtfilt(b, a, unfiltered_signal)

        return filtered_signal
    except:
        return []


def frequency_band_analysis(N, low, high, event, fs):

    try:
        y = band_filter(N, event, low, high)
        f, Pxx_spec = signal.periodogram(y, fs, 'flattop', scaling='spectrum')

        return f, Pxx_spec, y
    except:
        return [], [], []


def event_detection_and_analysis(sig, sigstr, fs):
    record_dt = 1 / fs
    start_plot_time = 50 * msecond
    start_ind = int(start_plot_time / record_dt)
    sig_rms = window_rms(sig[start_ind:] - mean(sig[start_ind:]), int(10 * ms / record_dt))
    sig_std = std(sig_rms)

    #detection des events
    all_begin = []
    all_end = []
    begin = 0
    peak = False

    peak_cond = 4.5 * sig_std
    boundaries_cond = 3 * sig_std

    tmax = 60 * second

    for ind in range(len(sig_rms)):
        t = ind * record_dt
        if t > tmax:
            break
        rms = sig_rms[ind]
        if rms > boundaries_cond and begin == 0:
            begin = ind
        if rms > peak_cond and peak == False:
            #elif rms>3*sig_std and peak==False:
            peak = True
        #elif rms<0.2*sig_std and peak:    
        elif rms < boundaries_cond and peak:
            all_begin.append(begin)
            all_end.append(ind)
            begin = 0
            end = 0
            peak = False
        elif rms < boundaries_cond and not peak:
            begin = 0
            end = 0
            peak = False

    all_duration = []
    all_spectrum = []
    all_spectrum_peak = []

    theta_spectrum = []
    gamma_spectrum = []
    ripple_spectrum = []

    events = []
    filtered_events = []
    sharp_wave_ripples = []
    sharp_wave_ripple_peaks = []
    sharp_wave_ripple_durations = []

    N = 2
    nyq = 0.5 * fs
    low = 30 / nyq
    high = 400 / nyq
    fs = fs / Hz
    test_ind = 0

    num_events = len(all_begin)

    # general analysis
    for i in range(num_events):
        # signal of event
        event = sig[all_begin[i] + start_ind:all_end[i] + start_ind]
        duration = len(event) * record_dt

        # Original/general analysis
        f, Pxx_spec, filtered_event = frequency_band_analysis(N, low, high, event, fs)
        if len(f) != 0 and len(Pxx_spec) != 0:
            events.append(event)
            filtered_events.append(filtered_event)
            all_duration.append(duration)
            all_spectrum.append(Pxx_spec)

            peak_frequency = f[argmax(Pxx_spec)]
            all_spectrum_peak.append(peak_frequency)
            if 100 <= peak_frequency <= 250:
                sharp_wave_ripples.append(event)
                sharp_wave_ripple_peaks.append(peak_frequency)
                sharp_wave_ripple_durations.append(duration)

            test_ind += 1

        # Band specific analysis
        # theta_spectrum.extend(frequency_band_analysis(N, 5/nyq, 10/nyq, event, fs)[1])
        # gamma_spectrum.extend(frequency_band_analysis(N, 30/nyq, 100/nyq, event, fs)[1])
        # ripple_spectrum.extend(frequency_band_analysis(N, 120/nyq, 200/nyq, event, fs)[1])


    band_spectra = [theta_spectrum, gamma_spectrum, ripple_spectrum]
    all_events = [events, filtered_events]
    all_swr_data = [sharp_wave_ripples, sharp_wave_ripple_peaks, sharp_wave_ripple_durations]
    non_swr_peaks = [x for x in all_spectrum_peak if x not in sharp_wave_ripple_peaks]

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
    # print(non_swr_peaks)

    return all_spectrum_peak, band_spectra, all_events, all_swr_data


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
