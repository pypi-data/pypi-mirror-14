from pypts.tissue import Tissue
import numpy as np
import scipy as sp

def hexagons(num_rows, num_cols, wall_length=1.0, bricks=True, two_thirds=False):
    """
    This function returns a rectagonal tissue of hexagonal cells, given the
    number of cell rows and cell columns.
    For example, the following tissue has 5 cell rows and 3 cell columns.
    (Notice the origin of the coordinate system is in the lower left corner)
    
     / \ / \ / \          \ 
    |   |   |   |         |
     \ / \ / \ / \        |
      |   |   |   |       |
     / \ / \ / \ /        |
    |   |   |   |         |- # rows
     \ / \ / \ / \        |
      |   |   |   |       |
     / \ / \ / \ /        |
    |   |   |   |         |
     \ / \ / \ /          /
    
    \______________/
           |
         #cols
    
    The total number of cells is: #rows * #cols                       (ex.: 15)
    The total number of nodes is: 2 * (#rows + 1) * (#cols + 1) - 2   (ex.: 46)

    Within a cell the nodes are labeled as:
             N
           /   \ 
        NW       NE
         |       |
        SW       SE
           \   /
             S
    Although hexagonal, I prefer to draw the cells as rectangles to align nodes
    horizontally for easier reference; this is the default behavior as
    indicated by the optional bricks argument:

        NW -- N -- NE
         |         |
        SW -- S -- SE

    Within a cell, the node counting starts from SW and follows in the ccw dir.

    Optionally, the bricks argument can be set to False to indicate that the
    node coordinates should be scaled such that all cells are regular hexagons.
    """
    # First I need an empty tissue to work on:
    t = Tissue()

    # See comment above
    t.num_cells = num_rows * num_cols
    t.num_nodes = 2 * (1 + num_rows) * (1 + num_cols) - 2
    num_nodes_per_cell = 6

    # Number of node rows and columns
    num_node_rows = num_rows + 1
    num_node_cols = 2 * (num_cols + 1)

    print '# node rows: ', num_node_rows
    print '# node cols: ', num_node_cols

    l = 1.0 # Length of a cell wall, used to calculate node spacing
    print ('Generating a rectangular tissue of {0} hex cells').format(t.num_cells)

    # IDs of nodes are just num_nodes consecutive integers
    t.nodes_id = np.arange(t.num_nodes)

    # IDs of cells are just num_cells consectutive integers
    t.cells_id = np.arange(t.num_cells)
    # All cells are hexagons and have the same number of nodes, 6
    t.cells_num_nodes = num_nodes_per_cell * np.ones(t.num_cells, dtype='=i4')
    # Space for the cells_nodes list of numpy arrays
    t.cells_nodes = [np.zeros(num_nodes_per_cell, dtype='=i4')
                     for _ in xrange(t.num_cells)]
    # Inner cells have 6 walls, boundary cells range from 3 to 6
    # Here, we just reserve space for the information
    t.cells_num_walls = np.empty(t.num_cells, dtype='=i4')
    t.cells_walls = [[] for _ in t.cells_id]

    # TODO: number of walls can be calculated explicitly to prevent extending
    # the below array over and over again.
    t.walls_cells = np.empty((0,2), dtype='=i4')
    t.walls_nodes = np.empty((0,2), dtype='=i4')

    # Used to keep track of wall id while adding them
    curr_wall_id = 0

    # In each cell row generate coordinates for the 'south' nodes and add the
    # top row nodes too.
    t.nodes_xy = np.empty((t.num_nodes,2), dtype='=f8')
    # First, the bottom row of nodes (has one node less than the middle rows)
    t.nodes_xy[:(num_node_cols-1),0] = np.arange(num_node_cols-1)
    t.nodes_xy[:(num_node_cols-1),1] = np.zeros(num_node_cols-1)
    # Then generate the middle rows
    for c_row_idx in xrange(1, num_rows):
        idx_beg = (c_row_idx * num_node_cols - 1)
        idx_end = idx_beg + num_node_cols
        t.nodes_xy[idx_beg:idx_end,0] = np.arange(num_node_cols)
        t.nodes_xy[idx_beg:idx_end,1] = np.repeat(c_row_idx, num_node_cols)
    # Finally, generate the upper row of nodes which also has one less node
    t.nodes_xy[-(num_node_cols-1):,0] = np.arange(num_node_cols-1) + ((num_rows + 1) % 2)
    t.nodes_xy[-(num_node_cols-1):,1] = np.repeat(num_rows, num_node_cols-1)

    # Scale the node coordinates to provide the requested wall_length
    t.nodes_xy *= wall_length

    # For true hexagons rescaling of node coordinates is necessary to guarantee
    # the requested wall length while creating regular hexagons for cells
    if not bricks:
        # X coordinates are scaled by multiplication with cos(pi / 6) as in:
        t.nodes_xy[:,0] *= 0.86602540378443871 # = cos(pi / 6)
        # Y coordinates need more work depending on their index and row being
        # even or odd. As before bottom and top rows of nodes are special cases
        t.nodes_xy[0:(num_node_cols-1):2,1] += 0.5 * wall_length
        for c_row_idx in xrange(1, num_rows):
            idx_beg = (c_row_idx * num_node_cols - 1)
            idx_end = idx_beg + num_node_cols
            if c_row_idx % 2 == 1:
                t.nodes_xy[idx_beg:idx_end:2,1] += 0.5 * wall_length * c_row_idx
                t.nodes_xy[(idx_beg+1):idx_end:2,1] += 0.5 * wall_length * (c_row_idx + 1)
            else:
                t.nodes_xy[idx_beg:idx_end:2,1] += 0.5 * wall_length * (c_row_idx + 1)
                t.nodes_xy[(idx_beg+1):idx_end:2,1] += 0.5 * wall_length * c_row_idx
        t.nodes_xy[-(num_node_cols-1)::2,1] += 0.5 * wall_length * num_rows
        t.nodes_xy[-(num_node_cols-2)::2,1] += 0.5 * wall_length * (num_rows + 1)

    # If cells are to be of the form:
    #
    #   o-----o-o-----o-o
    #   |       |       |
    # o-o-----o-o-----o-o
    # |       |       |
    # o-o-----o-o-----o-o
    #   |       |       |
    # o-o-----o-o-----o-o
    # |       |       |
    # o-o-----o-o-----o
    #
    # we need to shift certain points in each row a bit (2 x 1/6 of the wall
    # length) to the left
    if two_thirds:
        shift = wall_length / 3.0
        # First row of nodes is special: it has one point less than the others
        t.nodes_xy[1:(num_node_cols-1):2, 0] -= shift
        for n_row_idx in xrange(1, num_node_rows-1):
            # Other rows have length num_node_cols
            # (-1 for the pt the 1st row is missing)
            idx_beg = n_row_idx * num_node_cols - 1
            idx_end = idx_beg + num_node_cols
            t.nodes_xy[(1+idx_beg):idx_end:2, 0] -= shift
        # Last row has one point less again. Also, if the number of cell rows
        # is even, the even nodes must be shifted. If the number of cell rows
        # is odd, the odd nodes must be shifted
        t.nodes_xy[-(num_node_cols - 1 - (num_rows % 2))::2, 0] -= shift

    # Assemble all cells one by one
    for c_row_idx in xrange(num_rows):
        # Used for alternating indices for even/odd cell rows
        # (note that row_idx of first row is 0, which is even!!!)
        one_if_even_row = (c_row_idx + 1) % 2

        for c_col_idx in xrange(num_cols):
            # Id of current cell, will be used for the walls
            cell_id = c_row_idx * num_cols + c_col_idx
            # Id of the SW node of current cell
            sw_node_id = num_node_cols * c_row_idx + 2 * c_col_idx
            # In cell rows with even idx (and > 0) the sw_node_id is one less
            if c_row_idx % 2 == 0 and c_row_idx > 0:
                sw_node_id -= 1

            # South nodes of each cell are simple
            t.cells_nodes[c_row_idx*num_cols + c_col_idx][0] = sw_node_id
            t.cells_nodes[c_row_idx*num_cols + c_col_idx][1] = sw_node_id + 1
            t.cells_nodes[c_row_idx*num_cols + c_col_idx][2] = sw_node_id + 2

            # North nodes have two exceptions:
            if c_row_idx == 0 or (c_row_idx == num_rows - 1 and c_row_idx % 2 == 1):
                # ( first cell row ) AND ( last cell row (but only when its index is odd) )
                t.cells_nodes[c_row_idx*num_cols + c_col_idx][3] = sw_node_id + 2 + num_node_cols - 1
                t.cells_nodes[c_row_idx*num_cols + c_col_idx][4] = sw_node_id + 1 + num_node_cols - 1
                t.cells_nodes[c_row_idx*num_cols + c_col_idx][5] = sw_node_id + num_node_cols - 1
            else:
                # general case:
                t.cells_nodes[c_row_idx*num_cols + c_col_idx][3] = sw_node_id + 2 + num_node_cols
                t.cells_nodes[c_row_idx*num_cols + c_col_idx][4] = sw_node_id + 1 + num_node_cols
                t.cells_nodes[c_row_idx*num_cols + c_col_idx][5] = sw_node_id + num_node_cols

            # Distinguish between the 9 possible scenarios for adding walls
            if c_row_idx == 0:
                if c_col_idx == 0:
                    # Lower-left cell (with id 0) has 3 walls; add them all:
                    t.cells_num_walls[cell_id] = 3
                    # .--o--o       (o are end nodes, . are nodes inside walls)
                    # |     |
                    # .--.--o
                    t.walls_cells = np.vstack((t.walls_cells,
                                               [cell_id, cell_id + 1],
                                               [cell_id, cell_id + num_cols],
                                               [cell_id, -1]))
                    # Wall nodes
                    t.walls_nodes = np.vstack((t.walls_nodes,
                        [t.cells_nodes[cell_id][2], t.cells_nodes[cell_id][3]],
                        [t.cells_nodes[cell_id][3], t.cells_nodes[cell_id][4]],
                        [t.cells_nodes[cell_id][4], t.cells_nodes[cell_id][2]]))
                    curr_wall_id += 3
                elif c_col_idx < num_cols - 1:
                    # Lower-inner cells have 5 walls;
                    t.cells_num_walls[cell_id] = 5
                    # Add these 4 now:
                    # o--o--o       (o are end nodes, . are nodes inside walls)
                    #       |
                    # o--.--o
                    t.walls_cells = np.vstack((t.walls_cells,
                                               [cell_id, -1],
                                               [cell_id, cell_id + 1],
                                               [cell_id, cell_id + num_cols],
                                               [cell_id, cell_id + num_cols - 1]))
                    # Wall nodes
                    t.walls_nodes = np.vstack((t.walls_nodes,
                        [t.cells_nodes[cell_id][0], t.cells_nodes[cell_id][2]],
                        [t.cells_nodes[cell_id][2], t.cells_nodes[cell_id][3]],
                        [t.cells_nodes[cell_id][3], t.cells_nodes[cell_id][4]],
                        [t.cells_nodes[cell_id][4], t.cells_nodes[cell_id][5]]))
                    curr_wall_id += 4
                else:
                    # Lower-right cell (with id num_cols-1) has 4 walls
                    t.cells_num_walls[cell_id] = 4
                    # Add these 3 now:
                    # o--o--o       (o are end nodes, . are nodes inside walls)
                    #       |
                    # o--.--.
                    t.walls_cells = np.vstack((t.walls_cells,
                                               [cell_id, -1],
                                               [cell_id, cell_id + num_cols],
                                               [cell_id, cell_id + num_cols - 1]))
                    # Wall nodes
                    t.walls_nodes = np.vstack((t.walls_nodes,
                        [t.cells_nodes[cell_id][0], t.cells_nodes[cell_id][3]],
                        [t.cells_nodes[cell_id][3], t.cells_nodes[cell_id][4]],
                        [t.cells_nodes[cell_id][4], t.cells_nodes[cell_id][5]]))
                    curr_wall_id += 3
            elif c_row_idx < num_rows - 1:
                if c_col_idx == 0:
                    # Cells from inner-left region have 6 (odd rows) or 4 (even
                    # rows) walls.
                    if c_row_idx % 2 == 1:
                        t.cells_num_walls[cell_id] = 6
                        # Add these 4 now:
                        # o--o--o       (o are end nodes, . are nodes inside walls)
                        # |     |
                        # o  o  o
                        t.walls_cells = np.vstack((t.walls_cells,
                                                   [cell_id, cell_id + 1],
                                                   [cell_id, cell_id + num_cols + 1],
                                                   [cell_id, cell_id + num_cols],
                                                   [cell_id, -1]))
                        # Wall nodes
                        t.walls_nodes = np.vstack((t.walls_nodes,
                            [t.cells_nodes[cell_id][2], t.cells_nodes[cell_id][3]],
                            [t.cells_nodes[cell_id][3], t.cells_nodes[cell_id][4]],
                            [t.cells_nodes[cell_id][4], t.cells_nodes[cell_id][5]],
                            [t.cells_nodes[cell_id][5], t.cells_nodes[cell_id][0]]))
                        curr_wall_id += 4
                    else:
                        t.cells_num_walls[cell_id] = 4
                        # Add these 3 now:
                        # .--o--o       (o are end nodes, . are nodes inside walls)
                        # |     |
                        # .--o  o
                        t.walls_cells = np.vstack((t.walls_cells,
                                                   [cell_id, cell_id + 1],
                                                   [cell_id, cell_id + num_cols],
                                                   [cell_id, -1]))
                        # Wall nodes
                        t.walls_nodes = np.vstack((t.walls_nodes,
                            [t.cells_nodes[cell_id][2], t.cells_nodes[cell_id][3]],
                            [t.cells_nodes[cell_id][3], t.cells_nodes[cell_id][4]],
                            [t.cells_nodes[cell_id][4], t.cells_nodes[cell_id][1]]))
                        curr_wall_id += 3
                elif c_col_idx < num_cols - 1:
                    # Inner cells that don't touch the 'outer world' have 6
                    # walls. If we create half of these in each cell, we'll
                    # have the right number of walls in the end.
                    t.cells_num_walls[cell_id] = 6
                    # Add these three walls: right, upper right and upper left
                    # o--o--o       (o are nodes)
                    #       |
                    # o  o  o
                    #
                    # Which connect the cell as follows (if c_row_idx is odd)
                    #    o o        (o are cells)
                    #    |/
                    #    o-o
                    # ... or (if c_row_idx is even)
                    #  o o          (o are cells)
                    #   \| 
                    #    o-o
                    t.walls_cells = np.vstack((t.walls_cells,
                        [cell_id, cell_id + 1],
                        [cell_id, cell_id + num_cols - one_if_even_row + 1],
                        [cell_id, cell_id + num_cols - one_if_even_row]))
                    # Wall nodes
                    t.walls_nodes = np.vstack((t.walls_nodes,
                        [t.cells_nodes[cell_id][2], t.cells_nodes[cell_id][3]],
                        [t.cells_nodes[cell_id][3], t.cells_nodes[cell_id][4]],
                        [t.cells_nodes[cell_id][4], t.cells_nodes[cell_id][5]]))
                    curr_wall_id += 3
                else:
                    # Cells from inner-right region have 6 (even rows) or 4 (odd
                    # rows) walls.
                    if c_row_idx % 2 == 0:
                        t.cells_num_walls[cell_id] = 6
                        # Add these 3 now:
                        # o--o--o       (o are end nodes, . are nodes inside walls)
                        #       |
                        # o  o  o
                        t.walls_cells = np.vstack((t.walls_cells,
                                                   [cell_id, -1],
                                                   [cell_id, cell_id + num_cols],
                                                   [cell_id, cell_id + num_cols - 1]))
                        # Wall nodes
                        t.walls_nodes = np.vstack((t.walls_nodes,
                            [t.cells_nodes[cell_id][2], t.cells_nodes[cell_id][3]],
                            [t.cells_nodes[cell_id][3], t.cells_nodes[cell_id][4]],
                            [t.cells_nodes[cell_id][4], t.cells_nodes[cell_id][5]]))
                        curr_wall_id += 3
                    else:
                        t.cells_num_walls[cell_id] = 4
                        # Add these 2 now:
                        # o--o--.       (o are end nodes, . are nodes inside walls)
                        #       |
                        # o  o--.
                        t.walls_cells = np.vstack((t.walls_cells,
                                                   [cell_id, -1],
                                                   [cell_id, cell_id + num_cols]))
                        # Wall nodes
                        t.walls_nodes = np.vstack((t.walls_nodes,
                            [t.cells_nodes[cell_id][1], t.cells_nodes[cell_id][4]],
                            [t.cells_nodes[cell_id][4], t.cells_nodes[cell_id][5]]))
                        curr_wall_id += 2
            else:
                if c_col_idx == 0:
                    # Upper left cell: either even or odd cell row
                    if c_row_idx % 2 == 0:
                        # Even row: cell has 3 walls
                        t.cells_num_walls[cell_id] = 3
                        # Add the following 2:
                        # .--.--o       (o are end nodes, . are nodes inside walls)
                        # |     |
                        # .--o  o
                        t.walls_cells = np.vstack((t.walls_cells,
                                                   [cell_id, cell_id + 1],
                                                   [cell_id, -1]))
                        t.walls_nodes = np.vstack((t.walls_nodes,
                            [t.cells_nodes[cell_id][2], t.cells_nodes[cell_id][3]],
                            [t.cells_nodes[cell_id][3], t.cells_nodes[cell_id][1]]))
                        curr_wall_id += 2
                    else:
                        # Odd row: cell has 4 walls
                        t.cells_num_walls[cell_id] = 4
                        # Add the following 2:
                        # .--.--o       (o are end nodes, . are nodes inside walls)
                        # |     |
                        # o  o  o
                        t.walls_cells = np.vstack((t.walls_cells,
                                                   [cell_id, cell_id + 1],
                                                   [cell_id, -1]))
                        t.walls_nodes = np.vstack((t.walls_nodes,
                            [t.cells_nodes[cell_id][2], t.cells_nodes[cell_id][3]],
                            [t.cells_nodes[cell_id][3], t.cells_nodes[cell_id][0]]))
                        curr_wall_id += 2
                elif c_col_idx < num_cols - 1:
                    # Upper inner cells have 5 cell walls
                    t.cells_num_walls[cell_id] = 5
                    # Add the following 2:
                    # o--.--o       (o are end nodes, . are nodes inside walls)
                    #       |
                    # o  o  o
                    t.walls_cells = np.vstack((t.walls_cells,
                                               [cell_id, cell_id + 1],
                                               [cell_id, -1]))
                    t.walls_nodes = np.vstack((t.walls_nodes,
                        [t.cells_nodes[cell_id][2], t.cells_nodes[cell_id][3]],
                        [t.cells_nodes[cell_id][3], t.cells_nodes[cell_id][5]]))
                    curr_wall_id += 2
                else:
                    # Upper right cell: either even or odd cell row
                    if c_row_idx % 2 == 0:
                        # Even row: cell has 4 walls
                        t.cells_num_walls[cell_id] = 4
                        # Add the following 1:
                        # o--.--.       (o are end nodes, . are nodes inside walls)
                        #       |
                        # o  o  o
                        t.walls_cells = np.vstack((t.walls_cells,
                                                   [cell_id, -1]))
                        t.walls_nodes = np.vstack((t.walls_nodes,
                            [t.cells_nodes[cell_id][2], t.cells_nodes[cell_id][5]]))
                        curr_wall_id += 1
                    else:
                        # Odd row: cell has 3 walls
                        t.cells_num_walls[cell_id] = 3
                        # Add the following 1:
                        # o--.--.       (o are end nodes, . are nodes inside walls)
                        #       |
                        # o  o--.
                        t.walls_cells = np.vstack((t.walls_cells,
                                                   [cell_id, -1]))
                        t.walls_nodes = np.vstack((t.walls_nodes,
                            [t.cells_nodes[cell_id][1], t.cells_nodes[cell_id][5]]))
                        # Add new walls to the current cell & increase cntr
                        curr_wall_id += 1

    t.num_walls = curr_wall_id
    t.walls_id = np.arange(t.num_walls)

    # For each wall assign its id to the two cells it connects
    # TODO: I might be able to do that in the previous loop
    for w_id in t.walls_id:
        for c_id in t.walls_cells[w_id]:
            if c_id != -1:
                t.cells_walls[c_id].append(w_id)

    # Convert the cells_walls to a list of numpy arrays which makes it more
    # consistent with tissues loaded from files
    for c_idx in xrange(t.num_cells):
        t.cells_walls[c_idx] = np.array(t.cells_walls[c_idx], dtype=np.int32)

    # That's it for the required data. The rest can be processed automatically.
    t.prepare_for_use()
    return t

