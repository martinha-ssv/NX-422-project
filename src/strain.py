import numpy as np
def strain_layer_x(E,t,z,z_np):
    """
    Calculate the strain in a layer due to bending about the x-axis.

    Parameters
    ----------
    E : array_like
        Young's modulus of each layer material.
    t : array_like
        Thickness of each layer.
    z : np.ndarray
        Distance(s) from zero (base) to the point(s) where strain is calculated.

    Returns
    -------
    np.ndarray
        Strain at the specified distance(s) from the neutral axis.
    """
    # Calculate strain using the formula: strain = z / (t/2)
    
    y_i=abs(z_np - z)
    strains = y_i / (300)
    
    return strains

z_1=np.array([0,100,100.005,100.035,200])
z=np.array([50,100.0025,100.0225,  150])
E=np.array([1e6,140e9,44e9,1e6])
t=np.array([100,0.005,0.035,100])
z_np=np.sum((E*z*t))/np.sum(E*t)
strain_layer_x(E,t,z,z_np)
print(strain_layer_x(E,t,z,z_np)*100)
