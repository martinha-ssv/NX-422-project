# THEORY
# In this script, we calculate the SAR of our device using the formula:
# SAR = P_absorbed / mass
# We will calculate the absorbed power from the device's power output and the mass from the volume and density of a heated volume.
# 
# P_absorbed = RI**2 across our system components + wireless power transfer losses
# mass = volume * density
# volume = mu**3 * (4/3) * pi for a spherical heated region, where mu is the thermal diffusion length
# mu = sqrt(D/(pi*f)), where D is the thermal diffusivity and f is the modulation frequency

# -------------------------------- #
# 0. Imports and constants         #
# -------------------------------- #
import numpy as np
from waveforms import electrode_waveform

SAR_LIMIT = 0.5  # W/kg, Specific Absorption Rate limit for human exposure # TODO look up value (currently placeholder)

# Device Design Parameters
R_s = 0.1  # Ohms, resistance of the system (placeholder value)
A_track = 1e-4  # m^2, cross-sectional area of the track (placeholder value)

# Device Properties
PDMS_thermal_conductivity = 0.16  # W/(m·K), thermal conductivity of PDMS (Polymer Data Handbook, Oxford University Press, https://ceimusb.wordpress.com/wp-content/uploads/2015/04/mark-polymer-data-handbook.pdf#page=514.00)


# Waveform Operation Parameters
A = 2.0  # Amperes, current through the system (placeholder value)
carrier_f = 22e3  # Hz, modulation frequency
PRF = 33 # Hz, pulse repetition frequency
BD = 250e-6  # seconds, burst duration
f_s = 1e3 # Hz, sampling frequency (for waveform generation)
n_pulses = 33 # number of pulses
TD = n_pulses / PRF  # seconds, total duration of the waveform

# Tissue Properties
D = 1.4e-7  # m^2/s, thermal diffusivity of tissue (placeholder value)
density = 1000.0  # kg/m^3, density of tissue (placeholder value)



# -------------------------------- #
# 1. Functions                     #
# -------------------------------- #
def thermal_diffusion_length(D: float, f: float) -> float:
    '''Calculate the thermal diffusion length.
    -----
    Parameters:
    D : float
        Thermal diffusivity in m^2/s.
    f : float
        Modulation frequency in Hz.
    -------
    Returns:
    float
        The thermal diffusion length in meters (m).
    '''

    mu = np.sqrt(D / (np.pi * f))
    return mu

def heated_volume(mu: float) -> float:
    '''Calculate the volume of the heated region assuming a spherical shape with radius mu (thermal diffusion length).
    -----
    Parameters:
    mu : float
        Thermal diffusion length in meters (m).
    -------
    Returns:
    float
        The volume of the heated region in cubic meters (m^3).
    '''

    volume = (4/3) * np.pi * mu**3
    return volume

def energy_dissipated(R_s: float, A_track: float, I: np.array) -> float:
    '''Calculate the absorbed power in the system. Simplified model, where the power loss is assumed to happen only in the tracks through resistive heating.
    -----
    Parameters:
    R_s : float
        Resistance in ohms (Ω).
    A_track : float
        Track area in square meters (m^2).
    I   : np.array
        Current in amperes (A).
    -------
    Returns:
    float
        The absorbed power in watts (W).
    '''

    P_loss = R_s * A_track * I**2  # Power loss due to resistance

    return np.sum(P_loss)  # Total absorbed power in W

# -------------------------------- #
# 2. Main calculation              #
# -------------------------------- #
I = electrode_waveform(A, TD, PRF, BD, carrier_f, f_s)[0]  # Get current waveform
E = energy_dissipated(R_s, A_track, I)  # Calculate absorbed power
mu = thermal_diffusion_length(D, carrier_f)  # Calculate thermal diffusion length
V = heated_volume(mu)  # Calculate heated volume
mass = V * density  # Calculate mass of heated tissue

