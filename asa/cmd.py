"""Asana CLI (asa): Command line interface to the Asana task management system

Usage:
    asa [options] conf
    asa [options] conf me
    asa [options] state
    asa [options] ws 
    asa [options] ws set
    asa [options] ws t
    asa [options] ws t set
    asa [options] ws <workspace_id>
    asa [options] p
    asa [options] p set
    asa [options] p t
    asa [options] p t set
    asa [options] t

Options:
    -h --help              Show this screen
    -v --version           Show version information

"""
import sys
from docopt import docopt

from asa import config, workspace, task, project


def main():
    from . import __version__
    args = docopt(__doc__, version='asa {}'.format(__version__))

    if args['conf']:
        if args['me']:
            ec = config._set_me()
        else:
            ec = config.init()
        sys.exit(ec)

    conf = config.get()
    if not conf:
        sys.stderr.write("Please run 'asa configure' before running for the first time.\n")
        sys.exit(1)

    if args['state']:
      ec = config.show()
    elif args['ws']:
        if args['t']:
            if args['set']:
                ec = workspace.task_set()
            else:
                ec, _ = workspace.tasks()
        elif args['set']:
            ec = workspace.set()
        elif args['<workspace_id>'] is not None:
            ec = workspace.show(args['<workspace_id>'])
        else:
            ec, _ = workspace.list()
    elif args['p']:
        if args['t']:
            if args['set']:
                ec = project.task_set()
            else:
                ec, _ = project.tasks()
        elif args['set']:
            ec = project.set()
        else:
            ec, _ = project.list()
    elif args['t']:
        ec = task.show()

    sys.exit(ec)
