"""
Functions to help parse PGN file of a chess game.
"""

from importlib.resources import files
import re

from . build_tree import buildtree
from . import constants
from . utilities import ReportError

def acquire_pgnstring():
    """
    Get string of PGN from built-in PGN file or other source
    """
    # Which of the available sample PGNs is to be read
    pgnfilepath = constants.CHOSEN_SAMPLE_PGN_FILE

    # Branches depending on whether sample PGN file is to be read (a) from the file system or (b) as a resource
    if constants.DO_READ_PGN_FROM_FILE_SYSTEM:
        pgnstring = read_filesystem_pgnfile_into_string(constants.PATH_TO_CHOSEN_SAMPLE_PGN_FILE)
    else:
        pgnstring = read_resource_pgnfile_into_string(constants.PACKAGE_FOR_SAMPLE_PGN,
                                                      constants.CHOSEN_SAMPLE_PGN_FILE)
    if not pgnstring:
        raise ReportError("Error in PGN: No valid movetext found.")
    return pgnstring


def build_tree_from_pgnstring(pgnstring):
    """ Takes string of PGN, tokenize it, and build tree from it. Return dictionary of nodes."""


    # Parse string into a list of tokens, either (a) a movetext entry (e.g., "e4"), (b) “(”, or (c) “)”.
    tokenlist = tokenize_pgnstring(pgnstring)

    # Build tree from tokenlist
    nodedict = buildtree(tokenlist)

    return nodedict


def read_filesystem_pgnfile_into_string(pgnfilepath):
    """
    Read raw PGN text file on the file system (as opposed to a package resource) and return its non-header contents as a
    character string.

    Skips over tag-pair header section (by advancing until the first blank line is reached), thus considers only the
    first game in a multi-game PGN file.

    Assumes that textual comments have already been stripped by the user before being provided to pgnfocus to be read.
    """
    with open(pgnfilepath, "r") as currentpgnfile:
        # Iterate through each line in the file until an entirely whitespace line is found.
        # This results in the pointer into the file being located after the tag-pair header section.
        # See https://stackoverflow.com/a/11873623/8401379
        # Note: The .isspace() string method returns `True` iff all characters in the string are
        #     whitespace characters, where these include the newline `\n` character

        next(line for line in currentpgnfile if line.isspace())

        #   Read the remaining (non-header) data in the file and return it as a string.
        string_read_from_file = currentpgnfile.read()
    return string_read_from_file


def read_resource_pgnfile_into_string(pgnresource_package, pgnresource_filename):
    """
    Read raw PGN text file that is present as a packaged resource (rather than guaranteed to be on the file system) and
    return its non-header contents as a character string.

    Skips over tag-pair header section by finding the first non-whitespace character after the first “blank line,”
    defined by two consecutive newline characters. (Note that this is not very robust: Even a single whitespace
    character (other than a newline character) between the pair of newline characters will cause the blank line to fail
    to be detected.
    
    Considers only the first game in a multi-game PGN file.

    Assumes that textual comments have already been stripped by the user before being provided to pgnfocus to be read.
    """

    # Constructs a chained package representation of the location of the desired sample PGN file
    #
    # The following “/” syntax is equivalent to using files(pgnresource_package).joinpath(pgnresource_filename)
    # The function call importlib.resources.files(pgnresource_package) returns an importlib.resources.abc.Traversable
    # object representing the resource container for the package (think directory) and its resources (think files). A
    # Traversable may contain other containers (think subdirectories). 
    resource_location_as_string = files(pgnresource_package) / pgnresource_filename

    string_read_from_file = resource_location_as_string.read_text()

    # Find index of first character after a blank line (where I assume that the only way a blank line occurs is as two
    # adjacent newline characters—i.e., there is no white space separarting the two newline characters).
    index_of_first_newline_of_a_consecutive_pair = string_read_from_file.find("\n\n")

    if index_of_first_newline_of_a_consecutive_pair == -1:
        raise ReportError("Error in PGN: No blank line (two consecutive newline characters) found.")

    # Index of first character after the pair of consecutive newline characters is two characters beyond the
    # occurrence of the first of the pair of newline characters
    index_of_first_char_after_blank_line = index_of_first_newline_of_a_consecutive_pair + 2

    relevant_portion_of_string = string_read_from_file[index_of_first_char_after_blank_line::]

    # Remove any beginning white space
    relevant_portion_of_string = relevant_portion_of_string.lstrip()

    return relevant_portion_of_string


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