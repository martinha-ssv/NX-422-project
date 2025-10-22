import numpy as np

# CONSTANTS
PRF = 33 # Hz
PRP = 1 / PRF # s
burst_duration = 250e-6 # s
carrier_freqs = np.array([20e3, 22e3]) # Hz
carrier_amplitudes = np.array([1e-3, 1e-3]) # A

def gen_signals(freqs: np.ndarray, amps: np.ndarray, t: np.ndarray) -> np.ndarray:
    '''Generate sinusoidal signals for given frequencies and amplitudes over time t.
    -----
    Parameters:
    freqs : np.ndarray
        N x 1 array of N frequencies for the signals.
    amps : np.ndarray
        N x 1 array of N amplitudes for the signals.
    t : np.ndarray
        Array of time points at which to evaluate the signals.
    -------
    Returns:
    np.ndarray
        Array of N generated sinusoidal signals.
    '''

    signals = amps * np.sin(2 * np.pi * freqs * t)
    return signals

def gen_interference_signal(freqs: np.ndarray, amps: np.ndarray, t: np.ndarray) -> np.ndarray:
    '''Generate interference signals from given frequencies and amplitudes over time t.
    -----
    Parameters:
    freqs : np.ndarray
        N x 1 array of N frequencies for the signals.
    amps : np.ndarray
        N x 1 array of N amplitudes for the signals.
    -------
    Returns:
    np.ndarray
        Array of N generated interference signals.
    '''

    signals = gen_signals(freqs, amps, t)
    interf = np.sum(signals, axis=1)
    return interf
