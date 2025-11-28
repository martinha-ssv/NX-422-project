# THEORY
# In this script, we calculate the SAR of our device using the formula:
# SAR = P_absorbed / mass
# We will calculate the absorbed power from the device's power output and the mass from the volume and density of a heated volume.
# 
# P_absorbed = RI**2 across our system components + wireless power transfer losses
# mass = volume * density
# volume = mu**3 * (4/3) * pi for a spherical heated region, where mu is the thermal diffusion length
# mu = sqrt(D/(pi*f)), where D is the thermal diffusivity and f is the modulation frequency

import numpy as np

SAR_limit = 0.5  # W/kg, Specific Absorption Rate limit for human exposure

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
    '''Calculate the volume of the heated region assuming a spherical shape.
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

def power_absorbed(R_s: float, A_track: float, I: float, efficiency: float) -> float:
    '''Calculate the absorbed power in the system. Simplified model, where the power loss is assumed to happen only in the tracks through resistive heating.
    -----
    Parameters:
    R_s : float
        Resistance in ohms (Ω).
    A_track : float
        Track area in square meters (m^2).
    I   : float
        Current in amperes (A).
    efficiency : float
        Efficiency of wireless power transfer (0 < efficiency <= 1).
    -------
    Returns:
    float
        The absorbed power in watts (W).
    '''

    P_loss = R_s * A_track * I**2  # Power loss due to resistance
    P_absorbed = P_loss / efficiency  # Total absorbed power considering efficiency
    return P_absorbed

def sar(power_absorbed: float, volume: float, density: float) -> float:
    '''Calculate the Specific Absorption Rate (SAR).
    -----
    Parameters:
    power_absorbed : float
        The absorbed power in watts (W).
    volume : float
        The volume of the heated region in cubic meters (m^3).
    density : float
        The density of the tissue in kilograms per cubic meter (kg/m^3).
    -------
    Returns:
    float
        The calculated SAR in watts per kilogram (W/kg).
    '''

    mass = volume * density  # mass in kg
    sar = power_absorbed / mass  # SAR in W/kg
    return sar

def check_sar_limit(sar_value: float) -> bool:
    '''Check if the calculated SAR is within the safety limit.
    -----
    Parameters:
    sar_value : float
        The calculated SAR in watts per kilogram (W/kg).
    -------
    Returns:
    bool
        True if SAR is within the limit, False otherwise.
    '''

    return sar_value <= SAR_limit

