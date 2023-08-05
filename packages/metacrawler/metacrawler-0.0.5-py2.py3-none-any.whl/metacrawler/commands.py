# coding=utf-8

import os
import argparse
from shutil import copytree

import metacrawler


def execute(*args, **kwargs):
    """Execute from CLI."""
    argparser = argparse.ArgumentParser()
    subparsers = argparser.add_subparsers(help='sub-command -h')

    startproject_parser = subparsers.add_parser(
        'startproject', help='Help: startproject -h'
    )
    startproject_parser.add_argument('path', help='Path to new project')
    startproject_parser.set_defaults(func=start_project)

    args = argparser.parse_args()
    args.func(vars(args))

def start_project(kwargs):
    """Action."""
    template_path = os.path.join(metacrawler.__path__[0], 'template')
    copytree(template_path, kwargs['path'])
