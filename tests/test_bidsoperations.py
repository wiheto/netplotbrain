import netplotbrain
import pytest

def test_task_group(): 
    edges, info = netplotbrain.edges_from_bids('./examples/bids_test/', 
                                               './examples/bids_test/derivatives/connectivity/', 
                                               operation='avg',
                                               groups='task')
    #assert 'a' in info['groups']
    
def test_session_group(): 
    edges, info = netplotbrain.edges_from_bids('./examples/bids_test/', 
                                            './examples/bids_test/derivatives/connectivity/', 
                                            operation='avg_subtract',
                                            groups='session')
    #print(info)
    #assert 'pre minus post' in info['groups']

#test_task_group()
#test_session_group()