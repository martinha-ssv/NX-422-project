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