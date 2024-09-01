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


def frequency_band_analysis(N, low, high, event, fs):

    b, a = scipy.signal.butter(N, [low, high], btype='band')
    try:
        y = scipy.signal.filtfilt(b, a, event)
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

    peak_cond = 4 * sig_std
    boundaries_cond = 2 * sig_std

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

    N = 3
    nyq = 0.5 * fs
    low = 30 / nyq
    high = 300 / nyq
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
            all_spectrum_peak.append(f[argmax(Pxx_spec)])

        # Band specific analysis
        theta_spectrum.extend(frequency_band_analysis(N, 5/nyq, 10/nyq, event, fs)[1])
        gamma_spectrum.extend(frequency_band_analysis(N, 30/nyq, 100/nyq, event, fs)[1])
        ripple_spectrum.extend(frequency_band_analysis(N, 120/nyq, 200/nyq, event, fs)[1])

        test_ind += 1

    band_spectra = [theta_spectrum, gamma_spectrum, ripple_spectrum]
    all_events = [events, filtered_events]

    # print('Analysis of the simulation ' + sigstr + ' :')
    # print("Number of studied events : " + str(test_ind))
    #
    # mean_peak = mean(all_spectrum_peak)
    # print('Mean peak frequency of the events=' + str(mean_peak) + ' Hz')
    # std_peak = std(all_spectrum_peak)
    # print('Standard deviation of the peak frequency of the events=' + str(std_peak) + ' Hz')
    # min_peak = min(all_spectrum_peak)
    # print('Minimum peak frequency of the events=' + str(min_peak) + ' Hz')
    # max_peak = max(all_spectrum_peak)
    # print('Maximum peak frequency of the events=' + str(max_peak) + ' Hz')
    # print(' ')
    #
    # mean_dur = mean(all_duration)
    # print('Mean duration of the events=' + str(mean_dur * 1000) + ' ms')
    # std_dur = std(all_duration)
    # print('Standard deviation of the duration  of the events=' + str(std_dur * 1000) + ' ms')
    # min_dur = min(all_duration)
    # print('Minimum duration of the events=' + str(min_dur))
    # max_dur = max(all_duration)
    # print('Maximum duration of the events=' + str(max_dur))

    return all_spectrum_peak, band_spectra, all_events
