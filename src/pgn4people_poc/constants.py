""" Constants for use within the pgn4people_poc project. """

import os


#   BEHAVIORAL CONSTANTS

# Boolean whether to clear console between each variation table
DO_CLEAR_CONSOLE_EACH_TIME = True

# Whether, in the variations table,  to precede each alternative movetext by a letter of the alphabet.
# If True, when printed, each alternative halfmove will be preceded by a single letter of the alphabet, e.g., "a:",
# "b:", etc.
# If False, the user would still enter the appropriate letter (e.g, "c" for the third alternative), but it would be up
# the user to manually count which position the alternative to be chosen occupied.
DO_PREFIX_MOVETEXT_WITH_ALPHA = True

#   CONSTANTS RELATED TO PROJECT NAMES AND FILE LOCATIONS

# Name of entry point a user types in the CLI to execute the program
entry_point_name = "pgn4people"

NAME_OF_IMPORT_PACKAGE = "pgn4people_poc"

# Name of directory of sample PGNs
DIRNAME_SAMPLE_PGNS = "example_pgns"

# Computes package entity from which sample PGN can be read
# (The sample PGN(s) are in a subpackage of the import package.)
PACKAGE_FOR_SAMPLE_PGN = NAME_OF_IMPORT_PACKAGE + "." + DIRNAME_SAMPLE_PGNS

# Names of sample PGN files
PGNFILE1 = "demo_pgn_1.pgn"

# Chosen sample PGN file to analyze; used for both (a) filesystem and (b) resource locations of the file
CHOSEN_SAMPLE_PGN_FILE = PGNFILE1

# Descriptor presented when sample PGN is chosen
PUBLIC_BASENAME_SAMPLE_PGN = f"Built-in sample PGN: {CHOSEN_SAMPLE_PGN_FILE}"
VERSION_SAMPLE_PGN = "1.0.0"

# ARBOREAL CONSTANTS

UNDEFINED_TREEISH_VALUE = -1
NODE_IS_TERMINAL_NODE = -1

INITIAL_NODE_ID = 0

# The choice_id at a node that corresponds to the main line.
INDEX_MAINLINE = 0

# VARIATIONS TABLE CONSTANTS

# String constants
REPEATED_STRING_FOR_TABLE_HEADER = " ♕"

WELCOME_MESSAGE = "Welcome to PGN4people!"

# Note: (a) BLACK_MOVE_PREFIX is a true ellipsis to economize on space but (b) BLACK_MOVE_DEFERRED is more spacious
# because it needs to span an entire movetext element of a White move.
WHITE_MOVE_ELLIPSIS = "... "
BLACK_MOVE_DEFERRED = "... "
BLACK_MOVE_PREFIX = "…"

MOVETEXT_WIDTH_IN_CHARACTERS = 11

# String constants for testing validity of user input
WHITE_PLAYER_COLOR_STRING = "W"
BLACK_PLAYER_COLOR_STRING = "B"

# User-input constants
# These must be lowercase, because they will be compared to lowercase-d versions of user input.
STOP_SIGN = "stop"
RESET_COMMAND = "reset"
REPORT_COMMAND = "report"
NODEREPORT_COMMAND = "nodereport"

# CONSTANTS FOR GameTreeReport
# Width for (a) depth or (b) halfmove-length
KEY_WIDTH_IN_CHARACTERS = 4

FREQ_WIDTH_IN_CHARACTERS = 11

KEY_STAT_DESCRIPTION_WIDTH = 27
KEY_STAT_VALUE_WIDTH = 5

# ARGPARSER CONSTANTS
# Help text if `pgn4people --help`
# Note that argparser appears to ignore newline characters
HELP_DESCRIPTION = ("A proof-of-concept demonstration of a better way to view deeply nested PGN files. "
                    "You can optionally supply the path to your own PGN file. To use your own PGN file "
                    "(rather than the supplied sample), enter the path to the file after the pgn4people "
                    "command. (Rather than typing the path, you can (a) drag the file’s icon to the command line "
                    "or (b) “cd” (change directory) to the directory with your PGN file; then just type the "
                    "file *name* (e.g., “mygame.pgn”); no path necessary.)")

HELP_EPILOG = "For more on PGN4people, see github.com/jimratliff/pgn4people-poc "


# WARNING: FIRST_NODE_TO_BE_PRINTED is NOT a constant, despite being defined in the constants.py file. This value
# needs to be referred to from two modules (construct_output.py and traverse_tree.py) and I didn't want to pass it as
# an argument.
FIRST_NODE_TO_BE_PRINTED = True

