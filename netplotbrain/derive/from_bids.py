import pandas as pd
import numpy as np
from bids import BIDSLayout

def array2df(array):
    i, j = np.triu_indices(array.shape[0], k=1)
    if not (array == array.transpose()).all():
        ii = i.copy()
        jj = j.copy()
        i = np.hstack([ii, jj])
        j = np.hstack([jj, ii])
    df = pd.DataFrame(data={'i': i, 'j': j, 'weights': array[i, j]})
    return df

def edges_from_bids(path: str, derivative: str, operation: str=None, select: str=None, groups: dict=None):
    """Creates a figure using data structured in a bids directory

    Args:
        select (dict): _description_
        operation (str): What should be done with the data. Alternatives include:
            'avg' - average over the data.
            'zavg' - first fischer transform the data, average, then transform back.
            'avg_subtract' - subtract groups from each other. Groups must be specified.
            If None, returns all subjects.
        path (str): path to bids connectivity derivatives. Required if groups are specified
        groups (str): can be "session", "task", or "run" (to group by session or task) or a column name from participants.tsv in the main bids directory.

    Returns:
        edges (df, dict): edges to be used in netplotbrain.plot.
                          this is either a dataframe or a dict of dataframes where the keys are the groups
        info (dict):    infomation about the grouping.

    ToDo:
    - Once bids specification for connectivity matrices is finalized, get source node info as well.
      Then the function may change to "network_from_bids"
    - Consider an option that just returns one group subtrction
    """
    if select is None:
        select = {}
    if path is None and groups is not None:
        raise ValueError('Bids path must be specified if groups are specified')
    layout = BIDSLayout(path)
    layout.add_derivatives(derivative)
    # Check there is only one deriviative
    if len(layout.derivatives) != 1:
        raise ValueError('wrong number of derivatives found')
    derivative = list(layout.derivatives.keys())[0]
    # If path is specified, load participants.tsv to get group info
    if groups:
        if groups == 'session' or groups == 'task':
            pass
        else:
            participants = pd.read_csv(layout.get_file('participants.tsv').path, sep='\t', index_col=[0])
            # Reindex as string if indx is int, cause they will be checked against filenames
            participants.index = participants.index.astype(str)
            groups = participants[groups]
            groups.dropna(inplace=True)
            #group_info = groups.value_counts()
            group_names = groups.unique()
            #group[g] = list(groups[groups==g].index)
    files = layout.derivatives[derivative].get(**select)
    # Remove any files that do not have subject in (e.g. data_description) if still included
    files = [f for f in files if 'subject' in f.entities]
    # Init con_mat groups
    con_mat = {}
    if groups is None:
        con_mat['all'] = []
    # In theory this could be expanded to any entity
    elif groups == 'session' or groups == 'task' or groups == 'run':
        for n in layout.derivatives[derivative].get_entities()[groups].unique():
            con_mat[n] = []
    else:
        non_grouped = []
        for g in group_names:
            con_mat[g] = []
    if operation is None:
        sub_list = []
    # loop through files and group based on task, group, or session
    for f in files:
        df = pd.read_csv(f, index_col=[0], sep='\t')
        if groups is None:
            # This assumes all connectivity matrices are same size (no missing rows)
            # Might have to be changed in the future
            con_mat['all'].append(df.values)
            if operation is None:
                sub_list.append(f.entities['subject'])
        if groups == 'session' or groups == 'task' or groups == 'run':
            entities = f.get_entities()
            con_mat[entities[groups]].append(df)
        else:
            if f.entities['subject'] in groups.index:
                con_mat[groups.loc[f.entities['subject']]].append(df.values)
            else:
                non_grouped.append(f.entities['subject'])

    edges = {}
    len_per_group = {}
    for g in con_mat:
        len_per_group[g] = len(con_mat[g])
        if operation == 'avg':
            op_con_mat = np.nanmean(np.stack(con_mat[g]), axis=0)
            edges[g] = array2df(op_con_mat)
        elif operation == 'avg_subtract':
            for gg in con_mat:
                if gg == g:
                    pass
                else:
                    op_con_mat = np.nanmean(np.stack(con_mat[g]), axis=0) - np.nanmean(np.stack(con_mat[gg]), axis=0)
                    edges[str(g) + ' minus ' + str(gg)] = array2df(op_con_mat)
        elif operation is None:
            for i, c in enumerate(con_mat):
                edges[sub_list[i]] = con_mat[c]

        #edges[g] =

    if 'all' in edges and len(edges) == 1:
        edges = edges['all']

    info = {}
    info['operation'] = operation
    info['groups'] = list(edges.keys())
    info['files_found'] = len(files)
    info['files_per_group'] = len_per_group
    return edges, info


