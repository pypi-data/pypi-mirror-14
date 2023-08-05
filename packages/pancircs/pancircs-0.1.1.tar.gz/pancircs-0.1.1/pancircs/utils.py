# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 23:34:16 2016

Library of objects and internal functions

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


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# %% Node class


class CircNode:

    def __init__(self, position, label, group=None):
        self.position = position
        self.label = label
        self.group = group
        self.relative_value = 0
        self.color = "b"
        self.opacity = 1
        self.patch = None


# %% Connection class

class CircConn:

    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.start_point = []
        self.end_point = []
        self.relative_value = 0
        self.color = "b"
        self.opacity = 1
        self.linewidth = 1
        self.patch = None

# %% Layer class


class CircLayer:

    def __init__(self, l_type, r, span, node_list=None, node_width=0,
                 conn_list=None):
        self.type = l_type
        self.r = r
        self.span = span
        self.node_list = node_list
        self.node_width = node_width
        self.conn_list = conn_list
        self.cmap = 'jet'  # Is this neccessary?
        self.sublayer = None  # This is only for heatmap
        self.labels = False


# %% Create labels

# TODO - make this a node funciton ?

def create_labels(node_list, node_width, ax):

    # Remove original ticks
    plt.xticks([])
    plt.yticks([])

    # Draw node labels
    for node in node_list:
        angle_deg = 180 * (node.position[0] + node_width/2) / np.pi
        angle_rad = (node.position[0] + node_width/2)

        if angle_deg >= 270 or angle_deg <= 90:
            ha = 'left'
        else:
            # Flip the label, so text is always upright
            angle_deg += 180
            ha = 'right'
        ax.text(angle_rad, ax.get_ylim()[1]+0.4, node.label,
                rotation=angle_deg, rotation_mode='anchor',
                horizontalalignment=ha, verticalalignment='center')


def create_group_labels(node_list, node_width, ax):

    # Remove original ticks
    plt.xticks([])
    plt.yticks([])

    # Get groups
    group_list = list(set([node.group for node in node_list]))

    for group in group_list:
        group_thetas = [node.position[0] for node in node_list
                        if node.group == group]
        group_start = min(group_thetas)
        group_end = max(group_thetas)
        group_width = group_end - group_start

        angle_deg = 180 * (group_start + group_width/2 + node_width/2) / np.pi
        angle_rad = (group_start + group_width/2 + node_width/2)

        if angle_deg >= 270 or angle_deg <= 90:
            ha = 'left'
        else:
            # Flip the label, so text is always upright
            angle_deg += 180
            ha = 'right'

        ax.text(angle_rad, ax.get_ylim()[1]+2, group,
                rotation=angle_deg, rotation_mode='anchor',
                horizontalalignment=ha, verticalalignment='center')

# %% Node operations


def create_node_list(nodes, data, r, orderby=None, groupby=None,
                     sublayers=None, r_increment=0.1):

    # TODO - needs incremet for heatmap

    # Create groups if set
    N_groups = 0
    if groupby is not None:
        # Reorder the dataframe to match the groups
        if orderby is not None:
            data = data.sort_values(by=[groupby, orderby])
        else:
            data = data.sort_values(by=[groupby])

        group_list = list(data[groupby].unique())
        N_groups = len(group_list)  # This number is equal to number of gaps

    N = len(data[nodes].unique())  # This should be the number of channels
    thetas = np.linspace(0.0, 2*np.pi, N + N_groups, endpoint=False)
    node_width = 2 * np.pi / (N + N_groups)

    node_list = []
    for node_idx, node_label in enumerate(data[nodes].unique()):
        if groupby is not None:
            node_groups = data[(data[nodes] == node_label)][groupby].unique()
            if len(node_groups) > 1:
                print('Node belongs to more than one group!!!')
            group_idx = group_list.index(node_groups)

            node_idx += group_idx
            group = group_list[group_idx]
        else:
            group = None

        # FIXME: There has to be a better way to deal withe heatmap problem
        if sublayers is None:

            # Create node instance
            node = CircNode([thetas[node_idx], r], node_label)
            node.group = group
            node.relative_value = data[(data[nodes] == node_label)]['rel_vals']

            # Add to node list
            node_list.append(node)
        else:
            i = 0
            for sublayer in data[sublayers].unique():
                row = r_increment * i
                # Create node instance
                node = CircNode([thetas[node_idx], r + row], node_label)
                node.group = group
                rel_val = data[(data[nodes] == node_label) &
                               (data[sublayers] == sublayer)]['rel_vals']
                # In case the value is not in the dataframe
                if len(rel_val):
                    node.relative_value = rel_val
                else:
                    node.relative_value = 0

                i += 1

                # Add to node list
                node_list.append(node)

    return node_list, node_width


def reuse_nodes(node_list, nodes, data, r, sublayers=None,
                r_increment=0.1):

    # Take care of nodes coming from heatmap - takes only inner circle
    min_val = min([x.position[1] for x in node_list])
    node_list = [x for x in node_list if x.position[1] == min_val]

    new_node_list = []
    for node in node_list:

        # FIXME: There has to be a better way to deal withe heatmap problem
        if sublayers is None:

            # Create node instance
            new_node = CircNode([node.position[0], 0], node.label,
                                  group=node.group)
            new_node.position[1] = r
            rel_val = data[(data[nodes] == new_node.label)]['rel_vals']
            # In case the value is not in the dataframe
            if len(rel_val):
                new_node.relative_value = rel_val
            else:
                new_node.relative_value = 0

            # Add to node list
            new_node_list.append(new_node)
        else:
            i = 0
            for sublayer in data[sublayers].unique():
                row = r_increment * i
                # Create node instance
                new_node = CircNode([node.position[0], 0], node.label,
                                      group=node.group)
                new_node.position[1] = r + row
                rel_val = data[(data[nodes] == new_node.label) &
                               (data[sublayers] == sublayer)]['rel_vals']
                # In case the value is not in the dataframe
                if len(rel_val):
                    new_node.relative_value = rel_val
                else:
                    new_node.relative_value = 0
                i += 1
                # Add to node list
                new_node_list.append(new_node)

    return new_node_list

# %% Connection operations


def create_conns(data, node_width, nodes, rel_interval):
    conns_df = pd.DataFrame()
    conns_df[['node_1', 'node_2', 'conn_val']] = data

    # Sort by connection strength? - to plot the strongest ones first?

    # Remove duplicate - move this into the function later
    conns_df = conns_df[(conns_df.node_1) != (conns_df.node_2)]
    max_value = conns_df.conn_val.max()
    min_value = conns_df.conn_val.min()
    val_range = max_value - min_value

    # Create relativistic values for connection strengths
    conns_df.conn_val = (conns_df.conn_val - min_value) / val_range

    # Reduce by interval
    if type(rel_interval[0]) == list:
        new_conn_df = pd.DataFrame()
        for interval in rel_interval:
            int_start = conns_df.conn_val.quantile(interval[0])
            int_stop = conns_df.conn_val.quantile(interval[1])
            pd.concat([new_conn_df,
                      conns_df[((conns_df.conn_val >= int_start) &
                                (conns_df.conn_val <= int_stop))]])
    else:
        int_start = conns_df.conn_val.quantile(rel_interval[0])
        int_stop = conns_df.conn_val.quantile(rel_interval[1])
        conns_df = conns_df[((conns_df.conn_val >= int_start) &
                             (conns_df.conn_val <= int_stop))]

    # Sorth the connections by strength
    conns_df = conns_df.sort_values(by=['conn_val'], ascending=True)

    # Get number of connections and reate start and end points with jitter
    # This should be proportional to number of nodes
    noise_max = node_width * 0.5
    rng = np.random.mtrand.RandomState(seed=0)
    conns_df['node_1_conns'] = 1
    conns_df['node_2_conns'] = 1
    for node in nodes:
        conns_df.loc[(conns_df.node_1 == node.label),
                     'node_1_conns'] = sum(
                     conns_df.node_1 == node.label) + sum(
                     conns_df.node_2 == node.label)
        conns_df.loc[(conns_df.node_1 == node.label),
                     'node_2_conns'] = sum(
                     conns_df.node_2 == node.label) + sum(
                     conns_df.node_1 == node.label)

    for conn_row in conns_df.iterrows():
        i = conn_row[0]
        start_noise = rng.uniform(-noise_max, noise_max,
                                  conns_df.loc[i, 'node_1_conns'])[0]
        conns_df.loc[i, 'start_noise'] = start_noise
        end_noise = rng.uniform(-noise_max, noise_max,
                                conns_df.loc[i, 'node_2_conns'])[-1]
        conns_df.loc[i, 'end_noise'] = end_noise

    nodes_n_con_seen = np.zeros(len(nodes))
    conn_list = []
    for conn_row in conns_df.iterrows():
        i = conn_row[0]
        row_vals = conn_row[1]

        start_idxs = [idx for idx, x in enumerate(nodes) if x.label ==
                      row_vals.node_1]
        end_idxs = [idx for idx, x in enumerate(nodes) if x.label ==
                    row_vals.node_2]
        if len(start_idxs) == 0 or len(end_idxs) == 0:
            continue
        start = start_idxs[0]
        end = end_idxs[0]
        nodes_n_con_seen[start] += 1
        nodes_n_con_seen[end] += 1

        # Create connection object
        conn = CircConn([x for x in nodes if x.label == row_vals.node_1][0],
                          [x for x in nodes if x.label == row_vals.node_2][0])
        start_noise = conns_df.loc[i, 'start_noise']
        end_noise = conns_df.loc[i, 'end_noise']
        conn.start_point = ([conn.start_node.position[0] +
                            (node_width/2) +
                            start_noise,
                            conn.start_node.position[1]])
        conn.end_point = ([conn.end_node.position[0] +
                          (node_width/2) +
                          end_noise,
                          conn.end_node.position[1]])
        conn.relative_value = conns_df.loc[i, 'conn_val']
        conn_list.append(conn)

    return conn_list
