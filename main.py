from src.python.funcs import imaging

from IPython.display import set_matplotlib_formats
set_matplotlib_formats('svg')

imaging(
    1,                  # Object number
    [20, 50, 100],      # Energies
    [6.5, 44.6, 44.6],  # Thickness dimensions
    1000,               # Number of photons
    [                   # Grid coordinates for plotting
        [2,  5,  (3,6),   (1,4)],
        [8,  11, (9,12),  (7,10)],
        [14, 17, (15,18), (13,16)]
    ]
)