import argparse
import aster.g as g
from aster.new import main as new_command
from aster.generate import main as generate_command
from aster.deploy import main as deploy_command
from aster.install import main as install_command
from aster.server import main as server_command
from aster.helpers import *

def main(args):
    parser = argparse.ArgumentParser(description='A pythonic serverless web application framework for minimalist')
    subparsers = parser.add_subparsers()

    new_parser = subparsers.add_parser(name='new')
    new_parser.add_argument('path')
    new_parser.set_defaults(func=new_command)

    generate_parser = subparsers.add_parser(name='generate')
    generate_parser.set_defaults(func=generate_command)

    install_parser = subparsers.add_parser(name='install')
    install_parser.set_defaults(func=install_command)

    deploy_parser = subparsers.add_parser(name='deploy')
    deploy_parser.set_defaults(func=deploy_command)

    server_parser = subparsers.add_parser(name='server')
    server_parser.set_defaults(func=server_command)

    if len(args) == 0:
        args = ['-h']

    g.args = parser.parse_args(args)

    if g.args.func == new_command:
        g.config = {}
    else:
        g.config = load_yaml('config/application.yml')

    g.args.func()
