#!/usr/bin/env python3

import argparse 
from main import Ella


def main():
    parser = argparse.ArgumentParser(prog='ella', description="Ella - simple version control")

    subparser = parser.add_subparsers(dest='command')

    subparser.add_parser('init', help="Initialize repository")

    add_parser = subparser.add_parser('add', help="Add file to stage")
    add_parser.add_argument('file')

    commit_parser = subparser.add_parser('commit', help="Commit staged files")
    commit_parser.add_argument('message')

    subparser.add_parser('log', help="Show commit log")

    diff_parser = subparser.add_parser('show-diff', help = "Show diff for a commit")
    diff_parser.add_argument('commit_hash')

    args = parser.parse_args()

    vcs = Ella()

    if args.command == 'init':
        vcs.init()
    elif args.command == 'add':
        vcs.add(args.file)
    elif args.command == 'commit':
        vcs.commit(args.message)
    elif args.command == 'log':
        vcs.log()
    elif args.command == 'show-diff':
        vcs.show_diff(args.commit_hash)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()