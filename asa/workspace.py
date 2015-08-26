import sys
from asa import client, config


def list():
    fmt_str = "{:<5}{:<20}{:<20}\n"
    sys.stdout.write(fmt_str.format('', 'ID','Name'))
    uri = '/workspaces'
    workspases = client.get(uri)
    for i, ws in enumerate(workspases):
        sys.stdout.write(fmt_str.format('[%s]' % (i+1), ws['id'], ws['name']))
    return 0, workspases


def show(ws_id):
    uri = '/workspaces/{}'.format(ws_id)
    data = client.get(uri)
    sys.stdout.write('ID:\t\t{}\n'.format(data['id']))
    sys.stdout.write('Name:\t\t{}\n'.format(data['name']))
    sys.stdout.write('Organization:\t{}\n'.format(data['name']))
    sys.stdout.write('Email Domains:\t{}\n'.format(', '.join(data['email_domains'])))


def set():
    conf = config.get()
    if 'state' not in conf:
        conf['state'] = {}
    ec, workspaces = list()
    ws_id = 0 
    while ws_id > len(workspaces) or ws_id <= 0:
        ws_id = input('Active workspace: ')
        if ws_id > len(workspaces) or ws_id <= 0:
            sys.stderr.write('Unknown workspace, valid options are 1 - {}\n'.format(len(workspaces)))
    conf['state']['workspace'] = workspaces[int(ws_id) - 1]['id']
    config.write(conf)


def tasks():
    fmt_str = "{:<5}{:<20}{:<20}\n"
    sys.stdout.write(fmt_str.format('', 'ID','Name'))

    conf = config.get()
    ws_id = conf['state']['workspace']
    uri = '/workspaces/{}/tasks'.format(ws_id)
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
