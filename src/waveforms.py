import numpy as np
from typing import Tuple
def electrode_waveform(A: float, TD: float, PRF: float, BD: float, carrier_f: float, f_s: float, start_t: float = 0) -> Tuple[np.array, np.array]:
    """
    Generate a simple sine wave electrode waveform.

    Parameters:
    A (float)          : The peak amplitude of the waveform.
    TD (float)         : The total duration of the waveform in seconds.  
    PRF (float)        : The pulse repetition frequency in Hz.
    BD (float)         : The burst duration in seconds.
    carrier_f (float)  : The frequency of the sine wave in Hz.
    f_s (float)        : The number of samples per second.

    Returns:
    signal (np.array)  : Electrode waveform time series
    t (np.array)       : Corresponding time values.
    """
    PRP = 1 / PRF  # s, Pulse repetition period
    N = int(TD * f_s)  # Total number of samples
    t = np.linspace(start=start_t, stop=start_t + TD, num=N).reshape(-1, 1) # s
    t_local = t % PRP
    bursts = (t_local) < BD
    signal = A * np.sin(2 * np.pi * carrier_f * t_local)
    
    return signal, t

# TODO review and optimize
def multi_electrode_waveform(
    A, TD, PRF, BD, carrier_f, f_s, num_electrodes: int, start_t: float = 0
) -> Tuple[np.array, np.array]:
    """
    Generate electrode waveforms for multiple electrodes.
    
    Parameters can be either floats (same value for all electrodes) or arrays 
    (one value per electrode).
    
    Parameters:
    A              : Peak amplitude(s). Float or array of length num_electrodes.
    TD             : Total duration(s) in seconds. Float or array of length num_electrodes.
    PRF            : Pulse repetition frequency(ies) in Hz. Float or array of length num_electrodes.
    BD             : Burst duration(s) in seconds. Float or array of length num_electrodes.
    carrier_f      : Carrier frequency(ies) in Hz. Float or array of length num_electrodes.
    f_s            : Sampling frequency in Hz. Float or array of length num_electrodes.
    num_electrodes : Number of electrodes.
    start_t        : Start time in seconds.
    
    Returns:
    signals (np.array) : Array of shape (N, num_electrodes) with electrode waveforms.
    t (np.array)       : Time array of shape (N, 1).
    """
    # Convert all parameters to arrays
    params = {
        'A': A, 'TD': TD, 'PRF': PRF, 'BD': BD, 
        'carrier_f': carrier_f, 'f_s': f_s
    }
    
    for key, value in params.items():
        if isinstance(value, (int, float)):
            params[key] = np.full(num_electrodes, value)
        else:
            params[key] = np.array(value)
            if len(params[key]) != num_electrodes:
                raise ValueError(f"{key} array length must match num_electrodes")
    
    # Generate waveforms for each electrode
    signals = []
    t = None
    # Vectorize the operation
    PRP = 1 / params['PRF']  # Pulse repetition period for each electrode
    max_TD = np.max(params['TD'])
    max_fs = np.max(params['f_s'])
    N = int(max_TD * max_fs)  # Total number of samples
    
    t = np.linspace(start=start_t, stop=start_t + max_TD, num=N).reshape(-1, 1)
    
    # Broadcast parameters to (N, num_electrodes) shape
    t_local = (t % PRP.reshape(1, -1))  # (N, num_electrodes)
    bursts = t_local < params['BD'].reshape(1, -1)  # (N, num_electrodes)
    
    # Generate all signals at once
    signals = params['A'].reshape(1, -1) * np.sin(
        2 * np.pi * params['carrier_f'].reshape(1, -1) * t_local
    ) * bursts  # (N, num_electrodes)
    return signals, t