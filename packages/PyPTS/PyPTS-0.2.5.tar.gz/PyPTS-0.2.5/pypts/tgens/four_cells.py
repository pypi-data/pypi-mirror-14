from pypts.tissue import Tissue
import numpy as np
import scipy as sp

def four_cells():
    """
    This function returns a small 4-cell tissue which is frequently used in
    VirtualLeaf2 simulations as a starting point. The coordinates and cells are
    hard coded.
    """
    # First I need an empty tissue to work on:
    t = Tissue()

    t.num_nodes = 22
    t.nodes_id = np.arange(t.num_nodes)
    t.nodes_xy = np.array([
        [ 22.9634E0, -2.37264E0],
        [ 14.6882E0,  17.9118E0],
        [ 1.57936E0,  25.1246E0],
        [-9.0893E0,   22.8165E0],
        [-19.7055E0,  16.962E0 ],
        [-22.6839E0,  5.00143E0],
        [-14.7271E0, -15.2131E0],
        [-6.78413E0, -23.4002E0],
        [ 3.60766E0, -25.1355E0],
        [ 21.3032E0, -13.6899E0],
        [ 17.4704E0,  7.41573E0],
        [-17.5799E0, -5.20265E0],
        [ 9.86837E0,  4.69636E0],
        [-9.28449E0, -3.92969E0],
        [12.5597E0,  -20.5161E0],
        [-1.62187E0, -3.10623E0],
        [ 7.55765E0, -14.4922E0],
        [ 2.97596E0, -8.80653E0],
        [ 1.95125E0,  3.2756E0 ],
        [-6.54614E0,  15.4702E0],
        [-2.72983E0,  8.96705E0],
        [ 9.33552E0,  23.0046E0]
    ])

    t.num_cells = 4
    t.cells_id = np.arange(t.num_cells)
    t.cells_num_nodes = np.array([9, 9, 9, 9])
    t.cells_nodes = [
        np.array([13, 11,  6,  7,  8, 14, 16, 17, 15]),
        np.array([12, 10,  1, 21,  2,  3, 19, 20, 18]),
        np.array([9,  0,  10, 12, 18, 15, 17, 16, 14]),
        np.array([4,  5,  11, 13, 15, 18, 20, 19,  3])
    ]
    t.cells_num_walls = np.array([3, 3, 4, 4])
    t.cells_walls = [
        np.array([6, 0, 1]),
        np.array([3, 4, 5]),
        np.array([1, 2, 8, 4]),
        np.array([5, 6, 7, 8])
    ]

    t.num_walls = 9
    t.walls_id = np.arange(t.num_walls)
    t.walls_cells = np.array([
        [0,-1],
        [0, 2],
        [2,-1],
        [1,-1],
        [2, 1],
        [1, 3],
        [0, 3],
        [3,-1],
        [2, 3]
    ])
    t.walls_nodes = np.array([
        [11,14],
        [14,15],
        [14,10],
        [10, 3],
        [10,18],
        [ 3,18],
        [15,11],
        [ 3,11],
        [18,15],
    ])

    # TODO: at some point I might decide to add the start values for IAA & PIN
    # as well. Maybe even the PINs on the walls. For now I'm doing geometry.

    t.prepare_for_use()
    return t

