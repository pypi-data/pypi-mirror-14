import argparse
import sys

import gitsub.add as add
import gitsub.ls as ls
import gitsub.fetch as fetch
import gitsub.sync as sync
from gitsub.utils import get_version
from gitsub.env import Environment

handler_list = {
    "add": add.handler,
    "ls": ls.handler,
    "fetch": fetch.handler,
    "sync": sync.handler,
}

def run_args(args):
    command = args.command
    command_args = args.command_args
    cmd_handler = handler_list[command]
    env = Environment(cache_dir=args.cache_dir)
    cmd_handler(command_args,env)


def main():
    parser = argparse.ArgumentParser(prog="gitsub")
    parser.add_argument("-v", "--version",
                        action="version",
                        version="gitsub v{}".
                        format(get_version())
                       )
    parser.add_argument("--cache-dir",
                        metavar="PATH",
                        default=Environment.cache_dir,
                        help="set custom repositories catalog"
                       )
    parser.add_argument("command",
                        choices=handler_list.keys(),
                        nargs="?",
                        default="fetch"
                       )
    parser.add_argument("command_args",
                        nargs=argparse.REMAINDER,
                        )

    args = parser.parse_args(sys.argv[1:])
    run_args(args)
