import sys
from asa import client, config


def list():
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


def show():
    fmt_str = "{:<20}{:>50}\n"
    conf = config.get()
    t_id = conf['state']['task']
    uri = '/tasks/{}'.format(t_id)
    task = client.get(uri)
    projects = map(lambda x: x['name'], task['projects'])

    sys.stdout.write(fmt_str.format('Name:', task['name'])) 
    sys.stdout.write(fmt_str.format('Parent:', task['parent'] if task['parent'] else ''))
    sys.stdout.write(fmt_str.format('Created:', task['created_at']))
    sys.stdout.write(fmt_str.format('Modified:', task['modified_at']))
    sys.stdout.write(fmt_str.format('Due:', task['due_on'] if task['due_on'] else ''))
    sys.stdout.write(fmt_str.format('Workspace:', task['workspace']['name']))
    sys.stdout.write(fmt_str.format('Projects:', ', '.join(projects)))
    sys.stdout.write(fmt_str.format('Notes:', task['notes']))
    sys.stdout.write('Comments:\n\n')

    uri = '/tasks/{}/stories'.format(t_id)
    stories = client.get(uri)
    for story in stories:
        if story['type'] == 'comment':
            sys.stdout.write('{:<80}'.format(story['text'])) 
            sys.stdout.write('\n' + '-' * 40 + '\n')
