# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 23:45:40 2016

Library of circles evaluating relationships between nodes.

Ing.,Mgr. (MSc.) Jan Cimbálník
Biomedical engineering
International Clinical Research Center
St. Anne's University Hospital in Brno
Czech Republic
&
Mayo systems electrophysiology lab
Mayo Clinic
200 1st St SW
Rochester, MN
United States
"""

# %% Imports

from .utils import *

import matplotlib.pyplot as plt
import matplotlib.path as m_path
import matplotlib.patches as m_patches


# %% Connection circo
def conn_circ(nodes_1, nodes_2, conn_val, data, r, rel_interval=[0, 1],
              orderby=None, groupby=None,
              ax=None, cmap='jet', labels=True, headlayer=None,
              codein=['color'], max_linewidth=1):
    """
    Creates circle with relationships between two nodes.

    Parameters:
    -----------
    nodes_1 - column name of the first node of the connection\n
    nodes_2 - column name of the second node of the connection\n
    conn_val - column name of the connection value\n
    data - pandas dataframe\n
    r - radius of the circle\n
    rel_interval - interval in witch the connections are displayed\n
    orderby - column name by which the nodes are ordered\n
    groupby - column name by which the nodes are grouped\n
    ax - axes to which the circle is plotted\n
    cmap - matplotlib cmap for colorcoding\n
    create_labels - wether to create node and group labels\n
    headlayer - leading layer where node positions are specified\n
    codein - list of methods for value coding (color, opacity, linewidth)\n
    max_linewidth - maximum linewidth\n

    Returns:
    --------
    ax - plot axes
    layer - layer object
    """

    # Create colormap
    colormap = plt.get_cmap(cmap)

    data.loc[:, 'rel_vals'] = 0
    if headlayer is None:
        node_list, node_width = create_node_list(nodes_1, data, r,
                                                 orderby=orderby,
                                                 groupby=groupby)
    else:
        node_list = headlayer.node_list
        node_list = reuse_nodes(node_list, nodes_1, data, r)
        node_width = headlayer.node_width

    conn_list = create_conns(data[[nodes_1, nodes_2, conn_val]],
                             node_width, node_list, rel_interval)

    # If no axis is passed, create onee
    if ax is None:
        plt.figure(facecolor='w')
        ax = plt.subplot(111, projection='polar')
        ax.spines['polar'].set_visible(False)

    circle = plt.Circle((0, 0), r, transform=ax.transData._b,
                        color="k", fill=False, alpha=1.)
    ax.add_artist(circle)

    for conn in conn_list:

        # Code relative value
        if 'color' in codein:
            conn.color = colormap(conn.relative_value)
        if 'opacity' in codein:
            conn.opacity = conn.relative_value
        if 'linewidth' in codein:
            conn.linewidth = max_linewidth * conn.relative_value

        t0 = conn.start_point[0]
        t1 = conn.end_point[0]

        verts = [(t0, r), (t0, r/2), (t1, r/2), (t1, r)]
        codes = [m_path.Path.MOVETO, m_path.Path.CURVE4,
                 m_path.Path.CURVE4, m_path.Path.LINETO]
        path = m_path.Path(verts, codes)

        patch = m_patches.PathPatch(path, fill=False, linewidth=conn.linewidth,
                                    edgecolor=conn.color, alpha=conn.opacity)

        ax.add_patch(patch)

    ax.set_rmax(ax.get_ylim()[1])

    if labels:
        create_labels(node_list, node_width, ax)
        if any([x.group for x in node_list]):
            create_group_labels([x for x in node_list if x.position[1] == r],
                              node_width, ax)

    # In the end create layer instance and return it
    layer = CircLayer('conn_circo', r, 0, node_list, node_width, conn_list)

    return ax, layer
