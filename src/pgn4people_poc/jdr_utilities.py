"""
Checks argument on command line for a path to a user-supplied PGN file.
"""

import argparse
import pathlib
import re

# Note: check_CLI_for_user_file belongs to jdr_utilities
def check_CLI_for_user_file(description=None, epilog=None):

    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    
    # Defines argument
    #   nargs='?': One argument will be consumed from the command line if possible, and produced as a single item.
    #       If no command-line argument is present, the value from default will be produced.
    #   default=None: Unnecessary, because `default` defaults to `None`, but included for clarity.`
    parser.add_argument('user_textfile_path', nargs='?', default=None, type=pathlib.Path)

    # Parse argument(s)
    args = parser.parse_args()

    # Return a pathlib.Path object, which supports the open() method.
    # See https://docs.python.org/3/library/pathlib.html#pathlib.Path.open
    user_textfile_path = args.user_textfile_path

    return user_textfile_path


def id_text_between_first_two_blankish_lines (string_from_file):
    """
    Here, a “blank-ish” line is any of:
    (a) a pair of consecutive newline characters,
    (b) a newline character, followed by a string of only non-newline whitespace, followed by a newline character,
    (c) a newline character, followed by a string of only non-newline whitespace, followed by an end of file

    (As implemented, however, consecutive blank-ish lines are treated as a single blank-ish line. This is a feature,
    not a bug.)

    When passed string_from_file, this function determines the start and stop indices such that the slice
    `string_from_file[start: end::]` contains exactly the text between the pair of blank-ish lines.

    Returns the 2-tuple (start_index, end_index), where these are interpreted in the same way as a Python string slice.

    If there is only an initial blank-ish line (or set of consecutive blank-ish lines), but not two, start_index will be
    returned with the index of the beginning of the text after the blank-ish line, but end_index will be returned as
    None. In this case, the desired text is a slice that begins at start_index but runs through the end of the string.

    If the file is empty or otherwise has no blank-ish line, both elements of the 2-tuple will be returned as None.

    Usage example:
        (start_index, end_index) = id_text_between_first_two_blankish_lines(string_from_file)
        if start_index is None:
            print("No match found. Invalid file.")
        elif end_index is not None:
            print(f"Desired text spans {start_index}–{end_index}:")
            print_selected_string(string_from_file[start_index: end_index:])
        else:
            print(f"Desired text begins at {start_index} and runs till the end of the file:")
            print_selected_string(string_from_file[start_index::])

    Designed to be tested and demo-ed with the program <run_id_text_between_first_two_blankish_lines.py> and files in:
        jdr-utilities/tests/run_id_text_between_first_two_blankish_lines
    in the repository:
        https://github.com/jimratliff/jdr-python-utilities

    Context (the application for which this was developed): A standards-conformant PGN file has:
    (a) headers for game 1
    (b) a blank line
    (c) movetext for game 1
    (d) a blank line
    (e) headers for game 2
    etc.

    When passed string_from_file, this function determines the start and stop indices such that the slice
    `string_from_file[start: end::]` contains exactly the desired movetext for game 1 in component (c) above.

    The PGN “output standard” requires that “a single blank line appears after the last of the tag pairs to conclude the
    tag pair section. This helps simple scanning programs to quickly determine the end of the tag pair section and the
    beginning of the movetext section.”
    http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm#c8.1.1

    This implementation relaxes this standard in two ways:
    (a) permits a “blank-ish” line (one with non-newline whitespace between two consecutive newline characters) rather
    than requires a blank line.
    (b) permits multiple consecutive blank-ish lines even when the standard specifies a single blank line.

    (This is in the spirit of being more permissive on input than output.)

    Although the PGN standard requires that the blank line be strictly empty, this function accepts other whitespace
    characters on the blank line. (Such a line is “blank-ish.”)

    Note: Because this is implemented with a regex that is greedy, it will gobble up as many consecutive blank-ish lines
    in component (b) as exist. In other words, even though such a file strictly violates the standard (by having more 
    that one blank line after the headers), it will not create an error. 
    """

    # Define regex pattern
    # Regex pattern matches a string characterized by:
    # (a) a newline (\n) character followed by
    # (b) zero or more (“*” quantifier) whitespace (\s) characters, followed by
    #       Because the “*” isn’t followed immediately by a “?”, this is greedy. Thus it will keep gobbling, even if
    #       it encounters a newline, as long as there is a later newline still within the matching text (i.e., with 
    #       nothing but whitespace preceding it). Greediness is relevant here because the outer delimiting characters
    #       (viz., newline chars) also themselves qualify as whitespace (the filling between the newline bread in this
    #       sandwich).
    # (c) a newline character OR end of string ($)
    #
    # The prefixing “r” specifies that regex_pattern is a “raw string” and thus backslashes are not seen as 
    # Python escape characters. See https://docs.python.org/3/howto/regex.html#the-backslash-plague

    regex_pattern = r"\n\s*(\n|$)"

    # I compile the regex because I believe only the compiled regular expression object can be used in the below syntax:
    #       for match in compiled_regex_pattern.finditer(string_from_file):
    # Otherwise, I think you'd have to use something (untested) like:
    #       iterable = re.match(regex_pattern, string_from_file)
    compiled_regex_pattern = re.compile(regex_pattern)

    # Return an iterator yielding match objects over all non-overlapping matches for the RE pattern in string.
    # See https://docs.python.org/3/library/re.html#re.finditer
    # re.finditer(pattern, string, flags=0)

    iterator_of_matches = compiled_regex_pattern.finditer(string_from_file)
    # First match
    match = next(iterator_of_matches, None)
    if match is not None:
        # The end of the first match is the beginning of the desired text. (Recall that the end_index of the first
        # match is not actually reached by the first match; thus it is the beginning of the following text.)
        start_index = match.end()
        # Second match
        match = next(iterator_of_matches, None)
        if match is not None:
            # The beginning of the second match is one character after the end of the desired movetext, thus the second
            # index of the slice for the desired text is precisely the beginning of the second match (because the
            # slice will stop before reaching the second index).
            end_index = match.start()
        else:
            end_index = None
    else:
        start_index = None
        end_index = None

    return (start_index, end_index)