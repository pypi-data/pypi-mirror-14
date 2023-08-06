#!/usr/bin/python

import argparse
import os
from .eclipse import write_metadata_files
from .git import clone


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("remote_url", help="url of the remote git repository (https or ssh)")
    parser.add_argument("destination", help="directory to clone repository to")
    parser.add_argument("--gitargs", metavar="args", type=str, help="extra arguments for git")
    parser.add_argument("--force", nargs="?", help="write metadata files even if they already exist in the repo",
                        default=False, type=bool)
    return parser.parse_args()


def main():
    args = parse_args()
    repo = clone(args.remote_url, args.destination)
    write_metadata_files(args.destination, os.path.split(args.destination)[1], args.force)

if __name__ == "__main__":
    main()