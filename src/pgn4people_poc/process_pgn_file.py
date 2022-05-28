"""
Functions to help parse PGN file of a chess game.
"""

from importlib.resources import files
import re

from . import constants
from . process_CLI import check_CLI_for_user_pgnfile
from . utilities import ReportError
from . strip_balanced_braces import strip_balanced_braces_from_string

def acquire_tokenized_pgnstring():
    """
    Get string of PGN from either (a) file specified by user in command line or (b) a built-in PGN file,
    strips the headers, and tokenizes the remaining movetext.
    """

    # Checks command line to see whether user specified her own PGN file to view
    # user_pgn_fileobject will be either (a) a file object or (b) None
    # user_pgn_fileobject = check_CLI_for_user_pgnfile_using_FileType()
    user_pgn_filepath = check_CLI_for_user_pgnfile()

    if user_pgn_filepath is None:
        # User didn't specify her own PGN file, so use sample PGN file included in the package
        string_read_from_file = read_resource_pgnfile_into_string(constants.PACKAGE_FOR_SAMPLE_PGN,
                                                                  constants.CHOSEN_SAMPLE_PGN_FILE)
    else:
        # string_read_from_file = user_pgn_fileobject.read()
        with user_pgn_filepath.open('r') as file:
            string_read_from_file = file.read()
    
    pgnstring = strip_headers_from_pgn_file(string_read_from_file)

    pgnstring = strip_balanced_braces_from_string(pgnstring)

    if not pgnstring:
        raise ReportError("Error in PGN: No valid movetext found.")
   
    # Parse string into a list of tokens, either (a) a movetext entry (e.g., "e4"), (b) “(”, or (c) “)”.
    tokenlist = tokenize_pgnstring(pgnstring)

    return tokenlist


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


def strip_headers_from_pgn_file(string_read_from_file):
    """
    Takes string read from PGN file and strips the headers to return a string ready for tokenizing.

    Assumes that textual comments have already been stripped by the user before being provided to pgnfocus to be read.
    """
    # Find index of first character after a blank line (where I assume that the only way a blank line occurs is as two
    # adjacent newline characters—i.e., there is no white space separating the two newline characters).
    index_of_first_newline_of_a_consecutive_pair = string_read_from_file.find("\n\n")

    if index_of_first_newline_of_a_consecutive_pair == -1:
        # Two consecutive newline characters not found
        raise ReportError("Error in PGN: No blank line (two consecutive newline characters) found.")

    # Index of first character after the pair of consecutive newline characters is two characters beyond the
    # occurrence of the first of the pair of newline characters
    index_of_first_char_after_blank_line = index_of_first_newline_of_a_consecutive_pair + 2

    # The desired substring is a slice
    movetext_string = string_read_from_file[index_of_first_char_after_blank_line::]

    # Remove any remaining leading white space
    movetext_string = movetext_string.lstrip()

    return movetext_string


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