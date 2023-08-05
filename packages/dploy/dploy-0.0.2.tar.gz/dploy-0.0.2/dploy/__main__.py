#!/usr/bin/env python3

import argparse

import dploy
from dploy.util import dynamic_import

parser = argparse.ArgumentParser(description='dploy dotfiles')
parser.add_argument(
        "--file",
        default="~/dotfiles/setup_config.py",
        help="path of the dploy file")

args = parser.parse_args()

setup_config = dynamic_import(args.file, "")


def main():
    dploy.backup(
            setup_config.DOTFILES,
            setup_config.DOTFILES_DIRECTORY)
    print("\n")

    dploy.symlink_files(
            setup_config.DOTFILES,
            setup_config.DOTFILES_DIRECTORY)
    print("\n")

    dploy.create_files(setup_config.FILES)
    print("\n")

    dploy.create_directories(setup_config.DIRECTORIES)
    print("\n")

if __name__ == "__main__":
    main()
