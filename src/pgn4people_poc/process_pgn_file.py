"""
Functions to help parse PGN file of a chess game.
"""
from build_tree import buildtree
import re

def get_pgn_string(pgnfilepath):
    """ Read raw PGN file into string."""

    # Read raw PGN file into string
    pgnstring = read_pgnfile_into_string(pgnfilepath)

    return pgnstring


def build_tree_from_pgnstring(pgnstring):
    """ Takes string of PGN, tokenize it, and build tree from it. Return dictionary of nodes."""


    # Parse string into a list of tokens, either (a) a movetext entry (e.g., "e4"), (b) “(”, or (c) “)”.
    tokenlist = tokenize_pgnstring(pgnstring)

    # Build tree from tokenlist
    nodedict = buildtree(tokenlist)

    return nodedict


def read_pgnfile_into_string(pgnfilepath):
    """
    Read raw PGN text file pgnfilepath and return its non-header contents as a character string.

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
        filedata = currentpgnfile.read()
    return filedata


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