from pypts.tissue import Tissue
import numpy as np
import scipy as sp

def squares(num_rows, num_cols, wall_length=1.0):
    """
    This function returns a square cell tissue, given the number of cell rows
    and cell columns.
    For example, the following tissue has 4 cell rows and 5 cell columns.
    (Notice the origin of the coordinate system in the lower left corner)
    
    .--.--.--.--.--.    \
    |  |  |  |  |  |    |
    .--.--.--.--.--.    |
    |  |  |  |  |  |    |
    .--.--.--.--.--.    |- #rows
    |  |  |  |  |  |    |
    .--.--.--.--.--.    |
    |  |  |  |  |  |    |
    0--.--.--.--.--.    /
    
    \______________/
           |
         #cols
    
    The total number of cells is: #rows * #cols                   (example: 20)
    The total number of nodes is: (#rows + 1) * (#cols + 1)       (example: 30)
    """
    # First I need an empty tissue to work on:
    t = Tissue()

    t.num_cells = num_rows * num_cols
    t.num_nodes = (1 + num_rows) * (1 + num_cols)
    num_nodes_per_cell = 4

    print ('Generating a rectangular tissue of {0} square cells').format(t.num_cells)

    # IDs of nodes are just num_nodes consectutive integers
    t.nodes_id = np.arange(t.num_nodes)
    # Node coordinates
    t.nodes_xy = np.empty((t.num_nodes, 2), dtype='=f8')
    # Create node_xy coordinates for num_nodes nodes (ordered from lower left to
    # upper right, row-wise)
    nodes_x = np.empty((num_rows + 1, num_cols + 1), dtype='=f8')
    nodes_y = np.empty_like(nodes_x)
    nodes_x[:] = wall_length * np.arange(num_cols + 1)
    nodes_y.T[:] = wall_length * np.arange(num_rows + 1)
    t.nodes_xy[:, 0] = np.reshape(nodes_x, t.num_nodes)
    t.nodes_xy[:, 1] = np.reshape(nodes_y, t.num_nodes)

    # Reshape these to make looking for cell nodes easier
    nodes_id = np.reshape(t.nodes_id, (num_rows + 1, num_cols + 1))
    sw_cell_nodes_id = nodes_id[:num_rows, :num_cols].flatten()
    ne_cell_nodes_id = nodes_id[-num_rows:, -num_cols:].flatten()

    # IDs of cells are just num_cells consectutive integers
    t.cells_id = np.arange(t.num_cells)
    # All cells have the same number of nodes
    t.cells_num_nodes = num_nodes_per_cell * np.ones(t.num_cells, dtype='=i4')
    # Node IDs of cells:
    t.cells_nodes = np.empty((t.num_cells, num_nodes_per_cell), dtype='=i4')
    t.cells_nodes[:, 0] = sw_cell_nodes_id
    t.cells_nodes[:, 1] = sw_cell_nodes_id + 1
    t.cells_nodes[:, 2] = ne_cell_nodes_id
    t.cells_nodes[:, 3] = ne_cell_nodes_id - 1

    # Reshape these to make looking for cell walls easier
    cells_id = np.reshape(t.cells_id, (num_rows, num_cols))

    # Generate walls
    # Inner walls (those that don't touch the boundary polygon with ID -1)
    # West cells:
    w_cells_id = cells_id[:, :(num_cols - 1)].flatten()
    # East cells:
    e_cells_id = w_cells_id + 1
    # South cells:
    s_cells_id = cells_id[:(num_rows - 1), :].flatten()
    # North cells:
    n_cells_id = s_cells_id + num_cols

    # Vertical inner walls: (num_cols - 1) * num_rows
    # Connect W cells with E cells:
    vi_walls_cells = np.empty(((num_cols - 1) * num_rows, 2), dtype='=i4')
    vi_walls_cells[:, 0] = w_cells_id
    vi_walls_cells[:, 1] = e_cells_id

    # Horizontal inner walls: (num_rows - 1) * num_cols
    # Connect S cells with N cells:
    hi_walls_cells = np.empty(((num_rows - 1) * num_cols, 2), dtype='=i4')
    hi_walls_cells[:, 0] = s_cells_id
    hi_walls_cells[:, 1] = n_cells_id

    # South nodes:
    s_nodes_id = nodes_id[:num_rows, 1:-1].flatten()
    # North nodes:
    n_nodes_id = s_nodes_id + num_cols + 1
    # West nodes:
    w_nodes_id = nodes_id[1:-1, :num_cols].flatten()
    # East nodes:
    e_nodes_id = w_nodes_id + 1

    vi_walls_nodes = np.empty(((num_cols - 1) * num_rows, 2), dtype='=i4')
    vi_walls_nodes[:, 0] = s_nodes_id
    vi_walls_nodes[:, 1] = n_nodes_id

    hi_walls_nodes = np.empty(((num_rows - 1) * num_cols, 2), dtype='=i4')
    hi_walls_nodes[:, 0] = e_nodes_id
    hi_walls_nodes[:, 1] = w_nodes_id

    # Outer walls (those that do touch the boundary polygon with ID -1)
    # (south)
    s_walls_cells = np.empty((num_cols - 2, 2), dtype='=i4')
    s_walls_cells[:, 0] = -np.ones(num_cols - 2)
    s_walls_cells[:, 1] = cells_id[0, 1:-1]
    s_walls_nodes = np.empty_like(s_walls_cells)
    s_walls_nodes[:, 0] = nodes_id[0, 2:-1]
    s_walls_nodes[:, 1] = nodes_id[0, 1:-2]
    # (north)
    n_walls_cells = np.empty_like(s_walls_cells)
    n_walls_cells[:, 0] = cells_id[num_rows - 1,1:-1]
    n_walls_cells[:, 1] = -np.ones(num_cols - 2)
    n_walls_nodes = np.empty_like(n_walls_cells)
    n_walls_nodes[:, 0] = nodes_id[num_rows, 2:-1]
    n_walls_nodes[:, 1] = nodes_id[num_rows, 1:-2]
    # (west)
    w_walls_cells = np.empty((num_rows - 2, 2), dtype='=i4')
    w_walls_cells[:, 0] = -np.ones(num_rows - 2)
    w_walls_cells[:, 1] = cells_id[1:-1, 0]
    w_walls_nodes = np.empty_like(w_walls_cells)
    w_walls_nodes[:, 0] = nodes_id[1:-2, 0]
    w_walls_nodes[:, 1] = nodes_id[2:-1, 0]
    # (east)
    e_walls_cells = np.empty_like(w_walls_cells)
    e_walls_cells[:, 0] = cells_id[1:-1, num_cols - 1]
    e_walls_cells[:, 1] = -np.ones(num_rows - 2)
    e_walls_nodes = np.empty_like(e_walls_cells)
    e_walls_nodes[:, 0] = nodes_id[1:-2, num_cols]
    e_walls_nodes[:, 1] = nodes_id[2:-1, num_cols]

    t.walls_cells = np.vstack([vi_walls_cells,
                               hi_walls_cells,
                               s_walls_cells,
                               n_walls_cells,
                               w_walls_cells,
                               e_walls_cells,
                               [-1, 0],
                               [-1, t.num_cells - num_cols],
                               [-1, t.num_cells - 1],
                               [-1, num_cols - 1]])
    t.walls_nodes = np.vstack([vi_walls_nodes,
                               hi_walls_nodes,
                               s_walls_nodes,
                               n_walls_nodes,
                               w_walls_nodes,
                               e_walls_nodes,
                               [1, num_cols + 1],
                               [t.num_nodes - 2 * num_cols - 2, t.num_nodes - num_cols],
                               [t.num_nodes - 2, t.num_nodes - num_cols - 2],
                               [2 * num_cols + 1, num_cols - 1]])

    t.num_walls = t.walls_cells.shape[0]
    t.walls_id = np.arange(t.num_walls)

    # Loop over walls and check the cells they connect.
    # Each cell must appear in 4 walls, except corner cells which have 3 walls.
    t.cells_walls = [[] for _ in t.cells_id]
    t.cells_num_walls = np.zeros(t.num_cells, dtype='=i4')
    for w_idx in t.walls_id:
        [c_idx, d_idx] = t.walls_cells[w_idx, :]
        if c_idx != -1:
            t.cells_walls[c_idx].append(w_idx)
            t.cells_num_walls[c_idx] += 1
        if d_idx != -1:
            t.cells_walls[d_idx].append(w_idx)
            t.cells_num_walls[d_idx] += 1

    # That's it for the required data. The rest can be processed automatically.
    t.prepare_for_use()
    return t

