"""
Functions to help parse PGN file of a chess game.
"""

from importlib.resources import files
import os
import re

from . import constants
from . error_processing import (fatal_error_exit_without_traceback,
                                fatal_pgn_error)
from . jdr_utilities import check_CLI_for_user_file
from . jdr_utilities import id_text_between_first_two_blankish_lines
from . strip_balanced_braces import strip_balanced_braces_from_string

def acquire_tokenized_pgnstring():
    """
    Get string of PGN from either (a) file specified by user in command line or (b) a built-in PGN file,
    strips the headers, and tokenizes the remaining movetext.
    """

    # Checks command line to see whether user specified her own PGN file to view
    # user_pgn_fileobject will be either (a) a file object or (b) None
    user_pgn_filepath = check_CLI_for_user_file(constants.HELP_DESCRIPTION, constants.HELP_EPILOG)

    if user_pgn_filepath is None:
        # User didn't specify her own PGN file, so use sample PGN file included in the package
        string_read_from_file = read_resource_pgnfile_into_string(constants.PACKAGE_FOR_SAMPLE_PGN,
                                                                  constants.CHOSEN_SAMPLE_PGN_FILE)
        is_sample_pgn = True
        pgn_source = PGNSource(is_sample_pgn, None)
    else:
        # string_read_from_file = user_pgn_fileobject.read()
        try:
            with user_pgn_filepath.open('r') as file:
                string_read_from_file = file.read()
                is_sample_pgn = False
                pgn_source = PGNSource(is_sample_pgn, user_pgn_filepath)
        except FileNotFoundError as err:
            pgn_file_not_found_fatal_error(user_pgn_filepath, err)
    
    pgnstring = strip_headers_from_pgn_file(string_read_from_file, pgn_source)

    pgnstring = strip_balanced_braces_from_string(pgnstring)

    if not pgnstring:
        fatal_pgn_error("No valid movetext found", pgn_source)
   
    # Parse string into a list of tokens, either (a) a movetext entry (e.g., "e4"), (b) “(”, or (c) “)”.
    tokenlist = tokenize_pgnstring(pgnstring)

    return tokenlist, pgn_source


class PGNSource():
    """
    Class instance embodies metadata for the chosen PGN file to be communicated, e.g., for output header
    """
    def __init__(self, is_sample_pgn, path_to_pgnfile):
        self.is_sample_pgn = is_sample_pgn
        if path_to_pgnfile is None:
            self.path_to_pgnfile = None
            self.filename_of_pgnfile = None
        else:
            self.path_to_pgnfile = path_to_pgnfile
            self.filename_of_pgnfile = os.path.basename(path_to_pgnfile)



def read_resource_pgnfile_into_string(pgnresource_package, pgnresource_filename):
    """
    Read raw PGN text file that is present as a packaged resource (rather than guaranteed to be on the file system).
    """

    # Constructs a chained package representation of the location of the desired sample PGN file
    #
    # The following “/” syntax is equivalent to using files(pgnresource_package).joinpath(pgnresource_filename)
    # The function call importlib.resources.files(pgnresource_package) returns an importlib.resources.abc.Traversable
    # object representing the resource container for the package (think directory) and its resources (think files). A
    # Traversable may contain other containers (think subdirectories). 
    resource_location_as_string = files(pgnresource_package) / pgnresource_filename

    string_read_from_file = resource_location_as_string.read_text()

    # # Find index of first character after a blank line (where I assume that the only way a blank line occurs is as two
    # # adjacent newline characters—i.e., there is no white space separarting the two newline characters).
    # index_of_first_newline_of_a_consecutive_pair = string_read_from_file.find("\n\n")

    # if index_of_first_newline_of_a_consecutive_pair == -1:
    #     raise ReportError("Error in PGN: No blank line (two consecutive newline characters) found.")

    # # Index of first character after the pair of consecutive newline characters is two characters beyond the
    # # occurrence of the first of the pair of newline characters
    # index_of_first_char_after_blank_line = index_of_first_newline_of_a_consecutive_pair + 2

    # relevant_portion_of_string = string_read_from_file[index_of_first_char_after_blank_line::]

    # # Remove any beginning white space
    # relevant_portion_of_string = relevant_portion_of_string.lstrip()

    return string_read_from_file


def find_next_blank_line(string, index_to_start):
    """
    # Returns index of first newline character of a pair of consecutive newline characters, where the scan begins at
    # index_to_start
    # I assume that the only way a blank line occurs is as two adjacent newline characters—i.e., there is no white space
    # separating the two newline characters).
    #
    # If a pair of consecutive newline characters is not found, the return value will be -1
    """
    index_of_first_newline_char_of_a_pair = string.find("\n\n", index_to_start)
    return index_of_first_newline_char_of_a_pair


def strip_headers_from_pgn_file(string_read_from_file, pgn_source):
    (start_index, end_index) = id_text_between_first_two_blankish_lines(string_read_from_file)

    if start_index is None:
        pgn_error_no_blank_line_after_headers(pgn_source)
    
    if end_index is None:
        movetext_string = string_read_from_file[start_index::]
    else:
        movetext_string = string_read_from_file[start_index: end_index:]
    
    # Remove any remaining leading white space
    movetext_string = movetext_string.lstrip()

    return movetext_string
    



# def strip_headers_from_pgn_file(string_read_from_file, pgn_source):
#     """
#     Takes string read from PGN file and prepares it for tokenizing by:
#         Skips over initial set of headers, followed by a blank line. The next text is the beginning of the relevant
#             movetext.
#         Searches for a second game in the PGN by searching for a subsequent blank line.
#         Returns the text between the beginning of the relevant movetext and any subsequent blank line.
#     pgn_source is passed here solely to allow it to be used in error messages. (Seems less than ideal.)
#     """

#     # Search for first blank line, which should be the line immediately following the series of headers
#     index_of_first_newline_of_a_consecutive_pair = find_next_blank_line(string_read_from_file, 0)

#     if index_of_first_newline_of_a_consecutive_pair == -1:
#         # Two consecutive newline characters not found
#         pgn_error_no_blank_line_after_headers(pgn_source)
#         # pgn_error_fatal_error("No blank line (two consecutive newline characters) found.", pgn_source)
#         # raise ReportError("Error in PGN: No blank line (two consecutive newline characters) found.")

#     # Index of first character after the pair of consecutive newline characters is two characters beyond the
#     # occurrence of the first of the pair of newline characters
#     index_of_first_char_after_blank_line = index_of_first_newline_of_a_consecutive_pair + 2

#     # Search for a subsequent blank line separating the first game from a second game
#     index_subsequent_blank_line = find_next_blank_line(string_read_from_file, index_of_first_char_after_blank_line)

#     # The desired substring is a slice
#     # The end of the slice is either (a) the first newline char of a pair of consecurity newline chars or (b) is -1.
#     # because find_next_blank_line didn't find a next blank line. In that case, the -1 as the end of the slice indicates
#     # the last character of the string.
#     movetext_string = string_read_from_file[index_of_first_char_after_blank_line:index_subsequent_blank_line:]

#     # Remove any remaining leading white space
#     movetext_string = movetext_string.lstrip()

#     return movetext_string


def tokenize_pgnstring(pgnstring):
    """
    Parse string into a list of tokens, either a movetext entry (e.g., "Nf3"), “(”, or “)”. Return the list.
    """
    # Bursts the string at each space
    tokenlist = pgnstring.split()

    # Strips any move-number indication (e.g., “2.” or “6...”) from a movetext token that precedes the movetext itself.
    # This skips over tokens that are either “(” or “)”, which are not movetext tokens.
    # for token in tokenlist:
    #    token = strip_leading_movenumber_indication(token)

    # See https://www.geeksforgeeks.org/python-change-list-item/

    tokenlist = [strip_leading_movenumber_indication(token) for token in tokenlist]

    # Removes any empty token
    # See, e.g., https://www.geeksforgeeks.org/python-remove-empty-strings-from-list-of-strings/
    #
    # An empty token can occur, e.g., with the “*” at the end or if a move-number indication is in a separate component
    # of the burst string from its movetext).
    # Note: If the PGN is in “export format,” there will be no space between the move-number indication and the
    # move. In this case, each burst component will have the movenumber and movetext together. 
    # Otherwise, a component may have ONLY the move-text indicator, and this string will be converted to the
    # empty string by strip_leading_movenumber_indication(). This is OK, as empty strings are stripped out.
    #
    # NOTE: An empty string is considered False.
    tokenlist = [token for token in tokenlist if token]

    return tokenlist

def strip_leading_movenumber_indication(string_to_strip):
    """
    Strips leading move-number indication (e.g., “2.” or “4...”) from supplied movetext token. Returns stripped string. 
    """
    # Requirements
    # import re  # Requires re package to be imported by the module.

    # Use regular expression to strip all non-alpha leading characters, except for “(” and “)”, from string.
    # Adapted the answer from https://stackoverflow.com/a/31034061/8401379, which strips non-alphanumeric characters.

    # Compiles pattern
    regex_pattern = re.compile(r"^[^A-Za-z()]+")

    # Finds characters matching pattern and replaces them with null character
    #   See, e.g., https://medium.com/@zohaibshahzadTO/regular-expressions-sub-method-and-verbose-mode-1902cbc0ceef

    stripped_string = regex_pattern.sub("",string_to_strip)

    return stripped_string


def pgn_file_not_found_fatal_error(user_pgn_filepath, original_error_message):
    """
    Called when user-specified file could not be found at path specified in CLI argument. This is a fatal error.
    Program exits with no traceback information.
    """
    basename = user_pgn_filepath.name
    path_fo_file = str(user_pgn_filepath.parent)
    errmsg_list = []
    errmsg_list.append("FileNotFoundError")
    errmsg_list.append("PGN file specified on command line could not be found:\n")
    errmsg_list.append(f"Could not find a file “{basename}” at the user-specified path:\n")
    errmsg_list.append(f"{path_fo_file}\n")
    errmsg_list.append(f"Please try again by calling “{constants.entry_point_name}” with either ")
    errmsg_list.append("(a) a different file path or (b) no argument at all to use a default PGN file.")
    errmsg_list.append(f"\nOriginal error message = “str({original_error_message})”")
    error_message = "".join(errmsg_list)
    fatal_error_exit_without_traceback(error_message)


def pgn_error_no_blank_line_after_headers(pgn_source):
    errmsg_list = []
    errmsg_list.append("No blank line found after headers.\n")
    error_message = "".join(errmsg_list)
    fatal_pgn_error(error_message, pgn_source)