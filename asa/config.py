import os
import sys
from shutil import copyfile 

import pytoml

from asa import DIR


_CONFIG = None

def get():
    global _CONFIG
    if _CONFIG is not None:
        return _CONFIG
    c_path = _config_fpath()
    if not os.path.isfile(c_path):
        _CONFIG = {}
    else:
        with open(c_path, 'r') as fs:
            _CONFIG = pytoml.load(fs)
        return _CONFIG


def show():
    from . import client
    fmt_str = "{:<20}{:>60}\n"
    conf = get()

    state = conf['state']
    p_id = state['project'] if 'project' in state else None
    project = client.get('/projects/{}'.format(p_id))['name'] if p_id else None
    sys.stdout.write(fmt_str.format('Project:', project))

    t_id = state['task'] if 'task' in state else None
    task = client.get('/tasks/{}'.format(t_id))['name'] if t_id else None
    sys.stdout.write(fmt_str.format('Task:', task))

    u_id = state['user_id'] if 'user_id' in state else None
    user = client.get('/users/{}'.format(u_id))['name'] if u_id else None
    sys.stdout.write(fmt_str.format('User:', user))

    w_id = state['workspace'] if 'workspace' in state else None
    workspace = client.get('/workspaces/{}'.format(w_id))['name'] if w_id else None
    sys.stdout.write(fmt_str.format('Workspace:', workspace))

    return 0


def write(config):
    global _CONFIG
    _CONFIG = config
    c_path = _config_fpath()
    with open(c_path, 'w') as fs:
        pytoml.dump(fs, config)


def init():
    tmpl_path = os.path.join(DIR, 'tmpl', 'asa.toml')
    c_path = _config_fpath()
    if not os.path.isfile(c_path):
        copyfile(tmpl_path, c_path)
    _set_me()

    editor = os.environ.get('EDITOR', 'vi')
    ec = os.system('{} {}'.format(editor, c_path))
    if ec == 0:
        sys.stdout.write('asa successfully configured!\n')
    else:
        try:
            os.remove(c_path)
        except:
            pass
        sys.stderr.write('An unknown error occoured while creating a configuration file, please try again\n')
    return ec


def _set_me():
    from asa import client
    conf = get()
    if 'state' not in conf:
        conf['state'] = {}
    me = client.get('/users/me')
    conf['state']['user_id'] = me['id']
    write(conf)
    

def _config_fpath():
    return os.path.expanduser('~/.asa.toml')
