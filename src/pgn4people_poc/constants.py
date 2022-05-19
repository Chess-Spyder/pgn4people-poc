""" Constants for use within the pgn4people_poc project. """

import os

# do_read_pgn_from_file_system = True
DO_READ_PGN_FROM_FILE_SYSTEM = False
NAME_OF_IMPORT_PACKAGE = "pgn4people_poc"

# Name of directory of sample PGNs
DIRNAME_SAMPLE_PGNS = "example_pgns"

# Computes filesystem path of chosen sample PGN
# Relative path of directory of sample PGNs
# Relies on the standard package structure, beginning with src/
# RELATIVE_PATH_FOR_SAMPLE_PGN_FILES = "src/pgn4people_poc/example_pgns"
# RELATIVE_PATH_FOR_SAMPLE_PGN_FILES = "src/" + NAME_OF_IMPORT_PACKAGE + "/" + DIRNAME_SAMPLE_PGNS
RELATIVE_PATH_FOR_SAMPLE_PGN_FILES = os.path.join("src/", NAME_OF_IMPORT_PACKAGE, DIRNAME_SAMPLE_PGNS)

# Computes absolute filesystem path from relative path
ABSOLUTE_PATH_FOR_SAMPLE_PGN_FILES = os.path.abspath(RELATIVE_PATH_FOR_SAMPLE_PGN_FILES)

#Computes package entity from which sample PGN can be read
PACKAGE_FOR_SAMPLE_PGN = NAME_OF_IMPORT_PACKAGE + "." + DIRNAME_SAMPLE_PGNS

# Names of sample PGN files
PGNFILE1 = "test_pgn_1_simple_one_variation.pgn"
PGNFILE2 = "test_pgn_2_simple_repeated_variations_and_depth_2_variation.pgn"
PGNFILE3 = "test_pgn_3_space_between_movenumber_and_movetext.pgn"
PGNFILE4 = "test_pgn_4.pgn"
PGNFILE5 = "test_pgn_5.pgn"
PGNFILE6 = "test_pgn_6.pgn"

# Chosen sample PGN file to analyze; used for both (a) filesystem and (b) resource locations of the file
CHOSEN_SAMPLE_PGN_FILE = PGNFILE6

# Filesystem path of chosen sample PGN file
PATH_TO_CHOSEN_SAMPLE_PGN_FILE = os.path.join(ABSOLUTE_PATH_FOR_SAMPLE_PGN_FILES, CHOSEN_SAMPLE_PGN_FILE)

# Arboreal constants
UNDEFINED_NODE_MOVE_VALUE = -1
UNDEFINED_TREEISH_VALUE = -1
NODE_IS_TERMINAL_NODE = -1

INITIAL_NODE_ID = 0

# The choice_id at a node that corresponds to the main line.
INDEX_MAINLINE = 0

# Configuration constant
# Boolean
# If true, when printed, each alternative halfmove will be preceded by a single letter of the alphabet, e.g., "a:", "b:",
# etc.
# If false, the user would still enter the appropriate letter (e.g, "c" for the third alternative), but it would be up the
# user to manually count which position the alternative to be chosen occupied.
DO_PREFIX_MOVETEXT_WITH_ALPHA = True

# String constants
REPEATED_STRING_FOR_TABLE_HEADER = " ♕"

# Boolean whether to clear console between each variation table
DO_CLEAR_CONSOLE_EACH_TIME = True

# Note: (a) BLACK_MOVE_PREFIX is a true ellipsis to economize on space but (b) BLACK_MOVE_DEFERRED is more spacious
# because it needs to span an entire movetext element of a White move.
WHITE_MOVE_ELLIPSIS = "... "
BLACK_MOVE_DEFERRED = "... "
BLACK_MOVE_PREFIX = "…"
MOVETEXT_WIDTH_IN_CHARACTERS = 11

# String constants for testing validity of user input
WHITE_PLAYER_COLOR_STRING = "W"
BLACK_PLAYER_COLOR_STRING = "B"

STOP_SIGN = "stop"
RESET_COMMAND = "reset"
REPORT_COMMAND = "report"

# WARNING: FIRST_NODE_TO_BE_PRINTED is NOT a constant, despite being defined in the constants.py file. This value
# needs to be referred to from two modules (construct_output.py and traverse_tree.py) and I didn't want to pass it as
# an argument.
FIRST_NODE_TO_BE_PRINTED = True

