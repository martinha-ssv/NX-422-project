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

import matplotlib.pyplot as plt



SAR_LIMIT = 0.5  # W/kg, Specific Absorption Rate limit for human exposure # TODO look up value (currently placeholder)



# Device Design Parameters

R_s_list = [5.0, 10.0]  # Ohms, resistance of the system (placeholder value)

R_track = [R * (29/0.2) for R in R_s_list]  # Ohms, resistance of the tracks (length/resistivity) (placeholder value)







# Device Properties

PDMS_thermal_conductivity = 0.16  # W/(m·K), thermal conductivity of PDMS (Polymer Data Handbook, Oxford University Press, https://ceimusb.wordpress.com/wp-content/uploads/2015/04/mark-polymer-data-handbook.pdf#page=514.00)





# Waveform Operation Parameters

A = 2.0/6  # Amperes, current through the system (placeholder value)

PRF = 33 # Hz, pulse repetition frequency

BD = 250e-6  # seconds, burst duration

f_s = 1e3 # Hz, sampling frequency (for waveform generation)

n_pulses = 1# number of pulses

TD = n_pulses / PRF  # seconds, total duration of the waveform



# Tissue Properties

D_values = {

    "Extracel": 1.4848e-7,

    "Nerve": 1.26e-7,

    "Skin": 9.8389e-8,

    "Connective": 1.6e-7

} # m^2/s, thermal diffusivity of tissue (placeholder value)

c_values = {

    "Extracel": 3997.0,

    "Nerve": 3613.0,

    "Skin": 3391.0,

    "Connective": 2372.0

}  

density_values = {

    "Extracel": 1011.0,

    "Nerve": 1075.0,  

    "Skin": 1109.0,

    "Connective": 1027.0

}  # kg/m^3, density of tissue (placeholder value)



D_surround = np.mean([D_values["Extracel"], D_values["Skin"], D_values["Connective"]])

c_surround = np.mean([c_values["Extracel"], c_values["Skin"], c_values["Connective"]])

density_surround = np.mean([density_values["Extracel"], density_values["Skin"], density_values["Connective"]])



carrier_pairs = [

    (2.0, 20.0),

    (20000.0, 22000.0),

    (222222.0, 2.0)

] #Hz, carrier frequency pairs (f_carrier_1, f_carrier_2)





t = np.arange(0.0, TD, 1.0/f_s)

dt = 1.0 / f_s





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



    #mu = np.sqrt(D / (np.pi * f))

    #print(f"Thermal diffusion length for f={f} Hz: {mu*1e3:.6f} mm")

    return 16e-3  # Placeholder value for mu in meters (m)



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

    return 1500e-9



def energy_dissipated(R_t: float, I: np.array) -> float:

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

   

    I_rms = np.max(I)/np.sqrt(2)

    P_avg = R_t * I_rms**2

    E = P_avg * BD

    print(f"Energy dissipated for R={R_t} Ohms: {E:.09f} J")

    return E

  # Total absorbed power in W~



 

def tissue_heating(c: float, E: float, mass: float) -> float:

    '''Calculate the temperature rise in tissue due to absorbed energy.

    -----

    Parameters:

    c : float

        Specific heat capacity of tissue in J/(kg·K).

    E : float

        Absorbed energy in joules (J).

    mass : float

        Mass of the heated tissue in kilograms (kg).

    -------

    Returns:

    float

        The temperature rise in Kelvin (K).

    '''



    delta_T = E / (c * mass)

    return delta_T



results = []



delta_Ts = []

for i, pair in enumerate(carrier_pairs):

    f1,f2 = pair

    f_mod = abs(f1 - f2) if abs(f1 - f2) != 0 else f1

    I_1= electrode_waveform(A, TD, PRF, BD, f1, f_s)[0]
    print(I_1.mean())


    I_2= electrode_waveform(A, TD, PRF, BD, f2, f_s)[0]





    #for R in R_track:

    R = R_track[1]

    E_1 = energy_dissipated(R, I_1)

    E_2 = energy_dissipated(R, I_2)

    E1_total = E_1 * 3.0

    E2_total = E_2 * 3.0

    E_total= E1_total + E2_total

    print(f"Total Energy Dissipated for f1={f1} Hz and f2={f2} Hz: {E_total:.09f} J")





    mu = thermal_diffusion_length(D_values["Extracel"], f_mod)

    V = heated_volume(mu)

    mass = V * density_values["Extracel"]

    print(f"Heated Volume: {V*1e9:.6f} mm^3, Mass: {mass*1e3:.6f} g")

    delta_T = tissue_heating(c_values["Extracel"], E_total, mass)

    print(f"Modulation Frequency: {f_mod} Hz, Resistance: {R} Ohms, \nTemperature Rise in Nerve Tissue: {delta_T:.4f} K")



    delta_Ts.append(delta_T)



#plot reuslts

plt.figure(figsize=(7,5))



# for tissue_label, color, marker in [

#     ("Nerve", "tab:blue", "o"),

#     ("Surrounding", "tab:orange", "^"),

# ]:

#     x = [r["f_mod"] for r in results if r["tissue"] == tissue_label]

#     y = [r["delta_T"] for r in results if r["tissue"] == tissue_label]



#     plt.scatter(x, y, label=tissue_label, color=color, marker=marker)



plt.scatter(x=[(f"{pair[0]} Hz & {pair[1]} Hz") for pair in carrier_pairs],

            y=delta_Ts,

            color="tab:blue", marker="o")

plt.axhline(275.15, linestyle="--", color="red", label="2 °C limit")

plt.xlabel("Modulation Frequency (Hz)")

plt.ylabel("Temperature Rise (K)")

plt.title("Temperature Rise vs Modulation Frequency")

plt.legend()

plt.xscale("log")  

plt.show()