import netplotbrain

npbpath = netplotbrain.__path__[0]
def test_task_group():
    edges, info = netplotbrain.edges_from_bids(npbpath + '/example_data/bids_test/',
                                               npbpath + '/example_data/bids_test/derivatives/connectivity/',
                                               operation='avg',
                                               groups='task')
    assert 'a' in info['groups']

def test_session_group():
    edges, info = netplotbrain.edges_from_bids(npbpath + '/example_data/bids_test/',
                                               npbpath + '/example_data/bids_test/derivatives/connectivity/',
                                               operation='avg_subtract',
                                               groups='session')
    assert 'pre minus post' in info['groups']

test_task_group()
test_session_group()