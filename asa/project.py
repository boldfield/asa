import sys
from asa import client, config


def list():
    fmt_str = "{:<5}{:<20}{:<20}\n"
    sys.stdout.write(fmt_str.format('', 'ID','Name'))

    conf = config.get()
    ws_id = conf['state']['workspace']
    uri = '/workspaces/{}/projects'.format(ws_id)
    projs = client.get(uri)

    for i, p in enumerate(projs):
        sys.stdout.write(fmt_str.format('[%s]' % (i+1), p['id'], p['name']))
    return 0, projs


def set():
    conf = config.get()
    if 'state' not in conf:
        conf['state'] = {}
    ec, projs = list()
    p_id = 0 
    while p_id > len(projs) or p_id <= 0:
        p_id = input('Active project: ')
        if p_id > len(projs) or p_id <= 0:
            sys.stderr.write('Unknown project, valid options are 1 - {}\n'.format(len(projs)))
    conf['state']['project'] = projs[int(p_id) - 1]['id']
    config.write(conf)
    return 0


def tasks():
    fmt_str = "{:<5}{:<20}{:<20}\n"
    sys.stdout.write(fmt_str.format('', 'ID','Name'))

    conf = config.get()
    p_id = conf['state']['project']
    uri = '/projects/{}/tasks'.format(p_id)
    params = {
        'assignee': conf['state']['user_id'],
        'completed_since': 'now'
    }
    tasks = client.get(uri, params=params)

    for i, t in enumerate(tasks):
        sys.stdout.write(fmt_str.format('[%s]' % (i+1), t['id'], t['name']))
    return 0, tasks


def task_set():
    conf = config.get()
    if 'state' not in conf:
        conf['state'] = {}
    ec, ts = tasks()
    t_id = 0 
    while t_id > len(ts) or t_id <= 0:
        t_id = input('Active task: ')
        if t_id > len(ts) or t_id <= 0:
            sys.stderr.write('Unknown task, valid options are 1 - {}\n'.format(len(ts)))
    conf['state']['task'] = ts[int(t_id) - 1]['id']
    config.write(conf)
