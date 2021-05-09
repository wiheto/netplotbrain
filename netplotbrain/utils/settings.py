import json
import os
from .. import __path__ as netplotpath


def _load_profile(**kwargs):
    """
    Loads profile.
    """
    profilename = kwargs.get('profile', 'default')
    if profilename != 'default' and os.path.exists(profilename):
        profilespath = profilename
    else:
        profilespath = netplotpath[0] + '/profiles/%s.json' % profilename
    with open(profilespath) as f:
        profile = json.load(f)
    profile.update(kwargs)
    return profile
