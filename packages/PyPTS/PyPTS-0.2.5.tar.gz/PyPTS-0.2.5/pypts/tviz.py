import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np
import logging

def plot(tissue, axes=None, axes_cbar=None,
         show_nodes=False, show_node_ids=False,
         show_cells=False, show_cell_ids=False, show_edges=False,
         show_walls=False, color_cells_by=None, cmap_cells=None,
         norm_cells=None):
    # Make sure we have a logger object
    logger = logging.getLogger(__name__)

    axes_was_none = False
    if axes is None:
        fig = plt.figure(figsize=(8, 8))
        axes = fig.add_subplot(111)
        axes_was_none = True

    if cmap_cells is None:
        cmap_cells = cm.YlGn

    axes.cla()
    axes.set_aspect(1.)
    #axes.grid()

    if show_nodes:
        col_nodes = (1.0,0.0,0.0)
        nodes_plot, = axes.plot(tissue.nodes_xy[:,0], tissue.nodes_xy[:,1],
                                color=col_nodes, linestyle='None', marker='o',
                                markersize=4, picker=5)
    #else:
    # If nodes were not drawn, the figure ranges are off, fix them manually
    [x_max, y_max] = tissue.nodes_xy.max(axis=0)
    [x_min, y_min] = tissue.nodes_xy.min(axis=0)
    axes.set_xlim(x_min, x_max)
    axes.set_ylim(y_min, y_max)

    if show_node_ids:
        for n_idx in tissue.nodes_idx:
            n_id = tissue.nodes_id[n_idx]
            n_xy = tissue.nodes_xy[n_idx]
            plt.text(n_xy[0], n_xy[1], ('{0}').format(n_id), color=(0.6,0,0))

    if show_cells:
        cells_poly = []
        for c_idx in tissue.cells_idx:
            # Nodes of the current cell
            cell_nodes_xy = tissue.get_cell_nodes_coord(c_idx)
            # Polygon that defines the cell geometry
            cells_poly.append(Polygon(cell_nodes_xy))

            if show_cell_ids:
                # Plot cell ID
                cc_xy = np.average(cell_nodes_xy, axis=0)
                c_id = tissue.cells_id[c_idx]
                plt.text(cc_xy[0], cc_xy[1], ('{0}').format(c_id))

        # Collection of patches to draw is created from the list of polygons
        cells_patches = PatchCollection(cells_poly, cmap=cmap_cells, norm=norm_cells)

        # Set the array of per-polygon (cell) values used to color the cells
        # That might be either a string holding the name of a cell attribute,
        # a predefined string ('num_neighbors' is the only supported atm) or
        # an array with the values used for plotting (len() == num_cells).
        if isinstance(color_cells_by, basestring):
            if color_cells_by is 'num_neighbors':
                cells_patches.set_array(tissue.cells_num_walls)
            elif color_cells_by in tissue.cells_attributes.keys():
                cells_patches.set_array(tissue.cells_attributes[color_cells_by])
            else:
                err_str = 'Cell attribute {0} not found'.format(color_cells_by)
                logger.error(err_str)
                raise Exception(err_str)
        elif isinstance(color_cells_by, np.ndarray) \
            and color_cells_by.ndim == 1 \
            and len(color_cells_by) == tissue.num_cells:
            cells_patches.set_array(color_cells_by)
        else:
            err_str = 'I can\'t color cells by ' + color_cells_by
            logger.error(err_str)
            raise Exception(err_str)

        # Add the collection to draw to the axis
        axes.add_collection(cells_patches)

        if axes_cbar is not None:
            # Create a legend-like color bar to show the range of cell based values
            #axes_cbar.cla()
            #plt.colorbar(cells_patches, cax=axes_cbar, orientation='horizontal')
            plt.colorbar(cells_patches, ax=axes, orientation='horizontal')

    if show_edges:
        for e_idx in tissue.edges_idx:
            ns_id = tissue.edges_nodes[e_idx]
            n0_xy = tissue.nodes_xy[tissue.nodes_idx[ns_id[0]]]
            n1_xy = tissue.nodes_xy[tissue.nodes_idx[ns_id[1]]]
            ec_xy = 0.5 * (n0_xy + n1_xy)
            plt.plot((n0_xy[0], n1_xy[0]), (n0_xy[1], n1_xy[1]), '--', color=(.1,.1,.7), lw=5)
            plt.text(ec_xy[0], ec_xy[1], ('{0}').format(e_idx), color=(.5,.6,.0), fontsize=16)

    if show_walls:
        for w_idx in tissue.walls_idx:
            w_id = tissue.walls_id[w_idx]
            ns_id = tissue.walls_nodes[w_idx]
            n0_xy = tissue.nodes_xy[tissue.nodes_idx[ns_id[0]]]
            n1_xy = tissue.nodes_xy[tissue.nodes_idx[ns_id[1]]]
            wc_xy = 0.5 * (n0_xy + n1_xy) + [0.04,0.04]
            plt.plot((n0_xy[0], n1_xy[0]), (n0_xy[1], n1_xy[1]), ':', color=(.1,.7,.1), lw=5)
            plt.text(wc_xy[0], wc_xy[1], ('{0}').format(w_id), color=(.1,.3,.1), fontsize=20)

    if axes_was_none:
        plt.show()
        return fig

def plot_cells(axes, tissue):
    """
    Uses a matplotlib axes object to draw the tissue on screen
    """
    axes.cla()
    axes.set_aspect(1.)
    axes.grid()

    # Plot cells (loop over all cells and plot each separately)
    for c_idx in tissue.cells_idx:
        # Nodes of the current cell
        cell_nodes_xy = tissue.get_cell_nodes_xy(c_idx)
        # Polygon that defines the cell geometry
        cell_poly = Polygon(cell_nodes_xy, facecolor=(1,1,1), linewidth=1)
        axes.add_patch(cell_poly)

        # Plot cell ID
        cc_xy = np.average(cell_nodes_xy, axis=0)
        c_id = tissue.cells_id[c_idx]
        plt.text(cc_xy[0], cc_xy[1], ('{0}').format(c_id))

    # Plot nodes
    col_nodes = (1.0,0.0,0.0)
    nodes_plot, = axes.plot(tissue.nodes_xy[:,0], tissue.nodes_xy[:,1],
                            color=col_nodes, linestyle='None', marker='o',
                            markersize=4)

    # Plot node IDs
    for n_idx in tissue.nodes_idx:
        n_id = tissue.nodes_id[n_idx]
        n_xy = tissue.nodes_xy[n_idx]
        plt.text(n_xy[0], n_xy[1], ('{0}').format(n_id), color=(0.6,0,0))

