from aster.backend import import_backend
from aster import g
from aster.helpers import plan


def main():
    backend = import_backend()
    backend.deploy()
    plan("{} has been deployed, yay!".format(g.config['name']))

