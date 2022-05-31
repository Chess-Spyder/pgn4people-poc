""" Constants for use within the pgn4people_poc project. """

import os

#   BEHAVIORAL CONSTANTS

# do_read_pgn_from_file_system = True
DO_READ_SAMPLE_PGN_FROM_FILE_SYSTEM = False

# Boolean whether to clear console between each variation table
DO_CLEAR_CONSOLE_EACH_TIME = True

# Whether to precede each alternative movetext by a letter of the alphabet
# If true, when printed, each alternative halfmove will be preceded by a single letter of the alphabet, e.g., "a:", "b:",
# etc.
# If false, the user would still enter the appropriate letter (e.g, "c" for the third alternative), but it would be up the
# user to manually count which position the alternative to be chosen occupied.
DO_PREFIX_MOVETEXT_WITH_ALPHA = True

#   CONSTANTS RELATED TO FILE LOCATIONS

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

# ARBOREAL CONSTANTS

UNDEFINED_NODE_MOVE_VALUE = -1
UNDEFINED_TREEISH_VALUE = -1
NODE_IS_TERMINAL_NODE = -1

INITIAL_NODE_ID = 0

# The choice_id at a node that corresponds to the main line.
INDEX_MAINLINE = 0

# VARIATIONS TABLE CONSTANTS

# String constants
REPEATED_STRING_FOR_TABLE_HEADER = " ♕"

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
ARGPARSER_DESCRIPTION = "Demonstrates a better way to view deeply nested PGN files. You can optionally supply the path to your own PGN file."

ARGPARSER_USAGE_1 = "To use your own PGN file (rather than the supplied sample), enter the path to\n"
ARGPARSER_USAGE_2 = "the file after the pgn4people command. (Rather than typing the path, you can\n"
ARGPARSER_USAGE_3 = "drag the file’s icon to the command line. "
ARGPARSER_USAGE = ARGPARSER_USAGE_1 + ARGPARSER_USAGE_2 + ARGPARSER_USAGE_3


# WARNING: FIRST_NODE_TO_BE_PRINTED is NOT a constant, despite being defined in the constants.py file. This value
# needs to be referred to from two modules (construct_output.py and traverse_tree.py) and I didn't want to pass it as
# an argument.
FIRST_NODE_TO_BE_PRINTED = True

