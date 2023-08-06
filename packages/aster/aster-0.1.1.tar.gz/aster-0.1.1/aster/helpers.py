import os
import shlex
import subprocess
import sys
import yaml
from termcolor import colored, cprint

def error(msg):
    """Prints an error message and terminate the program."""
    sys.exit(colored('{}'.format(msg), 'red'))


def notice(msg):
    """Prints an notice."""
    cprint('{}'.format(msg), 'yellow')


def info(msg):
    """Prints an informational message."""
    cprint(msg, 'blue')


def progress(msg):
    """Prints progress."""
    cprint('==> ' + msg, 'blue', attrs=['bold'])


def plan(msg):
    """Prints an execution plan."""
    cprint('==> ' + msg, 'green', attrs=['bold'])


def doing(cmd, *target):
    """Prints a 'cmd target' message. """

    cmd_len = 12 if len(cmd) < 10 else 25
    print('  {}{} {}'.format(colored(cmd, 'magenta'),
                             (' ' * (cmd_len - len(cmd))),
                             ' '.join(target)))


def cmd(argv):
    subprocess.Popen(argv).wait()


def create_file(path, content):
    doing('GEN', path)
    with open(path, 'w') as f:
        f.write(content)


def load_yaml(path, validator=None):
    """Loads a yaml file."""
    yml = yaml.safe_load(open(path))
    if validator is not None:
        try:
            validator(yml)
        except ValidationError as e:
            error("validation error in '{}': {}".format(path, str(e)))
    return yml

