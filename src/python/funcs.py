import numpy as np
import matplotlib.pyplot as plt

# Import c++ module function
from ..cpp.build.Release import cpp_funcs

# Python version of photon_propagation
def photon_propagation(
    mu,              # (np.array)  - Array with attenuation coefficient
    thickness,       # (float)     - Thickness of material
    N                # (int)       - Number of photons to simulate
):
    ### Discretization of thickness
    x, dx = np.linspace(0, thickness, len(mu), retstep=True)
    
    ### Probability of scattering or absorption
    p =  mu * dx

    ### Photons per discretization step
    photons_cont = N
    
    ### Loop through discretization steps
    for i in range(len(x)):
        z = np.random.rand(photons_cont) # Array with random values [0, 1), len = number of entering photons
        photons_cont = np.sum(z > p[i])  # Number of photons not absorbed or scattered

    return photons_cont / N

def imaging(
    object_number, # (int)    - Object number
    energies,      # (array)  - Array with energies for stored data
    dimensions,    # (array)  - Array with x, y, z dimension in cm: [x, y, z]
    N_photons,     # (int)    - Number of photons per beam
    grid           # (list)   - List with axes-coordinates to plot results
):
    ### Array with filepaths
    filenames = [f'data/object{object_number}_{energy}keV.npy' for energy in energies]
    
    ### Figure
    fig = plt.figure()
    
    ### Enumerate files
    for energy_idx, filename in enumerate(filenames):
        ### Load data
        data = np.load(filename)
        
        ### Get shape of 3d matrix and store plane discretization
        shape = data.shape
        planes = [
            [shape[0], shape[1], [dimensions[0], dimensions[1]]],  # [N_x, N_y, [dimensions in cm]]
            [shape[0], shape[2], [dimensions[0], dimensions[2]]],  # [N_x, N_z, [dimensions in cm]]
            [shape[1], shape[2], [dimensions[1], dimensions[2]]]   # [N_y, N_z, [dimensions in cm]]
        ]
        
        ### Show energy text
        ax = plt.subplot(6, 3, grid[energy_idx][-1])
        ax.text(.5, .5, f'Photon-energy = {energies[energy_idx]}keV', ha='center', va='center', size=15)
        ax.axis('off')
        
        ### Enumerate planes
        for idx, N in enumerate(planes):
            ### Final datastore
            detector_data = np.empty((N[0], N[1]))
            
            ### Thickness of plane
            thickness = dimensions[2 - idx] 
            
            ### Loop through plane grid (x and y represents first and second axis of plane)
            for x in range(N[0]):
                for y in range(N[1]):
                    ### Get xy-column of 3d-matrix
                    column = [x, y]
                    column[2-idx:2-idx] = [(slice(None))]  # Gives for instance [x, y, :]
                    
                    ### Store detector intensity for coordinate
                    detector_data[x, y] = cpp_funcs.photon_propagation(
                        data[tuple(column)],
                        thickness,
                        N_photons,
                    )
            
            ### Get correct axis and show data
            ax = plt.subplot(6, 3, grid[energy_idx][idx])
            ax.imshow(detector_data)

            ax.grid(False)
            ax.set_xticks([])
            ax.set_yticks([])
            
            ax.set_xlabel(f'{N[2][1]}cm x {N[2][0]}cm')
    
    plt.tight_layout()
    plt.show()