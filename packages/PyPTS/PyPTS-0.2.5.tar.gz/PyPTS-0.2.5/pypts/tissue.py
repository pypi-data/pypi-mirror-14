import sys
import h5py
import logging
import numpy as np
import scipy as sp
import numpy.linalg as npla

def get_time_steps(tissue_file_name):
    """
    Returns two arrays as a tuple: time_steps and time_steps_idx arrays
    contained in the requested tissue file.
    This is used to get time steps info without having to read the whole file.
    """
    # Used for error reporting
    err_str = 'Dataset / group \'{0}\' not found in file \'{1}\''

    # Open the HDF5 file with tissue data
    tissue_file = h5py.File(tissue_file_name, 'r')

    # =====================================================================
    # Read time steps:
    #   /time_steps          Time step values in seconds
    #   /time_steps_idx      Indices of time steps, refer to n in '/step_n'

    if '/time_steps' in tissue_file:
        time_steps = tissue_file['/time_steps'][...]
    else:
        raise Exception(err_str.format('/time_steps', tissue_file_name))

    if '/time_steps_idx' in tissue_file:
        time_steps_idx = tissue_file['/time_steps_idx'][...]
    else:
        raise Exception(err_str.format('/time_steps_idx', tissue_file_name))

    # We're done reading, close the HDF5 file with tissue data & return values
    tissue_file.close()
    return (time_steps, time_steps_idx)

class Tissue(object):
    def __init__(self, tissue_file_name=None, step=None):
        """
        Constructs an empty tissue or loads one from a vleaf HDF5 file.
        By default the last step (i.e. '/step_n' group with highest n) is read.
        This default behavior can be overridden when the step argument
        is used explicitly to specify which steps should be read.

        Upon reading, the following data members are available in the tissue:
            Nodes:
            =====
                num_nodes           Number of nodes
                nodes_id            IDs of nodes, length: num_nodes
                nodes_idx           Dictionary of node indices stored by ID
                                    length: num_nodes
                nodes_xy            Coordinates of nodes, dims: (num_nodes, 2)
                nodes_nodes         IDs of neighboring nodes (TODO: could be removed as it's just cached info that can be reproduced from nodes_edges)
                nodes_edges         IDs of edges incident to nodes
                nodes_walls         TODO: Whenever the need arises
                nodes_cells         TODO: Whenever the need arises
                nodes_attributes    Dict. of node based attribute values
                                    Each element in dict. has length num_nodes

            Cells:
            =====
                num_cells           Number of cells
                cells_id            IDs of cells, length: num_cells
                cells_idx           Dict. of cell indices
                                    keys: IDs
                                    values: index values
                                    length: num_cells
                cells_num_nodes     Number of nodes in each cell
                cells_nodes         IDs of nodes in each cell (CCW)
                cells_edges         TODO: Whenever the need arises
                cells_num_walls     Number of walls in each cell
                cells_walls         IDs of walls in each cell
                cells_cells         IDs of neighboring cells
                cells_attributes    Dict. of cell based attribute values
                                    Each element in dict. has length num_cells

            Boundary polygon:
            ================
                bp_nodes            IDs of nodes in the boundary polygon (CW)
                bp_walls            IDs of walls in ths boundary polygon (CW)

            Walls:
            =====
                num_walls           Number of walls
                walls_id            IDs of walls, length: num_walls
                walls_idx           Dict. of wall indices
                                    keys: IDs
                                    values: index values
                                    length: num_walls
                walls_nodes
                walls_edges         IDs / index values of edges in a wall
                walls_walls         TODO: whenever the need arises
                walls_cells
                walls_attributes    Dict. of wall based attribute values
                                    Each element in dict. has length num_walls

            Edges:
            =====
                num_edges           Number of edges
                edges_idx           Index values of edges
                                    (IDs not available since equiv. to idx)
                edges_nodes         IDs of the two nodes connected by the edge
                edges_edges         TODO: whenever the need arises
                edges_walls         IDs of walls that contain an edge
                edges_cells         IDs of the two cells connected by the edge
                edges_attributes    Dict. of edge based attribute values
                                    Each element in dict. has length num_edges
        """
        if tissue_file_name is not None:
            self.load(tissue_file_name, step)
        else:
            # Create a minimal tissue with no nodes / cells / walls
            # Required node entities
            self.num_nodes = 0
            self.nodes_id = np.empty(0, dtype=np.int32)
            self.nodes_xy = np.empty((0,2), dtype=np.float64)
            self.nodes_attributes = {}

            # Required cell entities
            self.num_cells = 0
            self.cells_id = np.empty(0, dtype=np.int32)
            self.cells_nodes = []
            self.cells_num_nodes = np.empty(0, dtype=np.int32)
            self.cells_walls = []
            self.cells_num_walls = np.empty(0, dtype=np.int32)
            self.cells_attributes = {}

            # Required wall entities
            self.num_walls = 0
            self.walls_id = np.empty(0, dtype=np.int32)
            self.walls_cells = np.empty((0,2), dtype=np.int32)
            self.walls_nodes = np.empty((0,2), dtype=np.int32)
            self.walls_attributes = {}

        # Make sure the loaded tissue is checked and that all incidence
        # relations are set up and cached.
        self.prepare_for_use()

    def load(self, tissue_file_name, step=None):
        """
        Loads the state of a tissue from a vleaf HDF5 file.
        By default the last step (i.e. '/step_n' group with highest n) is read.
        This default behavior can be overridden when the step argument
        is used explicitly to specify which steps should be read.

        Upon reading, the following data members are available in the tissue:
            Nodes:
            =====
                num_nodes           Number of nodes
                nodes_id            IDs of nodes, length: num_nodes
                nodes_xy            Coordinates of nodes, dims: (num_nodes, 2)
                nodes_attributes    Dict. of node based attribute values
                                    Each element in dict. has length num_nodes

            Cells:
            =====
                num_cells           Number of cells
                cells_id            IDs of cells, length: num_cells
                cells_num_nodes     Number of nodes in each cell
                cells_nodes         IDs of nodes in each cell (CCW)
                cells_num_walls     Number of walls in each cell
                cells_walls         IDs of walls in each cell
                cells_attributes    Dict. of cell based attribute values
                                    Each element in dict. has length num_cells

            Walls:
            =====
                num_walls           Number of walls
                walls_id            IDs of walls, length: num_walls
                walls_nodes
                walls_cells
                walls_attributes    Dict. of wall based attribute values
                                    Each element in dict. has length num_walls

        Note that prior to doing any useful work with the tissue the function
        'prepare_for_use()' must be called to set up all other necessary info
        that's not stored in the HDF5 file.
        """
        logger = logging.getLogger(__name__)
        # Used for error reporting
        err_str = 'Dataset / group \'{0}\' not found in file \'{1}\''

        # Open the HDF5 file with tissue data
        logger.info('Loading tissue from file \'{0}\''.format(tissue_file_name))
        tissue_file = h5py.File(tissue_file_name, 'r')

        # =====================================================================
        # Read time steps:
        #   /time_steps          Time step values in seconds
        #   /time_steps_idx      Indices of time steps, refer to n in '/step_n'

        if '/time_steps' in tissue_file:
            self.time_steps = tissue_file['/time_steps'][...]
        else:
            raise Exception(err_str.format('/time_steps', tissue_file_name))

        if '/time_steps_idx' in tissue_file:
            self.time_steps_idx = tissue_file['/time_steps_idx'][...]
        else:
            raise Exception(err_str.format('/time_steps_idx', tissue_file_name))

        # The number of steps contained in the file (<= the number of steps
        # performed during simulation; depending on the stride)
        num_steps = self.time_steps.shape[0]
        if step == None:
            # Take the last saved step by default
            curr_step_idx = self.time_steps_idx[-1]
        else:
            # If a step was given, try to use it
            if step in self.time_steps_idx:
                curr_step_idx = step
            else:
                raise Exception(err_str.format('/step_n', tissue_file_name))

        # Open the HDF5 group that contains all of the current step
        step_grp = tissue_file[('/step_{0}').format(curr_step_idx)]
        logger.info('Using tissue data from \'{0}\''.format(step_grp.name))

        # =====================================================================
        # Read nodes:
        #   /step_n/nodes_id            The IDs of all nodes
        #           nodes_xy(z)         Coordinates of all nodes
        #           nodes_attr_*        node-based attribute values

        # /step_n/nodes_id
        if 'nodes_id' in step_grp:
            self.nodes_id = step_grp['nodes_id'][...]
        else:
            raise Exception(err_str.format(step_grp.name + '/nodes_id',
                                           tissue_file_name))
        # Number of nodes in the tissue at current step
        self.num_nodes = self.nodes_id.shape[0]

        # /step_n/nodes_xy(z)
        if 'nodes_xyz' in step_grp:
            self.nodes_xyz = step_grp['nodes_xyz'][...]
        elif 'nodes_xy' in step_grp:
            self.nodes_xy = step_grp['nodes_xy'][...]
        else:
            raise Exception(err_str.format(step_grp.name + '/nodes_xy(z)',
                                           tissue_file_name))

        # Load node attributes into a dictionary {attr_name: attr_values, ...}
        # Node attributes are datasets whose name starts with 'nodes_attr_'
        # 'nodes_attr_' prefix (len=11) must be removed to get the actual name
        n_attr_names = [ds for ds in step_grp if ds.startswith('nodes_attr_')]
        # Start with an empty dict for node attributes, loop over the attribute
        # names and read the attribute data
        self.nodes_attributes = {}
        for attr_name in n_attr_names:
            if step_grp[attr_name].dtype.kind in ['i', 'f']:
                # In case of int or float data conversion will be automatic
                self.nodes_attributes[attr_name[11:]] = \
                    step_grp[attr_name][...]
            elif step_grp[attr_name].dtype == h5py.special_dtype(vlen=str):
                # If variable length strings are used in HDF5 the dtype will be
                # an object with some additional data. Convert it to a numpy
                # array of strings which is more convenient to handle later.
                self.nodes_attributes[attr_name[11:]] = \
                    np.array([str(el) for el in step_grp[attr_name][...]])
            else:
                # No other dtypes are supported as of now.
                logger.warning('\'' + attr_name + '\' ignored; unsupported data type')

        # =====================================================================
        # Read cells:
        #   /step_n/cells_id            The IDs of all cells
        #           cells_num_nodes     How many nodes each cell has
        #           cells_nodes         IDs of the nodes of all cells
        #           cells_num_walls     How many walls each cell has
        #           cells_walls         IDs of the walls of all cells
        #           cells_attr_*        Cell-based attribute values

        # /step_n/cells_id
        if 'cells_id' in step_grp:
            self.cells_id = step_grp['cells_id'][...]
        else:
            raise Exception(err_str.format(step_grp.name + '/cells_id',
                                           tissue_file_name))
        # Number of cells in the tissue at current step
        self.num_cells = self.cells_id.shape[0]

        # /step_n/cells_num_nodes
        if 'cells_num_nodes' in step_grp:
            self.cells_num_nodes = step_grp['cells_num_nodes'][...]
        else:
            raise Exception(err_str.format(step_grp.name + '/cells_num_nodes',
                                           tissue_file_name))

        # /step_n/cells_nodes
        if 'cells_nodes' in step_grp:
            cells_nodes_data = step_grp['cells_nodes'][...]
        else:
            raise Exception(err_str.format(step_grp.name + '/cells_nodes',
                                           tissue_file_name))
        # Remove the padding by storing cells_nodes in a list of numpy arrays
        # (instead of a 2D numpy array with padding)
        self.cells_nodes = \
            [np.array([], dtype=np.int32) for _ in xrange(self.num_cells)]
        for c_idx in xrange(self.num_cells):
            self.cells_nodes[c_idx] = \
                cells_nodes_data[c_idx, :self.cells_num_nodes[c_idx]]

        # /step_n/cells_num_walls
        if 'cells_num_walls' in step_grp:
            self.cells_num_walls = step_grp['cells_num_walls'][...]
        else:
            raise Exception(err_str.format(step_grp.name + '/cells_num_walls',
                                           tissue_file_name))

        # /step_n/cells_walls
        if 'cells_walls' in step_grp:
            cells_walls_data = step_grp['cells_walls'][...]
        else:
            raise Exception(err_str.format(step_grp.name + '/cells_walls',
                                           tissue_file_name))
        # Remove the padding by storing cells_walls in a list of numpy arrays
        # (instead of a 2D numpy array with padding)
        self.cells_walls = \
            [np.array([], dtype=np.int32) for _ in xrange(self.num_cells)]
        for c_idx in xrange(self.num_cells):
            self.cells_walls[c_idx] = \
                cells_walls_data[c_idx, :self.cells_num_walls[c_idx]]

        # Load cell attributes into a dictionary {attr_name: attr_values, ...}
        # Cell attributes are datasets whose name starts with 'cells_attr_'
        # 'cells_attr_' prefix (len=11) must be removed to get the actual name
        c_attr_names = [ds for ds in step_grp if ds.startswith('cells_attr_')]
        # Start with an empty dict for cell attributes, loop over the attribute
        # names and read the attribute data
        self.cells_attributes = {}
        for attr_name in c_attr_names:
            if step_grp[attr_name].dtype.kind in ['i', 'f']:
                # In case of int or float data conversion will be automatic
                self.cells_attributes[attr_name[11:]] = \
                    step_grp[attr_name][...]
            elif step_grp[attr_name].dtype == h5py.special_dtype(vlen=str):
                # If variable length strings are used in HDF5 the dtype will be
                # an object with some additional data. Convert it to a numpy
                # array of strings which is more convenient to handle later.
                self.cells_attributes[attr_name[11:]] = \
                    np.array([str(el) for el in step_grp[attr_name][...]])
            else:
                # No other dtypes are supported as of now.
                logger.warning('\'' + attr_name + '\' ignored; unsupported data type')

        # =====================================================================
        # TODO: the boundary polygon complicates things unnecessarily, consider
        # removing it. For now it's commented away to check if it's necessary.
        # TODO: Since VirtualLeaf requires the boundary polygon in its files
        # it is calculated explicitly in Tissue.prepare_for_use() using
        # Tissue.update_boundary_polygon(). See there for some more info
        # ragarding the ordering of nodes and walls of the boundary polygon.
        #
        # Read the boundary polygon:
        #   /step_n/bp_nodes            IDs of nodes in the boundary polygon
        #           bp_walls            IDs of walls in the boundary polygon
        # /step_n/bp_nodes
        #if 'bp_nodes' in step_grp:
            #self.bp_nodes = step_grp['bp_nodes'][...].tolist()
            # It's more convenient (and makes more sense) to have the boundary
            # polygon in inverse order, it's CCW but inside out, hence CW.
            # Unfortunately VL uses CCW ordering for the boundary polygon so
            # the list of node IDs needs to be reverted for I/O.
            #self.bp_nodes.reverse()
        #else:
            #raise Exception(err_str.format(step_grp.name + '/bp_nodes',
                                           #tissue_file_name))

        # /step_n/bp_walls
        #if 'bp_walls' in step_grp:
            #self.bp_walls = step_grp['bp_walls'][...].tolist()
        #else:
            #raise Exception(err_str.format(step_grp.name + '/bp_walls',
                                           #tissue_file_name))

        # =====================================================================
        # Read walls:
        #   /step_n/walls_id            The IDs of all walls
        #           walls_cells         IDs of the cells connected by walls
        #           walls_nodes         IDs of the end nodes of walls
        #           walls_attr_*        Wall-based attribute values

        # /step_n/walls_id
        if 'walls_id' in step_grp:
            self.walls_id = step_grp['walls_id'][...]
        else:
            raise Exception(err_str.format(step_grp.name + '/walls_id',
                                           tissue_file_name))
        # Number of walls in the tissue at current step
        self.num_walls = self.walls_id.shape[0]

        # /step_n/walls_cells
        if 'walls_cells' in step_grp:
            self.walls_cells = step_grp['walls_cells'][...]
        else:
            raise Exception(err_str.format(step_grp.name + '/walls_cells',
                                           tissue_file_name))

        # /step_n/walls_nodes
        if 'walls_nodes' in step_grp:
            self.walls_nodes = step_grp['walls_nodes'][...]
        else:
            raise Exception(err_str.format(step_grp.name + '/walls_nodes',
                                           tissue_file_name))

        # Load wall attributes into a dictionary {attr_name: attr_values, ...}
        # Wall attributes are datasets whose name starts with 'walls_attr_'
        # 'walls_attr_' prefix (len=11) must be removed to get the actual name
        w_attr_names = [ds for ds in step_grp if ds.startswith('walls_attr_')]
        # Start with an empty dict for wall attributes, loop over the attribute
        # names and read the attribute data
        self.walls_attributes = {}
        for attr_name in w_attr_names:
            if step_grp[attr_name].dtype.kind in ['i', 'f']:
                # In case of int or float data conversion will be automatic
                self.walls_attributes[attr_name[11:]] = \
                    step_grp[attr_name][...]
            elif step_grp[attr_name].dtype == h5py.special_dtype(vlen=str):
                # If variable length strings are used in HDF5 the dtype will be
                # an object with some additional data. Convert it to a numpy
                # array of strings which is more convenient to handle later.
                self.walls_attributes[attr_name[11:]] = \
                    np.array([str(el) for el in step_grp[attr_name][...]])
            else:
                # No other dtypes are supported as of now.
                logger.warning('\'' + attr_name + '\' ignored; unsupported data type')

        # We're done reading, close the HDF5 file with tissue data
        tissue_file.close()

    def prepare_for_use(self):
        """
        TODO: document why this is necessary
        """
        # =====================================================================
        # Tissue preprocessing:

        # Preprocess ID <-> idx translation maps for cells / nodes / walls
        self.nodes_idx = \
            {n_id : n_idx for (n_idx, n_id) in enumerate(self.nodes_id)}
        self.cells_idx = \
            {c_id : c_idx for (c_idx, c_id) in enumerate(self.cells_id)}
        self.walls_idx = \
            {w_id : w_idx for (w_idx, w_id) in enumerate(self.walls_id)}

        # Cell connectivity information:
        # -----------------------------
        # Cached cell neighbor IDs for cells
        self.cache_cell_neighbors()

        # Create edges from walls:
        # -----------------------
        # An edge is a direct connection between two nodes.
        # Each wall contains at least one edge and each edge is contained
        # in exactly one wall. This means that looping over walls and
        # collecting edges is sufficient to get all edges.
        #
        # The following information about edges must be constructed:
        # (which is all pretty similar to wall information)
        #
        #   edges_cells         IDs of the two cells incident with each edge
        #   edges_nodes         IDs of the two nodes incident with each edge
        #   edges_walls         ID of the wall each edge is part of
        #   edges_attributes    General edge attributes
        #   walls_edges         IDs of edges contained in a wall

        self.edges_walls = np.array([], dtype=np.int32)
        self.edges_nodes = np.zeros((0, 2), dtype=np.int32)
        self.edges_cells = np.zeros((0, 2), dtype=np.int32)
        self.walls_edges = \
            [np.array([], dtype=np.int32) for _ in xrange(self.num_walls)]
        self.walls_nodes_all = \
            [np.array([], dtype=np.int32) for _ in xrange(self.num_walls)]

        # Loop over all walls and extract edges
        # (start from edge with idx 0 and increase the idx while adding edges)
        # Since edges are never stored or deleted after creation, it doesn't
        # make sense to distinguish between edge ID and index. As a convention
        # index values are used throughout the code.
        e_idx = 0
        for w_idx in xrange(self.num_walls):
            cs_id = self.walls_cells[w_idx, :] # IDs of neighboring cells
            ns_id = self.walls_nodes[w_idx, :] # IDs of start/end wall nodes
            w_id = self.walls_id[w_idx] # ID of the current wall
            # Shorthand for cells connected by current wall
            c0_id = cs_id[0]
            c1_id = cs_id[1]
            
            # A wall's orientation follows the CCW order of nodes in the FIRST
            # of its cells (i.e: c0).
            # cfr:          c0
            #        n0 -- ... -> n1
            #               c1
            # so we need to get c0's nodes before we do anything else
            if -1 == c0_id:
                # c0 is the boundary polygon, get its nodes from bp_nodes
                # get the nodes from c1, reversed.
                c0_ns_id = self.cells_nodes[self.cells_idx[c1_id]].tolist()
                c0_ns_id.reverse()
                #c0_ns_id = self.bp_nodes
                pass
            else:
                # c0 is a regular cell, get its nodes from cells_nodes
                c0_ns_id = self.cells_nodes[self.cells_idx[c0_id]].tolist()

            # Find position of start/end nodes (n0/n1) of current wall in the
            # node list of c0
            n0_pos = c0_ns_id.index(ns_id[0])
            n1_pos = c0_ns_id.index(ns_id[1])

            # Check for wrap-around:
            if n0_pos < n1_pos:
                # If no wrap around, then the wall nodes are just a
                # contiguous subset of c0's nodes
                # I.e: cells_nodes[c0_idx] = [... (n0 ... n1) ...]
                wall_nodes = c0_ns_id[n0_pos:(n1_pos + 1)]
            else:
                # If there is wrap around; go from wall's first node to
                # c0's last node and from c0's first node to wall's last
                # I.e: cells_nodes[c0_idx] = [... n1) ... (n0 ...]
                wall_nodes = c0_ns_id[n0_pos:] + c0_ns_id[:(n1_pos + 1)]

            # TODO; new
            self.walls_nodes_all[w_idx] = np.array(wall_nodes)

            # Now, we have a list of the node IDs of the current wall.
            # Loop through these nodes in pairs and create edges for each pair,
            # adding information about the cells / nodes they connect and the
            # wall they belong to.
            for e_n0_id, e_n1_id in zip(wall_nodes[:-1], wall_nodes[1:]):
                # Currently added edge is part of the currently visited wall.
                self.edges_walls = np.append(self.edges_walls, w_id)
                # Edge will have the same orientation as the wall it's part of
                self.edges_nodes = np.vstack((self.edges_nodes,
                                              [e_n0_id, e_n1_id]))
                self.edges_cells = np.vstack((self.edges_cells,
                                              [c0_id, c1_id]))
                # Add current edge index to the currently visited wall
                self.walls_edges[w_idx] = np.append(self.walls_edges[w_idx],
                                                    e_idx)
                e_idx += 1

        # Number of edges
        self.num_edges = self.edges_walls.shape[0]

        # Indices of edges (equivalent to IDs)
        self.edges_idx = xrange(self.num_edges)

        self.edges_attributes = {}

        # Edges connect both two cells and two nodes together, we preprocess
        # this information by looping through all edges and collect the cells
        # and nodes they connect in two lookup tables
        #
        # Cached neighbor index values for and nodes
        self.nodes_nodes = \
            [np.array([], dtype=np.int32) for _ in xrange(self.num_nodes)]

        self.nodes_edges = \
            [np.array([], dtype=np.int32) for _ in xrange(self.num_nodes)]

        # Loop over the edges and gather neighbors of cells and nodes
        for e_idx in xrange(self.num_edges):
            # Nodes
            ns_id = self.edges_nodes[e_idx, :] # IDs of start/end wall edge nodes
            # Translate to index values
            ns_idx = [self.nodes_idx[n_id] for n_id in ns_id]
            # For incidence of nodes it doesn't matter that one of the cells
            # is the boundary polygon
            self.nodes_nodes[ns_idx[0]] = np.append(self.nodes_nodes[ns_idx[0]],
                                                   ns_id[1])
            self.nodes_nodes[ns_idx[1]] = np.append(self.nodes_nodes[ns_idx[1]],
                                                   ns_id[0])
            # Same for the incidence of nodes with adjacent edges
            self.nodes_edges[ns_idx[0]] = np.append(self.nodes_edges[ns_idx[0]],
                                                   e_idx)
            self.nodes_edges[ns_idx[1]] = np.append(self.nodes_edges[ns_idx[1]],
                                                   e_idx)

        # Make sure the boundary polygon is correct
        self.update_boundary_polygon()

    def get_cell_nodes_coord(self, c_idx):
        """
        Returns the xy coordinates of a cell's nodes.
        All indexing is done using POSITIONAL INDICES.
        TODO: not 100% sure I need this
        """
        # Get cell node IDs, translate to index values & get their coordinates
        cell_nodes_id = self.cells_nodes[c_idx]
        cell_nodes_idx = [self.nodes_idx[n_id] for n_id in cell_nodes_id]
        if hasattr(self, 'nodes_xyz'):
            return self.nodes_xyz[cell_nodes_idx, :]
        else:
            return self.nodes_xy[cell_nodes_idx, :]

    #def get_length_of_wall_old(self, w_idx):
        #"""
        #Returns the length of a wall, i.e.: sum of the lengths of its edges.
        #TODO: I'm keeping it around for now to check if the results form the
        #optimized version below are identical.
        #"""
        #length = 0.0
        #for e_idx in self.walls_edges[w_idx]:
            #ns_id = self.edges_nodes[e_idx]
            #length += \
                #np.linalg.norm(self.nodes_xy[ns_id[0]] - self.nodes_xy[ns_id[1]])
        #return length

    def get_length_of_wall(self, w_idx):
        """
        Returns the length of a wall, i.e.: sum of the lengths of its edges.
        """
        # XY coordinates of the requested wall's nodes, ordered from n0 -> n1
        if hasattr(self, 'nodes_xyz'):
            wall_nodes_coord = self.nodes_xyz[self.walls_nodes_all[w_idx], :]
        else:
            wall_nodes_coord = self.nodes_xy[self.walls_nodes_all[w_idx], :]
        # I'm trying to do this as quickly as possible: it's a freq. operation
        v = wall_nodes_coord[1:] - wall_nodes_coord[:-1]
        v = v**2
        return sum(np.sqrt(v[:,0] + v[:,1]))

    def get_area_of_cell_old(self, c_idx):
        """
        Returns the area of a cell, i.e.: area of the cell's 2D polygon.
        TODO: I'm keeping it around for now to check if the results form the
        optimized version below are identical.
        """
        # XY coordinates of the requested cell
        xy = self.get_cell_nodes_coord(c_idx)
        return 0.5 * np.sum(xy[:,0] * np.roll(xy[:,1], -1)
                            - xy[:,1] * np.roll(xy[:,0], -1)
                            )

    def get_area_of_cell_fast(self, c_idx):
        """
        Returns the area of a cell, i.e.: area of the cell's 2D polygon.
        NOTE: assumes id = idx for nodes.
        """
        ns_idx = self.cells_nodes[c_idx]
        xy = self.nodes_xy[ns_idx,:]
        xy_rolled = np.roll(xy, -1, axis=0)
        return 0.5 * sum(xy[:,0] * xy_rolled[:,1] - xy[:,1] * xy_rolled[:,0])

    def get_area_of_cell(self, c_idx):
        """
        Returns the area of a cell, i.e.: area of the cell's 2D polygon.
        """
        # XY coordinates of the requested cell
        xy = self.get_cell_nodes_coord(c_idx)
        xy_rolled = np.roll(xy, -1, axis=0)
        return 0.5 * sum(xy[:,0] * xy_rolled[:,1] - xy[:,1] * xy_rolled[:,0])

    def get_moments_of_cell(self, c_idx):
        """
        Returns a tuple with the area, 1st and 2nd moments of a cell's polygon:
        (A, M_x, M_y, I_xx, I_yy, I_xy)
        where:
            A is the area of the cell: \sum (x_{i} y_{i+1} - x_{i+1} y_{i}) / 2
            M_x/y are the first moments, a.k.a. the coordinates of the center
                of mass (centroid).
            I_xx/yy/xy are the second moments
        Cfr.:
            http://dx.doi.org/10.1016/0098-3004(84)90032-3
            http://dx.doi.org/10.1016/0098-3004(88)90025-8
            http://dx.doi.org/10.1016/0098-3004(76)90008-X
            http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon
        """
        c_ns_xy = self.get_cell_nodes_coord(c_idx)

        # Will accumulate these quantities while looping over cell's nodes xy
        A = M_x = M_y = I_xx = I_yy = I_xy = 0.0

        # Loop zipped over nodes and 'rolled' nodes to get access to i and i+1
        # and cover the wrap-around at the same time.
        # (j plays the role of i+1)
        for (xy_i, xy_j) in zip(c_ns_xy, np.roll(c_ns_xy, -1, axis=0)):
            # a_{i} = x_{i} * y_{i+1} - x_{i+1} * y_{i}
            a_i = xy_i[0] * xy_j[1] - xy_j[0] * xy_i[1]

            # A = \sum a_{i} / 2
            A += a_i
            # M_x = \sum a_{i} (x_{i} + x_{i+1}) / (6A)
            M_x += (xy_i[0] + xy_j[0]) * a_i
            # M_y = \sum a_{i} (y_{i} + y_{i+1}) / (6A)
            M_y += (xy_i[1] + xy_j[1]) * a_i
            # I_xx = \sum a_{i} (y_{i}^{2} + y_{i} y_{i+1} + y_{i+1}^{2}) / 12
            I_xx += (xy_i[1]**2 + xy_i[1] * xy_j[1] + xy_j[1]**2) * a_i
            # I_yy = \sum a_{i} (x_{i}^{2} + x_{i} x_{i+1} + x_{i+1}^{2}) / 12
            I_yy += (xy_i[0]**2 + xy_i[0] * xy_j[0] + xy_j[0]**2) * a_i
            # I_xy = -\sum a_{i} (2 x_{i} y_{i} + 2 x_{i+1} y_{i+1}
            #                     + x_{i} y_{i+1} + x_{i+1} y_{i}
            #                    ) / 24
            I_xy += (2.0 * xy_i[0] * xy_i[1] + 2.0 * xy_j[0] * xy_j[1] \
                     + xy_i[0] * xy_j[1] + xy_j[0] * xy_i[1]) * a_i

        # Make sure the constant factors and signs are ok
        # For the correct interpretation, cfr. references above.
        A /= 2.0
        M_x /= (6.0 * A)
        M_y /= (6.0 * A)
        I_xx /= 12.0
        I_yy /= 12.0
        I_xy /= -24.0

        return (A, M_x, M_y, I_xx, I_yy, I_xy)

    def cache_cell_neighbors(self):
        """
        Internal helper function that creates cells_cells incidence relations
        based on cells_walls and walls_cells. Not to be called by end user!
        """
        def other_thing(two_things, one_thing):
            """
            Returns the other thing than one_thing from an array (or tuple)
            of two things.
            """
            if one_thing == two_things[0]: return two_things[1]
            elif one_thing == two_things[1]: return two_things[0]
            #else: raise Exception(str(one_thing) + ' not in ' + str(two_things))
            else: raise Exception(('{0} not in {1}').format(one_thing,
                                                            two_things))

        self.cells_cells = \
            [np.array([], dtype=np.int32) for _ in xrange(self.num_cells)]

        # Loop over all walls in all cells to extract cell cell connections
        # (Just looping over the walls would neglect the ordering of neighbor
        # cells w.r.t. the walls in a cell)
        for c_idx in self.cells_idx:
            c_id = self.cells_id[c_idx] # ID of current cell
            # Loop through all walls in current cell
            for w_id in self.cells_walls[c_idx]:
                w_idx = self.walls_idx[w_id]
                # Get the IDs of the two cells connected by the current wall
                # and find the cell on the OTHER side (hence the if/else to
                # distinguish current cell from its neighbors)
                # TODO: use other_thing
                cs_id = self.walls_cells[w_idx, :]
                if c_id != cs_id[0]:
                    self.cells_cells[c_idx] = \
                        np.append(self.cells_cells[c_idx], cs_id[0])
                else:
                    self.cells_cells[c_idx] = \
                        np.append(self.cells_cells[c_idx], cs_id[1])


    def divide_cell(self, c_idx, p_xy, v_xy):
        """
        Divides a cell by a line defined by the point p and vector v through p.
        Division of a cell has many side effects to the structures that
        describe nodes, cells, edges and walls and their incidence relations.
        All is described in the additional documentation.
        TODO: fix walls_nodes_all!!!
        """
        logger = logging.getLogger(__name__)
        logger.info('Dividing cell with idx = {0}'.format(c_idx))

        # ID of the cell to divide
        # TODO: will be phased out as soon as IDs disappear
        c_id = self.cells_id[c_idx]

        # =====================================================================
        # Find the two new nodes to be added: i.e. check each edge of the cell
        # for intersection with L, the line through p with direction vector v.
        # To keep things simple for now, exactly two points must be found.
        # Loop over the cell's walls (& edges) and test for intersection with L
        # The intersection points are called q0 and q1.
        qs_xy = []      # Coordinates of q0/1
        qs_edge = []    # Edges hit by the intersection line
        qs_wall = []    # Walls hit by the intersection line
        qs_nodes = []   # End nodes of the edges hit by the intersection line
        qs_cells = []   # Cells adjacent to C that are effected by the division
        for (w_id,c_jd) in zip(self.cells_walls[c_idx],self.cells_cells[c_idx]):
            w_idx = self.walls_idx[w_id]
            for e_idx in self.walls_edges[w_idx]:
                ns_id = self.edges_nodes[e_idx]
                ns_idx = [self.nodes_idx[n_id] for n_id in ns_id]
                n0_xy = self.nodes_xy[ns_idx[0]]
                n1_xy = self.nodes_xy[ns_idx[1]]
                # M = [ u_x, -v_x ]
                #     [ u_y, -v_y ]
                u_xy = n1_xy - n0_xy
                # TODO: as of now, I don't account for n[0,1] == q
                # This should be addressed by defining "attraction regions"
                # around each of the points. Some problematic corner cases can
                # arise though.
                M = np.array([u_xy, -v_xy]).T
                try:
                    # In the case that u is parallel to v the matrix M is
                    # singular, which means the current edge can be ignored
                    # since no intersection with that edge is possible.
                    st = npla.solve(M, p_xy - n0_xy)
                    eps = 1.0e-3
                    if abs(st[0]) < eps:
                        logger.debug('Intersection point is an existing node')
                    elif abs(1.0 - st[0]) < eps:
                        logger.debug('Intersection point is an existing node')
                    elif 0.0 < st[0] < 1.0:
                        # Intersection point q lies between n0 and n1, Good!
                        qs_xy.append(p_xy + st[1] * v_xy)
                        # Save q's neighbor nodes and incident edges & walls
                        qs_edge.append(e_idx)
                        qs_wall.append(w_id)
                        qs_nodes.append(ns_id)
                        qs_cells.append(c_jd)
                except npla.linalg.LinAlgError as err:
                    pass
                    # More rigorous specification of what error to ignore:
                    #if 'Singular matrix' not in err.message:
                        #raise
                    # else:
                        #pass

        logger.debug('Found {0} intersection points:'.format(len(qs_xy)))
        for q_idx in xrange(len(qs_xy)):
            s = 'q{0}: xy={1} on edge {2}, wall {3} with cell {4} between nodes {5}'
            logger.debug(s.format(q_idx, qs_xy[q_idx], qs_edge[q_idx], \
                                  qs_wall[q_idx], qs_cells[q_idx], \
                                  qs_nodes[q_idx]))

        # TODO: I've temporarily disabled the case w0 == w1
        if 2 == len(qs_xy) and qs_wall[0] != qs_wall[1]:
            # Two intersection points found on two different walls, proceed
            # with division
            logger.debug('Proceeding with division');

            # =================================================================
            # Shorthand notations for the IDs and index values of ...
            # ... the intersected edges and their nodes
            e0_id = qs_edge[0]
            e0_idx = e0_id
            e0_n0_id = qs_nodes[0][0]
            e0_n0_idx = self.nodes_idx[e0_n0_id]
            e0_n1_id = qs_nodes[0][1]
            e0_n1_idx = self.nodes_idx[e0_n1_id]
            # ...
            e1_id = qs_edge[1]
            e1_idx = e1_id
            e1_n0_id = qs_nodes[1][0]
            e1_n0_idx = self.nodes_idx[e1_n0_id]
            e1_n1_id = qs_nodes[1][1]
            e1_n1_idx = self.nodes_idx[e1_n1_id]
            #
            # ... the intersected walls and their nodes
            w0_id = qs_wall[0]
            w0_idx = self.walls_idx[w0_id]
            w0_n0_id = self.walls_nodes[w0_idx, 0]
            w0_n0_idx = self.nodes_idx[w0_n0_id]
            w0_n1_id = self.walls_nodes[w0_idx, 1]
            w0_n1_idx = self.nodes_idx[w0_n1_id]
            # ...
            w1_id = qs_wall[1]
            w1_idx = self.walls_idx[w1_id]
            w1_n0_id = self.walls_nodes[w1_idx, 0]
            w1_n0_idx = self.nodes_idx[w1_n0_id]
            w1_n1_id = self.walls_nodes[w1_idx, 1]
            w1_n1_idx = self.nodes_idx[w1_n1_id]
            #
            # ... the cells incident to the intersected walls w0 & w1
            c0_id = qs_cells[0]
            c1_id = qs_cells[1]
            # (note that either of those could be -1, this is handled later)

            # =================================================================
            # New IDs and index values for ...
            # ... the two new intersection nodes (points q0 & q1)
            q0_idx = self.num_nodes
            q1_idx = 1 + q0_idx
            q0_id = 1 + max(self.nodes_id)
            q1_id = 1 + q0_id
            self.nodes_id = np.append(self.nodes_id, [q0_id])
            self.nodes_id = np.append(self.nodes_id, [q1_id])
            self.nodes_idx[q0_id] = q0_idx
            self.nodes_idx[q1_id] = q1_idx
            #
            # ... the two new edges (q%) -- e%_new -> (e%_n1), % = 0 & 1
            e0_new_idx = self.num_edges
            e1_new_idx = 1 + e0_new_idx
            self.edges_idx = np.append(self.edges_idx, [e0_new_idx])
            self.edges_idx = np.append(self.edges_idx, [e1_new_idx])
            # ... and the new division edge (q0) -- e_div -> (q1)
            e_div_idx = 1 + e1_new_idx
            self.edges_idx = np.append(self.edges_idx, [e_div_idx])
            #
            # ... one new cell D (cfr.: 'daughter')
            d_idx = self.num_cells
            d_id = 1 + max(self.cells_id)
            self.cells_id = np.append(self.cells_id, [d_id])
            self.cells_idx[d_id] = d_idx
            #
            # ... three new walls (2 on the D cell, 1 div. wall on cells C & D)
            w0_new_idx = self.num_walls # Was part of w0, becomes new wall
            w1_new_idx = 1 + w0_new_idx # Was part of w1, becomes new wall
            w_div_idx = 1 + w1_new_idx # The 'dividing' wall
            w0_new_id = 1 + max(self.walls_id)
            w1_new_id = 1 + w0_new_id
            w_div_id = 1 + w1_new_id
            self.walls_id = np.append(self.walls_id, [w0_new_id])
            self.walls_id = np.append(self.walls_id, [w1_new_id])
            self.walls_id = np.append(self.walls_id, [w_div_id])
            self.walls_idx[w0_new_id] = w0_new_idx
            self.walls_idx[w1_new_id] = w1_new_idx
            self.walls_idx[w_div_id] = w_div_idx

            # =================================================================
            # First of all, find out which nodes of the original cell must be
            # assigned to which cell: mother or daughter. This determines the
            # orientation of many things. Hence this useful function:
            def left_of_q0_q1(n_xy):
                """
                Returns true when a point n_xy is on the left side of the 2D
                vector q0 -> q1, which means it's part of the mother cell.
                (i.e. look at the sign of the (2D) cross product of vector
                (q0 -> q1) with (q0 -> node).)
                """
                return np.cross(qs_xy[1] - qs_xy[0], n_xy - qs_xy[0]) > 0.0

            # IDs of the nodes on the left side of division line (q0 -> q1)
            # These will be the nodes of the mother cell C after division
            c_ns_id = [n_id for n_id in self.cells_nodes[c_idx]
                       if left_of_q0_q1(self.nodes_xy[self.nodes_idx[n_id]])
                      ]
            # IDs of the nodes on the right side of division line (q0 -> q1)
            # (= remaining nodes that are part of the new daughter cell D)
            d_ns_id = [n_id for n_id in self.cells_nodes[c_idx]
                       if n_id not in c_ns_id
                      ]

            logger.debug('Cell\'s nodes: {0}'.format(self.cells_nodes[c_idx]))
            logger.debug('Nodes {0} belong to the mother cell'.format(c_ns_id))
            logger.debug('Nodes {0} belong to the dghter cell'.format(d_ns_id))

            # Squeeze q0 & q1 in the list of nodes of mother and daughter cells
            #
            # Loop over pairs of nodes of the mother cell and insert [q0 q1]
            # (n_id is current node, m_id is next node, pos is the position
            # of n_id in cells_nodes[c_idx])
            for (n_id, m_id, pos) in zip(c_ns_id,
                                         np.roll(c_ns_id, -1),
                                         range(len(c_ns_id))):
                if n_id in qs_nodes[0] and m_id in qs_nodes[1]:
                    c_ns_id.insert(pos + 1, q0_id)
                    c_ns_id.insert(pos + 2, q1_id)

            # Loop over pairs of nodes of the daughter cell and insert [q1 q0]
            # (n_id is current node, m_id is next node, pos is the position
            # of n_id in cells_nodes[d_idx])
            for (n_id, m_id, pos) in zip(d_ns_id,
                                         np.roll(d_ns_id, -1),
                                         range(len(d_ns_id))):
                if n_id in qs_nodes[1] and m_id in qs_nodes[0]:
                    d_ns_id.insert(pos + 1, q1_id)
                    d_ns_id.insert(pos + 2, q0_id)

            logger.debug('Added intersection nodes to node lists')

            # Assign updated / new cells_nodes for C and D
            self.cells_nodes[c_idx] = np.array(c_ns_id)
            self.cells_nodes.append(np.array(d_ns_id))
            # ... and make sure cells_num_nodes is consistent for both
            self.cells_num_nodes[c_idx] = len(c_ns_id)
            self.cells_num_nodes = np.append(self.cells_num_nodes,
                                             len(d_ns_id))

            s = '{0} has {1} nodes: {2}'
            logger.debug(s.format('Mother', self.cells_num_nodes[c_idx], c_ns_id))
            logger.debug(s.format('Dghter', self.cells_num_nodes[d_idx], d_ns_id))

            # Find out which edges and walls lie on D's side of q0 -> q1.
            # IDs of the edges of the original cell C BEFORE division
            c_old_ws_id = self.cells_walls[c_idx]
            c_old_ws_idx = [self.walls_idx[w_id] for w_id in c_old_ws_id]
            c_old_es_id = [e_id for w_idx in c_old_ws_idx
                                    for e_id in self.walls_edges[w_idx]]

            # IDs of the walls / edges whose BOTH endnodes are in c/d_ns_id.
            # (i.e. walls / edges fully on the left/right side of q0 -> q1)
            # For walls, we need to EXCLUDE w0 and w1 to cover the case of the
            # division wall splitting w0 = w1 in two points (TODO: needs work)
            # TODO: profile this, it might be a hog
            c_ws_id = [w_id for w_id in self.cells_walls[c_idx] \
                       if set(self.walls_nodes[self.walls_idx[w_id],:]).issubset(set(c_ns_id)) \
                       and w_id not in [w0_id, w1_id]
                      ]
            c_es_id = [e_id for e_id in c_old_es_id \
                       if set(self.edges_nodes[e_id,:]).issubset(set(c_ns_id))
                      ]
            d_ws_id = [w_id for w_id in self.cells_walls[c_idx] \
                       if set(self.walls_nodes[self.walls_idx[w_id],:]).issubset(set(d_ns_id)) \
                       and w_id not in [w0_id, w1_id]
                      ]
            d_es_id = [e_id for e_id in c_old_es_id \
                       if set(self.edges_nodes[e_id,:]).issubset(set(d_ns_id))
                      ]

            logger.debug('Cell\'s edges: {0}'.format(c_old_es_id))
            logger.debug('Edges on mother cell\'s side: {0}'.format(c_es_id))
            logger.debug('Edges on dghter cell\'s side: {0}'.format(d_es_id))
            logger.debug('Cell\'s walls: {0}'.format(c_old_ws_idx))
            logger.debug('Walls on mother cell\'s side: {0}'.format(c_ws_id))
            logger.debug('Walls on dghter cell\'s side: {0}'.format(d_ws_id))

            # =================================================================
            # Nodes & Edges
            # Coordinates of the two new nodes are the intersection points q%
            self.nodes_xy = np.append(self.nodes_xy, [qs_xy[0]], axis=0)
            self.nodes_xy = np.append(self.nodes_xy, [qs_xy[1]], axis=0)

            # Both of the intersection edges e0 and e1 (denoted by e%) must be
            # split in two by inserting the node q% somewhere on the edge.
            #
            # Schematically, the situation:
            #   (e%_n0) -- e% -> (e%_n1)
            # becomes:
            #   (e%_n0) -- e% -> (q%) -- e%_new -> (e%_n1)
            #
            # Connect nodes to edges ==========================================
            # Replace e% by e%_new as incident edge of e%_n1
            self.nodes_edges[e0_n1_idx][e0_id == self.nodes_edges[e0_n1_idx]] \
                = e0_new_idx
            self.nodes_edges[e1_n1_idx][e1_id == self.nodes_edges[e1_n1_idx]] \
                = e1_new_idx
            # Connect new nodes q% to its 3 incident edges
            self.nodes_edges.append(np.array([e0_new_idx, e0_id, e_div_idx]))
            self.nodes_edges.append(np.array([e1_new_idx, e1_id, e_div_idx]))

            # Connect nodes to nodes ==========================================
            # (this could be done with post processing but all the info is here
            # anyway & things can be sped up by connecting nodes explicitly)
            # Replace e%_n1 by q% as incident node of e%_n0
            self.nodes_nodes[e0_n0_idx][e0_n1_id \
                                        == self.nodes_nodes[e0_n0_idx]] = q0_id
            self.nodes_nodes[e1_n0_idx][e1_n1_id \
                                        == self.nodes_nodes[e1_n0_idx]] = q1_id
            # Replace e%_n0 by q% as incident node of e%_n1
            self.nodes_nodes[e0_n1_idx][e0_n0_id \
                                        == self.nodes_nodes[e0_n1_idx]] = q0_id
            self.nodes_nodes[e1_n1_idx][e1_n0_id \
                                        == self.nodes_nodes[e1_n1_idx]] = q1_id
            # Connect new nodes q% to their 3 incident nodes
            self.nodes_nodes.append(np.array([e0_n1_id, e0_n0_id, q1_id]))
            self.nodes_nodes.append(np.array([e1_n1_id, e1_n0_id, q0_id]))

            # Connect edges to nodes ==========================================
            # Add new edges (q%) -- e%_new -> (e%_n1)
            self.edges_nodes = np.vstack([self.edges_nodes, [q0_id, e0_n1_id]])
            self.edges_nodes = np.vstack([self.edges_nodes, [q1_id, e1_n1_id]])
            # Add new edge (q0) -- e_div -> (q1)
            self.edges_nodes = np.vstack([self.edges_nodes, [q0_id, q1_id]])
            # Fix original edges e% to have q% as endpoint instead of e%_n1
            self.edges_nodes[e0_idx, 1] = q0_id
            self.edges_nodes[e1_idx, 1] = q1_id

            s = 'Replaced edge: ({0}) -- {1} -> ({2}) with ({3}) -- {4} -> ({5}) -- {6} -> ({7})'
            logger.debug(s.format(e0_n0_idx, e0_idx, e0_n1_idx, e0_n0_idx, \
                                  e0_idx, q0_idx, e0_new_idx, e0_n1_idx))
            logger.debug(s.format(e1_n0_idx, e1_idx, e1_n1_idx, e1_n0_idx, \
                                  e1_idx, q1_idx, e1_new_idx, e1_n1_idx))

            # Determine edges_cells for all e%_new and e% by looking whether
            # e%_n0 is a node of C or D
            #
            # TODO: ASCII sketches of the orientations!!!
            #
            # Edge e0:
            if e0_n0_id in c_ns_id:
                # e0 connects C with C0
                self.edges_cells[e0_idx, :] = [c_id, c0_id]
                # e0_new connects D with C0
                self.edges_cells = np.vstack([self.edges_cells, [d_id, c0_id]])
            else:
                # e0 connects C0 with D
                self.edges_cells[e0_idx, :] = [c0_id, d_id]
                # e0_new connects C0 with C
                self.edges_cells = np.vstack([self.edges_cells, [c0_id, c_id]])
            #
            # Edge e1:
            if e1_n0_id in c_ns_id:
                # e1 connects C1 with C
                self.edges_cells[e1_idx, :] = [c1_id, c_id]
                # e1_new connects C1 with D
                self.edges_cells = np.vstack([self.edges_cells, [c1_id, d_id]])
            else:
                # e1 connects D with C1
                self.edges_cells[e1_idx, :] = [d_id, c1_id]
                # e1_new connects C with C1
                self.edges_cells = np.vstack([self.edges_cells, [c_id, c1_id]])

            # The new edges e%_new are contained within the new walls w% since
            # walls and edges within walls have the same orientation w.r.t.
            # the cells / nodes they're incident with
            # (e% are still part of w%, that's why they don't need to be fixed)
            self.edges_walls = np.append(self.edges_walls, [w0_new_id])
            self.edges_walls = np.append(self.edges_walls, [w1_new_id])

            # The division edge is incident with cell C and D:
            # C is on the left of q0 -> q1, D is on the right.
            self.edges_cells = np.vstack([self.edges_cells, [c_id, d_id]])
            # The div. edge is part of the new division wall.
            self.edges_walls = np.append(self.edges_walls, [w_div_id])

            # Fix edges_walls for all edges that must belong to w%_new
            # Traverse the list of edges starting from the edge beyond e% and
            # tag these as belonging to w%_new
            w0_old_es_id = self.walls_edges[w0_idx].tolist()
            for e_id in w0_old_es_id[(w0_old_es_id.index(e0_idx) + 1):]:
                self.edges_walls[e_id] = w0_new_id
            w1_old_es_id = self.walls_edges[w1_idx].tolist()
            for e_id in w1_old_es_id[(w1_old_es_id.index(e1_idx) + 1):]:
                self.edges_walls[e_id] = w1_new_id

            # One last step for the edges:
            # Loop over ALL edges that are entirely on the right side of
            # q0 -> q1 (are part of D) and switch their neighbor from C to D.
            for e_id in d_es_id:
                e_idx = e_id
                self.edges_cells[e_idx,
                                 c_id == self.edges_cells[e_idx, :]] = d_id

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # All 'nodes_*' arrays are ok at this point.
            # All 'edges_*' arrays are ok at this point.
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            # =================================================================
            # Walls
            # Both of the intersection walls w0 and w1 (denoted by w%) must be
            # split in two by inserting the node q% somewhere on the wall.
            #
            # Schematically, the situation:
            #   (w%_n0) -- w% -> (w%_n1)
            # becomes:
            #   (w%_n0) -- w% -> (q%) -- w%_new -> (w%_n1)
            #
            # Special case: w0 == w1
            #if w0_id == w1_id:
                #print ('Division wall splits one wall: {0}').format(w0_id)
                ## Find out whether traversing the wall w0 from w0_n0 to w0_n1
                ## we first meet q0 or q1 by looking at which of the intersected
                ## edges e0 or e1 appears first in walls_edges[w0]. This works
                ## b/c walls_edges are ordered from n0 to n1.
                ##
                #if w0_old_es_id.index(e0_idx) < w0_old_es_id.index(e1_idx):
                    ## e0 (and therefore q0) is passed first
                    #print 'Case A'
                    ## In the first case the situation becomes:
                    ##                     / -- w_div -> \
                    ## (w0_n0) -- w0 -> (q0) -- w0_new -> (q1) -- w1_new -> (w1_n1)
                    ##
                    ## Add new walls w%_new
                    #self.walls_nodes = np.vstack([self.walls_nodes,
                                                  #[q0_id, q1_id]])
                    #self.walls_nodes = np.vstack([self.walls_nodes,
                                                  #[q1_id, w1_n1_id]])
                    ## Fix original wall w0 to have q0 as endpoint (was w0_n1)
                    #self.walls_nodes[w0_idx, 1] = q0_id
                #else:
                    ## e1 (and therefore q1) is passed first
                    #print 'Case B'
                    ## In the other case the situation becomes:
                    ##                     / <- w_div -- \
                    ## (w0_n0) -- w0 -> (q1) -- w0_new -> (q0) -- w1_new -> (w1_n1)
            #else:
                #pass
            # Add new walls (q%) -- w%_new -> (w%_n1)
            self.walls_nodes = np.vstack([self.walls_nodes,
                                          [q0_id, w0_n1_id]])
            self.walls_nodes = np.vstack([self.walls_nodes,
                                          [q1_id, w1_n1_id]])
            # Fix original walls w% to have q% as endpoint instead of w%_n1
            self.walls_nodes[w0_idx, 1] = q0_id
            self.walls_nodes[w1_idx, 1] = q1_id

            # Edges of w0_new are the 'second half' edges of the original w0
            # after e0 (plus e0_new in front)
            w0_new_es_id = [e0_new_idx] \
                         + w0_old_es_id[(w0_old_es_id.index(e0_idx) + 1):]
            # Edges of w0 are the 'first half' edges of the original w0 before
            # (and including) e0
            w0_es_id = w0_old_es_id[:(w0_old_es_id.index(e0_idx) + 1)]

            # Edges of w1_new are the 'second half' edges of the original w1
            # after e1 (plus e1_new in front)
            w1_new_es_id = [e1_new_idx] \
                         + w1_old_es_id[(w1_old_es_id.index(e1_idx) + 1):]
            # Edges of w1 are the 'first half' edges of the original w1 before
            # (and including) e1
            w1_es_id = w1_old_es_id[:(w1_old_es_id.index(e1_idx) + 1)]

            # Update / extend walls_edges with edge lists created above
            self.walls_edges[w0_idx] = np.array(w0_es_id)
            self.walls_edges[w1_idx] = np.array(w1_es_id)
            self.walls_edges.append(np.array(w0_new_es_id))
            self.walls_edges.append(np.array(w1_new_es_id))

            # NOTE that all previous manipulations preserve the order of edges
            # within walls and their orientation.

            # walls_cells for all w%_new and w% is the same as edges_cells of
            # their corresponding edges.
            # (b/c walls and edges have the same orientation)
            self.walls_cells[w0_idx, :] = self.edges_cells[e0_idx, :]
            self.walls_cells[w1_idx, :] = self.edges_cells[e1_idx, :]
            self.walls_cells = np.vstack([self.walls_cells,
                                          self.edges_cells[e0_new_idx, :]])
            self.walls_cells = np.vstack([self.walls_cells,
                                          self.edges_cells[e1_new_idx, :]])

            # Create the division wall which connects nodes q0 and q1
            # Add new wall (q0) -- w_div -> (q1) connecting cells C and D.
            # The div. wall also contains the division edge.
            self.walls_nodes = np.vstack([self.walls_nodes, [q0_id, q1_id]])
            self.walls_cells = np.vstack([self.walls_cells, [c_id, d_id]])
            self.walls_edges.append(np.array([e_div_idx]))

            # One last step for the walls (analogous to edges).
            # Loop over all walls that are entirely on the right side of
            # q0 -> q1 and switch their neighbor from C to D.
            # (I could do this by looking at edges_cells of the walls as well)
            for w_id in d_ws_id:
                w_idx = self.walls_idx[w_id]
                self.walls_cells[w_idx, c_id == self.walls_cells[w_idx, :]] \
                    = d_id

            # Make sure walls_nodes_all is updated for C and extended for D
            # TODO

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # All 'walls_*' arrays are ok at this point.
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            # =================================================================
            # Cells
            # TODO: better comment...
            c_ws_id.append(w_div_id)
            d_ws_id.append(w_div_id)

            if w0_n0_id in c_ns_id:
                c_ws_id.append(w0_id)
                d_ws_id.append(w0_new_id)
            elif w0_n0_id in d_ns_id:
                c_ws_id.append(w0_new_id)
                d_ws_id.append(w0_id)
            else: raise Exception('TODO')

            if w1_n0_id in c_ns_id:
                c_ws_id.append(w1_id)
                d_ws_id.append(w1_new_id)
            elif w1_n0_id in d_ns_id:
                c_ws_id.append(w1_new_id)
                d_ws_id.append(w1_id)
            else: raise Exception('TODO')
                
            # Update / extend cells_walls with the extended [c/d]_ws_id lists
            self.cells_walls[c_idx] = np.array(c_ws_id)
            self.cells_walls.append(np.array(d_ws_id))
            # Make sure cells_num_walls is consistent for both C and D
            self.cells_num_walls[c_idx] = len(self.cells_walls[c_idx])
            self.cells_num_walls = np.append(self.cells_num_walls,
                                             len(self.cells_walls[d_idx]))

            # Update cells c0 and c1 which are adjacent to the edges e0 and e1
            # being divided. Both c0 and c1 get a new wall w0_new resp. w1_new
            # and a new neighbor cell, d.
            # In both cases their lists of nodes in cells_nodes must be updated
            # to include the division points q0 and q1.
            # (Note: only do this for normal cells, ignore if ID = -1)
            if -1 != c0_id:
                c0_idx = self.cells_idx[c0_id]
                self.cells_walls[c0_idx] = np.append(self.cells_walls[c0_idx],
                                                     w0_new_id)
                self.cells_num_walls[c0_idx] += 1

                # Verify this: cells_nodes[c0_idx] += q0 between e0_n0 and e0_n1
                c0_ns_id = self.cells_nodes[c0_idx].tolist()
                for (n_id, m_id, pos) in zip(c0_ns_id,
                                             np.roll(c0_ns_id, -1),
                                             range(len(c0_ns_id))):
                    if [n_id, m_id] == [e0_n0_id, e0_n1_id] \
                        or [n_id, m_id] == [e0_n1_id, e0_n0_id]:
                        c0_ns_id.insert(pos + 1, q0_id)
                self.cells_nodes[c0_idx] = np.array(c0_ns_id)
                self.cells_num_nodes[c0_idx] = len(c0_ns_id)

            if -1 != c1_id:
                c1_idx = self.cells_idx[c1_id]
                self.cells_walls[c1_idx] = np.append(self.cells_walls[c1_idx],
                                                     w1_new_id)
                self.cells_num_walls[c1_idx] += 1

                # Verify this: cells_nodes[c1_idx] += q1 between e1_n0 and e1_n1
                c1_ns_id = self.cells_nodes[c1_idx].tolist()
                for (n_id, m_id, pos) in zip(c1_ns_id,
                                             np.roll(c1_ns_id, -1),
                                             range(len(c1_ns_id))):
                    if [n_id, m_id] == [e1_n0_id, e1_n1_id] \
                        or [n_id, m_id] == [e1_n1_id, e1_n0_id]:
                        c1_ns_id.insert(pos + 1, q1_id)
                self.cells_nodes[c1_idx] = np.array(c1_ns_id)
                self.cells_num_nodes[c1_idx] = len(c1_ns_id)

            # Now we can safely say we've added nodes / edges / cells & walls
            self.num_nodes += 2
            self.num_edges += 3
            self.num_cells += 1
            self.num_walls += 3

            # It is easier to extract cell cell connectivity from walls instead
            # of explicitly setting cell neighbors. It is a bit slower though.
            self.cache_cell_neighbors()

            # Extend all attributes for all entities accordingly, default to 0
            for attr_name in self.nodes_attributes:
                self.nodes_attributes[attr_name] = \
                    np.append(self.nodes_attributes[attr_name], [0.0, 0.0])
            for attr_name in self.edges_attributes:
                self.edges_attributes[attr_name] = \
                    np.append(self.edges_attributes[attr_name], [0.0, 0.0, 0.0])
            for attr_name in self.cells_attributes:
                self.cells_attributes[attr_name] = \
                    np.append(self.cells_attributes[attr_name], [0.0])
            for attr_name in self.walls_attributes:
                self.walls_attributes[attr_name] = \
                    np.append(self.walls_attributes[attr_name], [0.0, 0.0, 0.0])

            # Return IDs of the affected and new entities for further handling
            return (q0_id, q1_id,       # two new nodes q0_id and q1_id \
                    e0_id, e0_new_idx,  # old edge e0 and its new part e0_new \
                    e1_id, e1_new_idx,  # old edge e1 and its new part e1_new \
                    e_div_idx,          # new division edge q0 -> q1 \
                    w0_id, w0_new_id,   # old wall w0 and its new part w0_new \
                    w1_id, w1_new_id,   # old wall w1 and its new part w1_new \
                    w_div_id,           # new division wall q0 -> q1 \
                    c_id, d_id)         # mother and daughter cells
        else:
            logger.debug('I need exactly 2 intersection points to proceed')
            raise Exception('Error in cell division, bailing out')

    def split_edge(self, e_id):
        """
        Splits an edge e_id in the middle by inserting a new node.
        Returns the tuple:
            (ID of the divided edge: n0 -> q,
             ID of the new edge: q -> n1,
             ID of the new node: q)
        """
        # Edge ID and index are equivalent for now.
        e_idx = e_id

        # =====================================================================
        # Shorthand notations for ...
        # ... the nodes of this edge
        n0_id = self.edges_nodes[e_idx, 0]
        n1_id = self.edges_nodes[e_idx, 1]
        n0_idx = self.nodes_idx[n0_id]
        n1_idx = self.nodes_idx[n1_id]
        n0_xy = self.nodes_xy[self.nodes_idx[n0_id]]
        n1_xy = self.nodes_xy[self.nodes_idx[n1_id]]
        # ... the wall this edge is part of
        w_id = self.edges_walls[e_idx]
        w_idx = self.walls_idx[w_id]
        # ... the cells incident to this edge
        # (note that either of those could be -1, this is handled later)
        c0_id = self.edges_cells[e_idx, 0]
        c1_id = self.edges_cells[e_idx, 1]

        # New ID / index for the new node q
        q_idx = self.num_nodes
        q_id = 1 + max(self.nodes_id)
        self.nodes_id = np.append(self.nodes_id, [q_id])
        self.nodes_idx[q_id] = q_idx
        # ... and for the new edge
        e_new_idx = self.num_edges
        e_new_id = e_new_idx
        self.edges_idx = np.append(self.edges_idx, [e_new_idx])

        # q lies in the middle of the edge, set its coordinates accordingly
        q_xy = 0.5 * (n0_xy + n1_xy)
        self.nodes_xy = np.append(self.nodes_xy, [q_xy], axis=0)

        # Situation was:
        #        c0
        # [n0] --'e'-> [n1]
        #        c1
        #
        # Becomes: (note that e_new is always on n1's side)
        #              c0
        # [n0] --'e'-> [q] --'e_new'-> [n1]
        #              c1
        # Replace e by e_new as incident edge of n1
        self.nodes_edges[n1_idx][e_id == self.nodes_edges[n1_idx]] = e_new_idx
        # Connect new node q to its 2 incident edges and nodes
        # (in the right order)
        self.nodes_edges.append(np.array([e_id, e_new_id]))
        self.nodes_nodes.append(np.array([n0_id, n1_id]))

        # Add the new edge e_new:
        self.edges_nodes = np.vstack([self.edges_nodes, [q_id, n1_id]])
        self.edges_cells = np.vstack([self.edges_cells, [c0_id, c1_id]])
        # The new edge e_new is contained within the same wall as edge e
        self.edges_walls = np.append(self.edges_walls, [w_id])
        # 
        # Fix original edge e to have q as endpoint instead of n1
        self.edges_nodes[e_idx, n1_id == self.edges_nodes[e_idx, :]] = q_id
        # Replace n1/0 by q as incident node of n0/1
        self.nodes_nodes[n0_idx][n1_id == self.nodes_nodes[n0_idx]] = q_id
        self.nodes_nodes[n1_idx][n0_id == self.nodes_nodes[n1_idx]] = q_id

        # Make sure cells c0 and c1 have their node lists updated to include
        # the new node q between nodes n0 and n1 (iff their cell ID is not -1).
        # Since the orientation is fixed we know c0 has nodes:  ... n0 n1 ...
        # and c1 nodes: ... n1 n0 ...
        # Therefore: in c0 q must be insterted BEFORE n1
        #            in c1 q must be insterted BEFORE n0
        # (doing this also works in case of 'wrap around' between n0 and n1)
        # Also, the number of nodes must be increased in both cells
        # (Note that using python lists seems to be faster than numpy arrays)
        if -1 != c0_id:
            c0_idx = self.cells_idx[c0_id]
            c0_ns_id = self.cells_nodes[c0_idx].tolist()
            c0_ns_id.insert(c0_ns_id.index(n1_id), q_id)
            self.cells_nodes[c0_idx] = np.array(c0_ns_id)
            self.cells_num_nodes[c0_idx] = len(c0_ns_id)
        if -1 != c1_id:
            c1_idx = self.cells_idx[c1_id]
            c1_ns_id = self.cells_nodes[c1_idx].tolist()
            c1_ns_id.insert(c1_ns_id.index(n0_id), q_id)
            self.cells_nodes[c1_idx] = np.array(c1_ns_id)
            self.cells_num_nodes[c1_idx] = len(c1_ns_id)

        # Add the new edge to the wall it's part of; ie: the same wall as e
        self.walls_edges[w_idx] = np.append(self.walls_edges[w_idx], e_new_id)

        # Now we can safely say we've added one node and one edge
        self.num_nodes += 1
        self.num_edges += 1

        # Extend all attributes for nodes & edges, default to 0
        for attr_name in self.nodes_attributes:
            self.nodes_attributes[attr_name] = \
                np.append(self.nodes_attributes[attr_name], [0.0])
        for attr_name in self.edges_attributes:
            self.edges_attributes[attr_name] = \
                np.append(self.edges_attributes[attr_name], [0.0])

        # Return: the old edge ID, the new edge ID and the new node ID
        return (e_id, e_new_id, q_id)

    def update_boundary_polygon(self):
        """
        Some algorithms require the use of the tissue perimeter called
        "boundary polygon" which is essentially defined by the IDs of the nodes
        that make up that perimeter ordered CW (as oppsed to cells_nodes which
        are CCW). This function recalculates the boundary polygon nodes by
        looping over the exterior walls and ordering them. It also updates the
        corresponding boundary polygon walls.
        After calling this function, the self object has either newly created
        or updated members 'bp_nodes' and 'bp_walls'.
        NOTE: VirtualLeaf orders its BP nodes but does NOT order the BP walls
              whereas this code does both. So don't expect both codes to give
              identical results :-).
        """
        logger = logging.getLogger(__name__)
        # Get all exterior walls
        ext_ws_idx = [w_idx for w_idx in xrange(self.num_walls)
                      if -1 in self.walls_cells[w_idx]]

        # Catch the case of the empty tissue
        if len(ext_ws_idx) == 0:
            self.bp_nodes = []
            self.bp_walls = []
        else:
            # This dict maps the idx of one node (head) in a wall to a tuple
            # containing the other nodes (tail) in that wall and the wall's
            # idx.  The orientation of the nodes in each wall is checked to be
            # consistent with the clockwise ordering of nodes in the boundary
            # polygon. This structure is used basically for piecing walls
            # together in the correct order in (hopefully) linear time using a
            # hashmap.
            successor = {}
            for w_idx in ext_ws_idx:
                # All nodes of current wall
                w_nodes = self.walls_nodes_all[w_idx]
                # Check wall orientation: Since the orientation of cells &
                # nodes in a wall is like this:
                #     n_1
                # c_0  |  c_1
                #     n_0
                # it follows that if c_0 == -1 then n_0 comes before n_1 in the
                # boundary polygon nodes. If c_1 == -1, the order of the two
                # nodes in the boundary polygon is reversed.
                if self.walls_cells[w_idx,0] == -1:
                    successor[w_nodes[0]] = (w_nodes[1:], w_idx)
                else:
                    successor[w_nodes[-1]] = (w_nodes[-2::-1], w_idx)

            # Assembling the boundary polygon is just a matter of running
            # through the successor dict and using the tail's last node as key
            # for the next tail while appending the tails & visited walls.
            # Start with some random first node
            (head, (tail, w_idx)) = successor.iteritems().next()
            self.bp_nodes = [head] # First node of the BP
            self.bp_walls = [w_idx] # First wall of the BP
            while tail[-1] != head:
                # Add the tail nodes of the wall to the BP
                self.bp_nodes.extend(tail)
                # The next head node is the last element of the tail
                (tail, w_idx) = successor[tail[-1]]
                # The wall made of (head, tail...) nodes
                self.bp_walls.append(w_idx)
            # Make sure the last piece of tail is added too, excluding its last
            # node, which is by construction the head of the BP.
            self.bp_nodes.extend(tail[:-1])

            logger.info('Boundary polygon nodes & walls updated')

    def save(self, tissue_file_name, step_idx, step_time, overwrite=False):
        """
        Saves the current state of the Tissue inside the provided vleaf file
        'tissue_file_name' under the specified 'step_idx' with time 'step_time'
        in seconds.
        """
        logger = logging.getLogger(__name__)
        # The name of the HDF5 group that will be created to contain all of the
        # current step
        step_grp_name = ('/step_{0}').format(step_idx)

        logger.info('Saving tissue to file \'{0}\' as \'{1}\''.format(tissue_file_name, step_grp_name))
        # Read / write if exists, create otherwise
        tissue_file = h5py.File(tissue_file_name, 'a')

        # If the '/step_n' group to be written exists already, bail out
        overwrite_existing_step = False
        if step_grp_name in tissue_file:
            if not overwrite:
                logger.warning('\'{0}\' already exists in \'{1}\', ignoring save request!'.format(step_grp_name, tissue_file_name))
                return
            else:
                overwrite_existing_step = True
                logger.warning('\'{0}\' already exists in \'{1}\', overwriting!'.format(step_grp_name, tissue_file_name))
                # Remove existing group
                del tissue_file[step_grp_name]

        # ======================================================================
        # Write time steps:
        #   /time_steps                 Time step values in seconds
        #   /time_steps_idx             Indices of time steps, refer to n in '/step_n'

        if 'time_steps' in tissue_file:
            # Extend existing '/time_steps' dataset with new step
            time_steps_dset = tissue_file['time_steps']
            time_steps = time_steps_dset[...] # Read data
            if overwrite_existing_step:
                time_steps[step_idx] = step_time
            else:
                time_steps = np.append(time_steps, step_time) # Append time step
                time_steps_dset.resize(time_steps.shape) # Resize dataset
            time_steps_dset[...] = time_steps # Write new data to bigger dataset
        else:
            # Write a new extendable '/time_steps' dataset with one element
            time_steps_dset = tissue_file.create_dataset('time_steps',
                                                         (1,),
                                                         np.float64,
                                                         maxshape=(None,))
            time_steps_dset[...] = np.array([step_time])

        if 'time_steps_idx' in tissue_file:
            if not overwrite_existing_step:
                # Extend existing '/time_steps_idx' dataset with new step
                time_steps_idx_dset = tissue_file['time_steps_idx']
                time_steps_idx = time_steps_idx_dset[...] # Read data
                time_steps_idx = np.append(time_steps_idx, step_idx) # Append time step
                time_steps_idx_dset.resize(time_steps_idx.shape) # Resize dataset
                time_steps_idx_dset[...] = time_steps_idx # Write new data to bigger dataset
        else:
            # Write a new extendable '/time_steps_idx' dataset with one element
            time_steps_idx_dset = tissue_file.create_dataset('time_steps_idx',
                                                             (1,),
                                                             np.int32,
                                                             maxshape=(None,))
            time_steps_idx_dset[...] = np.array([step_idx])

        # Create /step_n group where all data will be stored
        step_grp = tissue_file.create_group(step_grp_name)

        # ======================================================================
        # Write nodes:
        #   /step_n/nodes_id            The IDs of all nodes
        #           nodes_xy            XY coordinates of all nodes
        #           nodes_attr_*        node-based attribute values

        # /step_n/nodes_id
        nodes_id_dset = step_grp.create_dataset('nodes_id',
                                                self.nodes_id.shape,
                                                np.int32)
        nodes_id_dset[...] = self.nodes_id

        # Optionally, 3D coordinates
        # /step_n/nodes_xyz
        if hasattr(self, 'nodes_xyz'):
            nodes_xyz_dset = step_grp.create_dataset('nodes_xyz',
                                                    self.nodes_xyz.shape,
                                                    np.float64)
            nodes_xyz_dset[...] = self.nodes_xyz
        else:
            # /step_n/nodes_xy
            nodes_xy_dset = step_grp.create_dataset('nodes_xy',
                                                    self.nodes_xy.shape,
                                                    np.float64)
            nodes_xy_dset[...] = self.nodes_xy

        # /step_n/nodes_attr_*
        for attr_name, attr_values in self.nodes_attributes.iteritems():
            if attr_values.dtype.kind in ['i', 'f']:
                # Numerical types can be written directly to HDF5
                attr_dset = step_grp.create_dataset(('nodes_attr_{0}').format(attr_name),
                                                    attr_values.shape,
                                                    attr_values.dtype)
                attr_dset[...] = attr_values
            elif attr_values.dtype.kind == 'S':
                # String types need a variable length string dtype for HDF5
                attr_dset = step_grp.create_dataset(('nodes_attr_{0}').format(attr_name),
                                                    dtype=h5py.special_dtype(vlen=str),
                                                    data=attr_values)
            else:
                # Other types are not supported
                print '\' nodes_attr_' + attr_name + \
                    '\': ignored; usupported data type.'

        # ======================================================================
        # Write cells:
        #   /step_n/cells_id            The IDs of all cells
        #           cells_num_nodes     How many nodes each cell has
        #           cells_nodes         IDs of the nodes of all cells
        #           cells_num_walls     How many walls each cell has
        #           cells_walls         IDs of the walls of all cells
        #           cells_attr_*        Cell-based attribute values

        # /step_n/cells_id
        cells_id_dset = step_grp.create_dataset('cells_id',
                                                self.cells_id.shape,
                                                np.int32)
        cells_id_dset[...] = self.cells_id

        # /step_n/cells_num_nodes
        cells_num_nodes_dset = step_grp.create_dataset('cells_num_nodes',
                                                       self.cells_num_nodes.shape,
                                                       np.int32)
        cells_num_nodes_dset[...] = self.cells_num_nodes
        
        # /step_n/cells_nodes
        # Remark: cells_nodes is saved as a full 2D array. Therefore, the
        # existing data in Tissue.cells_nodes needs to be embedded in a full
        # 2D numpy array first before saving to HDF5. Padding value -1 is used.
        cells_nodes_data = -np.ones([self.num_cells, max(self.cells_num_nodes)])
        for c_idx in self.cells_idx:
            cells_nodes_data[c_idx, :self.cells_num_nodes[c_idx]] \
                = self.cells_nodes[c_idx]
        cells_nodes_dset = step_grp.create_dataset('cells_nodes',
                                                   cells_nodes_data.shape,
                                                   np.int32)
        cells_nodes_dset[...] = cells_nodes_data

        # /step_n/cells_num_walls
        cells_num_walls_dset = step_grp.create_dataset('cells_num_walls',
                                                       self.cells_num_walls.shape,
                                                       np.int32)
        cells_num_walls_dset[...] = self.cells_num_walls

        # /step_n/cells_walls
        # Remark: cells_walls is saved as a full 2D array. Therefore, the
        # existing data in Tissue.cells_walls needs to be embedded in a full
        # 2D numpy array first before saving to HDF5. Padding value -1 is used.
        cells_walls_data = -np.ones([self.num_cells, max(self.cells_num_walls)])
        for c_idx in self.cells_idx:
            cells_walls_data[c_idx, :self.cells_num_walls[c_idx]] \
                = self.cells_walls[c_idx]
        cells_walls_dset = step_grp.create_dataset('cells_walls',
                                                   cells_walls_data.shape,
                                                   np.int32)
        cells_walls_dset[...] = cells_walls_data

        # /step_n/cells_attr_*
        for attr_name, attr_values in self.cells_attributes.iteritems():
            if attr_values.dtype.kind in ['i', 'f']:
                # Numerical types can be written directly to HDF5
                attr_dset = step_grp.create_dataset(('cells_attr_{0}').format(attr_name),
                                                    attr_values.shape,
                                                    attr_values.dtype)
                attr_dset[...] = attr_values
            elif attr_values.dtype.kind == 'S':
                # String types need a variable length string dtype for HDF5
                attr_dset = step_grp.create_dataset(('cells_attr_{0}').format(attr_name),
                                                    dtype=h5py.special_dtype(vlen=str),
                                                    data=attr_values)
            else:
                # Other types are not supported
                print '\' cells_attr_' + attr_name + \
                    '\': ignored; usupported data type.'

        # =====================================================================
        # Write the boundary polygon:
        #   /step_n/bp_nodes            IDs of nodes in the boundary polygon
        #           bp_walls            IDs of walls in the boundary polygon

        # /step_n/bp_nodes
        bp_nodes_dset = step_grp.create_dataset('bp_nodes',
                                                (len(self.bp_nodes),),
                                                np.int32)
        # Save inverted list of bp nodes since VL expects it that way
        bp_nodes_dset[...] = self.bp_nodes[::-1]

        # /step_n/bp_walls
        bp_walls_dset = step_grp.create_dataset('bp_walls',
                                                (len(self.bp_walls),),
                                                np.int32)
        # Save inverted list of bp walls to be consistent with the nodes
        # (VirtualLeaf does not require ordered walls but I do it anyway)
        bp_walls_dset[...] = self.bp_walls[::-1]

        # =====================================================================
        # Write walls:
        #   /step_n/walls_id            The IDs of all walls
        #           walls_cells         IDs of the cells connected by walls
        #           walls_nodes         IDs of the end nodes of walls
        #           walls_attr_*        Wall-based attribute values

        # /step_n/walls_id
        walls_id_dset = step_grp.create_dataset('walls_id',
                                                self.walls_id.shape,
                                                np.int32)
        walls_id_dset[...] = self.walls_id

        # /step_n/walls_cells
        walls_cells_dset = step_grp.create_dataset('walls_cells',
                                                self.walls_cells.shape,
                                                np.int32)
        walls_cells_dset[...] = self.walls_cells

        # /step_n/walls_nodes
        walls_nodes_dset = step_grp.create_dataset('walls_nodes',
                                                self.walls_nodes.shape,
                                                np.int32)
        walls_nodes_dset[...] = self.walls_nodes

        # /step_n/walls_attr_*
        for attr_name, attr_values in self.walls_attributes.iteritems():
            if attr_values.dtype.kind in ['i', 'f']:
                # Numerical types can be written directly to HDF5
                attr_dset = step_grp.create_dataset(('walls_attr_{0}').format(attr_name),
                                                    attr_values.shape,
                                                    attr_values.dtype)
                attr_dset[...] = attr_values
            elif attr_values.dtype.kind == 'S':
                # String types need a variable length string dtype for HDF5
                attr_dset = step_grp.create_dataset(('walls_attr_{0}').format(attr_name),
                                                    dtype=h5py.special_dtype(vlen=str),
                                                    data=attr_values)
            else:
                # Other types are not supported
                print '\' walls_attr_' + attr_name + \
                    '\': ignored; usupported data type.'

        # In the case the tissue has an attribute called 'attributes' that is a
        # dictionary with global tissue attributes it will be saved to HDF5 as
        # named attributes of the /step_n group in the HDF5 file.
        # This attribute is used mainly for compatibility with Virtual Leaf
        # since VL requires two following attributes:
        # - parameters: xml tree that holds the model parameters used for the
        #               current step of the tissue
        # - random_engine: xml tree representing the state of the random number
        #                  generator engine at the current step of the tissue
        if hasattr(self, 'attributes'):
            if isinstance(self.attributes, dict):
                logger.info('Saving tissue attributes: {0}'.format(self.attributes.keys()))
                for (name, value) in self.attributes.iteritems():
                    step_grp.attrs[name] = str(value)
            else:
                logger.warning('Tissue attributes must be stored in a dict!')

        # We're done writing, close the HDF5 file with tissue data
        tissue_file.close()

    def print_info(self):
        """
        Prints full tissue structure to the screen, including post-procesed
        information about incidence of entities.
        """
        print ('===[ NODES ({0}) ]===').format(self.num_nodes)
        nodes_fmt_str = '{0:5}{1:5}{2:16}{3:16}  {4}  {5}'
        print (nodes_fmt_str).format('idx', 'ID', 'X', 'Y', 'n-n', 'n-e')
        for n_idx in self.nodes_idx:
            print (nodes_fmt_str).format(self.nodes_idx[n_idx],
                                         self.nodes_id[n_idx],
                                         self.nodes_xy[n_idx,0],
                                         self.nodes_xy[n_idx,1],
                                         self.nodes_nodes[n_idx],
                                         self.nodes_edges[n_idx])

        print ('===[ CELLS ({0}) ]===').format(self.num_cells)
        cells_fmt_str = '{0:5}{1:5}  {2}  {3}  {4}  {5}  {6}'
        print (cells_fmt_str).format('idx', 'ID', '#nodes', 'c-n', '#walls', 
                                     'c-w', 'c-c')
        for c_idx in self.cells_idx:
            print (cells_fmt_str).format(self.cells_idx[c_idx],
                                         self.cells_id[c_idx],
                                         self.cells_num_nodes[c_idx],
                                         self.cells_nodes[c_idx],
                                         self.cells_num_walls[c_idx],
                                         self.cells_walls[c_idx],
                                         self.cells_cells[c_idx])

        print ('===[ WALLS ({0}) ]===').format(self.num_walls)
        walls_fmt_str = '{0:5}{1:5}  {2}  {3}'
        print (walls_fmt_str).format('idx', 'ID', 'w-n', 'w-c')
        for w_idx in self.walls_idx:
            print (walls_fmt_str).format(self.walls_idx[w_idx],
                                         self.walls_id[w_idx],
                                         self.walls_nodes[w_idx, :],
                                         self.walls_cells[w_idx, :])

        print ('===[ EDGES ({0}) ]===').format(self.num_edges)
        edges_fmt_str = '{0:5}  {1}  {2}  {3}'
        print (edges_fmt_str).format('idx', 'e-n', 'e-w', 'e-c')
        for e_idx in self.edges_idx:
            print (edges_fmt_str).format(self.edges_idx[e_idx],
                                         self.edges_nodes[e_idx, :],
                                         self.edges_walls[e_idx],
                                         self.edges_cells[e_idx, :])

class TissueSeries:
    """
    Serves as a wrapper around loading simulation steps from tissue files. 
    Upon construction a TissueSeries object contains the following properties:
        file_name: The name of the tissue file associated with the object
        t: Dictionary of Tissue objects. Keys are time step index values
        time_steps: Array-like of available time steps
        time_steps_idx: Array-like of available time step indices
    """
    def __init__(self, file_name=None, precache_all=False):
        """
        Associates a tissue series object with the given file. Optionally all
        the steps inside the file can be loaded / precached. This can get slow
        for large files. Steps are saved in a dict (keys: time step indices,
        values: tissues).
        """
        self.file_name = file_name
        self.time_steps,self.time_steps_idx = get_time_steps(self.file_name)

        # Load all steps from tissue file if precaching was requested
        if precache_all:
            self.t = {t_idx : Tissue(self.file_name, t_idx)
                      for t_idx in self.time_steps_idx}
        else:
            self.t = {}

    def __getitem__(self, n):
        """
        Retrieves tissue at time step index n ('/step_n' group in hdf5 file).
        Either a cached version is returned or a new step is loaded & cached.
        """
        logger = logging.getLogger(__name__)
        if n in self.time_steps_idx:
            if n in self.t:
                return self.t[n]
            else:
                tissue = Tissue(self.file_name, n)
                self.t[n] = tissue
                return tissue
        else:
            err_str = 'Requested step with index {0} not available!'.format(n)
            logger.error(err_str)
            raise Exception(err_str)

