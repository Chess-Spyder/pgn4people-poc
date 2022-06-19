"""
Error-processing functions
"""


import sys

from yachalk import chalk


def format_error_text(string):
    """
    Formats as red text a string that is intended as an error message in order to stand out in the console
    """

    formatted_string = chalk.red_bright(string)
    return formatted_string


def print_nonfatal_error(string):
    """
    Prints an error message for a nonfatal error
    """

    print(format_error_text(string))


def fatal_error_exit_without_traceback(string):
    """
    Print an error message for a fatal error, and exit without traceback

    Exits without throwing a traceback to the user. (A traceback gives scary info that's irrelevant to the user
    (e.g., where in the code the exception occurred.)
    """

    errmsg_list = []
    errmsg_list.append(f"FATAL ERROR! 💩 ")
    errmsg_list.append(str(string))
    errmsg_list.append("\nI must exit. Buh bye! 😘")
    error_message = "".join(errmsg_list)

    print(format_error_text(error_message))
    sys.exit(1)


def fatal_pgn_error(string, pgn_source = None):
    """
    Reports fatal error in PGN file being processed. Program exits without traceback.

    string:     Error message specific to this particular instance of a fatal PGN error.
    pgn_source: An instance of class PGNSource, containing information about the PGN being processed, whether it's the
                built-in sample PGN or the file specified by the user in a command-line argument. If the CLI-specified
                file, contains the path of the file.
    """
    errmsg_list = []
    errmsg_list.append(f"PGN ERROR: {string}")

    if pgn_source is not None:
        if pgn_source.is_sample_pgn:
            errmsg_list.append(f"\nThe error arose in the built-in sample PGN. Thus, this is a DEVELOPER ERROR! 😳")
        else:
            errmsg_list.append(f"\nThe problem arose in the PGN file you specified on the command line, viz.:\n")
            errmsg_list.append(str(pgn_source.path_to_pgnfile))

    error_message = "".join(errmsg_list)
    fatal_error_exit_without_traceback(error_message)


def fatal_developer_error(string):
    """
    Raises fatal developer error: An error that should NOT occur under any conceivable set of user inputs. It can result
    only from developer error or an erroneous understanding of, or assumption by, the developer.
    """

    errmsg_list = []
    errmsg_list.append("\nFATAL DEVELOPER ERROR. THIS SHOULD NOT HAPPEN! 🙀")
    if string:
        errmsg_list.append("\n" + string)
    error_message = "".join(errmsg_list)
    print(format_error_text(error_message))
    raise FatalDeveloperError(error_message)


class FatalDeveloperError(RuntimeError):
    pass