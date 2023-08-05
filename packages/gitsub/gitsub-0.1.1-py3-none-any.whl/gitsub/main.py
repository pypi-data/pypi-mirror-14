import argparse
import os
import sys
from .repo import RepoFactory
from . import utils
from .display import show

def handle_sync(repo_file):
    repos = [RepoFactory.new(path.rstrip("\n")) for path in open(repo_file,'r').readlines()]
    for repo in repos:
        repo.sync()

def handle_fetch(repo_file):
    repos = [RepoFactory.new(path.rstrip("\n")) for path in open(repo_file,'r').readlines()]
    updates = [ repo.query(['name', 'commits']) for repo in repos ]
    show(updates)

command_list = {
    "sync": handle_sync,
    "fetch": handle_fetch
}

def handle_cmd(repo_file, cmd):
    if not os.path.isfile(repo_file):
        rfile = open(repo_file,'w')
        rfile.close()

    command_list[cmd](repo_file)


def main():
    parser = argparse.ArgumentParser(prog="gitsub")
    parser.add_argument("-v", "--version",
                        action="version",
                        version="gitsub v{}".
                        format(utils.get_version())
                       )
    parser.add_argument("--repo-file",
                        metavar="FILE",
                        default=os.path.expanduser('~/.gitsub'),
                        help="set custom repositories catalog"
                       )
    parser.add_argument("command",
                        choices=["fetch","sync"],
                        nargs="?",
                        default="fetch"
                       )

    args = parser.parse_args(sys.argv[1:])

    handle_cmd(args.repo_file, args.command)
