# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 23:47:18 2016

Library of patch circles + dummy circle.

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
import numpy as np


# %% Add custom patches

def patch_circ(nodes, groupby, data, r, cmap='jet', patch_height=1, ax=None,
               group_order=None, group_colors=None, labels=False,
               headlayer=None):

    """
    Creates circle with each node as a patch colored according to its group.

    Parameters:
    -----------
    nodes - column name with node names\n
    groupby - column name with node groups\n
    data - pandas dataframe\n
    r - radius of the circle\n
    cmap - matplotlib cmap for colorcoding\n
    patch_height - height of the patch\n
    ax - axes to which the circle is plotted\n
    group_order - list with group names with set order\n
    group_colors - colors for groups - standar matplotlib coding\n
    create_labels - wether to create node and group labels\n
    headlayer - leading layer where node positions are specified\n

    Returns:
    --------
    ax - plot axes
    layer - layer object
    """

    # Groups
    if group_order is None:
        groups = list(data[groupby].unique())
    else:
        groups = group_order

    # Create colors if None are set
    if group_colors is None:
        # Create colormap
        colormap = plt.get_cmap(cmap)
        group_color_vals = np.linspace(0, 1, len(groups), endpoint=False)
        group_colors = colormap(group_color_vals)

    # Create node list
    data.loc[:, 'rel_vals'] = 0
    if headlayer is None:
        node_list, node_width = create_node_list(nodes, data, r,
                                                 groupby=groupby)
    else:
        node_list = headlayer.node_list
        node_list = reuse_nodes(node_list, nodes, data, r)
        node_width = headlayer.node_width

    # If no axis is passed, create one
    if ax is None:
        plt.figure(facecolor='w')
        ax = plt.subplot(111, projection='polar')
        ax.spines['polar'].set_visible(False)

    for node in node_list:
        node_group = data.loc[(data[nodes] == node.label), groupby].values[0]
        node.color = group_colors[groups.index(node_group)]

        # Create node in plot

        bar = ax.bar(node.position[0], patch_height, width=node_width,
                     bottom=r, color=node.color, edgecolor=node.color,
                     alpha=node.opacity)[0]

        node.patch = bar

    if labels:
        create_labels(node_list, node_width, ax)
        if any([x.group for x in node_list]):
            create_group_labels(node_list, node_width, ax)

    # In the end create layer instance
    layer = CircLayer('hist_circo', r, patch_height, node_list, node_width)

    return ax, layer


# %% Dummy circ

def dummy_circ(nodes, data, orderby=None, groupby=None,
               ax=None, headlayer=None):

    """
    Creates a dummy circle that is not visible. Serves for creation of node
    locations and groups.

    Parameters:
    -----------
    nodes - column name with node names\n
    data - pandas dataframe\n
    orderby - column name by which the nodes are ordered\n
    groupby - column name with node groups\n
    ax - axes to which the circle is plotted\n
    headlayer - leading layer where node positions are specified\n

    Returns:
    --------
    ax - plot axes
    layer - layer object
    """

    # Create node list
    data['rel_vals'] = 0
    if headlayer is None:
        node_list, node_width = create_node_list(nodes, data, 0,
                                                 orderby=orderby,
                                                 groupby=groupby)
    else:
        node_list = headlayer.node_list
        node_list = reuse_nodes(node_list, nodes, data, 0)
        node_width = headlayer.node_width

    # In the end create layer instance
    layer = CircLayer('dummy_circ', 0, 0, node_list, node_width)

    return ax, layer
