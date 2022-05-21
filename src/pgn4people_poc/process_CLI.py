"""
Checks argument on command line for a path to a user-supplied PGN file.
"""

import argparse
import pathlib

def check_CLI_for_user_pgnfile():

    parser = argparse.ArgumentParser()
    
    # Defines argument
    #   nargs='?': One argument will be consumed from the command line if possible, and produced as a single item.
    #       If no command-line argument is present, the value from default will be produced.
    #   default=None: Unnecessary, because `default` defaults to `None`, but included for clarity.`
    parser.add_argument('user_pgn_filepath', nargs='?', default=None, type=pathlib.Path)

    # Parse argument(s)
    args = parser.parse_args()

    # Return a pathlib.Path object, which supports the open() method.
    # See https://docs.python.org/3/library/pathlib.html#pathlib.Path.open
    user_pgn_filepath = args.user_pgn_filepath

    return user_pgn_filepath
