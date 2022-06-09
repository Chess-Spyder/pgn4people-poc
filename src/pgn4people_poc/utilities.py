""" Utilities more general than those found in more-targeted utility modules """

import os
import sys

from yachalk import chalk

from . import constants
# from . error_processing import format_error_text

def is_even_number(number):
    return (number % 2) == 0


def is_odd_number(number):
    return (number % 2) != 0


def lowercase_alpha_from_num(number):
    """
    Returns letter of the alphabet (lowercase) from an integer 1-26
    """
    import string
    SYMBOL_FOR_OUT_OF_RANGE_NUMBER = "∞"
    if number in range(1, 27):
        alpha = string.ascii_lowercase[number - 1]
        return alpha
    elif (isinstance(number, int) and number > 26):
        return SYMBOL_FOR_OUT_OF_RANGE_NUMBER
    else:
        fatal_developer_error(f"lowercase_alpha_from_num() says: Index to alphabet, {number}, invalid.")


def num_from_alpha(alphacharacter):
    """
    Returns number (1-26) from a letter of the alphabet (lowercase or uppercase)
    """
    if((alphacharacter.isalpha()) and (len(alphacharacter) == 1)):
        ord_string = ord(alphacharacter)
        if ord_string > 96:
#           Input was lower case
            numerical_equivalent = ord_string - 96
        else:
#           Input was upper case
            numerical_equivalent = ord_string - 64  
        return numerical_equivalent
    else:
        fatal_developer_error(f"num_from_alpha() says: String, “{alphacharacter}”, not a single alpha character.")


def clear_console():
    """
    Issues clear command to console, according to platform running
    """
    # See https://www.delftstack.com/howto/python/python-clear-console/
    
    clear_command_windoze = "cls"
    clear_command_mac_linux = "clear"
    if os.name in ("nt", "dos"):
        clear_command = clear_command_windoze
    else:
        clear_command = clear_command_mac_linux
    os.system(clear_command)


def conditionally_clear_console():
    if(constants.DO_CLEAR_CONSOLE_EACH_TIME):
        clear_console()


def wait_for_any_user_input():
    waiting = input(chalk.red_bright("\nPress <RETURN> to continue.\n"))


# class ReportError(Exception):
#     """ Base class for other exceptions """
#     def __init__(self, *args):
#         if args:
#             self.message = args[0]
#         else:
#             self.message = None
    
#     def __str__(self):
#         error_message = format_error_text('ERROR DETECTED')
#         print(error_message)
#         if self.message:
#             return 'ReportError, {0}, '.format(self.message)
#         else:
#             return 'ReportError has been raised'

def format_error_text(string):
    """
    Formats as red text a string that is intended as an error message that stands out in the console
    """

    formatted_string = chalk.red_bright(string)
    return formatted_string


def print_nonfatal_error(string):
    """
    Prints an error message for a nonfatal error
    """
    print(format_error_text(string))


def print_fatal_error_exit_without_traceback(string):
    """
    Prints an error message for a fatal error, and exit without traceback
    """
    errmsg_list = []
    errmsg_list.append(f"FATAL ERROR! 💩 ")
    errmsg_list.append(str(string))
    errmsg_list.append("\nI must exit. Buh bye! 😘")
    error_message = "".join(errmsg_list)

    print(format_error_text(error_message))
    # Exits without throwing a traceback to the user.
    # A traceback gives scary info that's irrelevant to the user (e.g., where in the code the exception
    # occurred.)
    sys.exit(1)

def pgn_error_fatal_error(string, pgn_source = None):
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
    print_fatal_error_exit_without_traceback(error_message)
    # print_fatal_error_exit_without_traceback("Howdy!")


def fatal_developer_error(string):
    """
    Raises fatal developer error: An error that should NOT occur under any conceivable set of user inputs. It can result
    only from developer error or an erroneous understanding of, or assumption by, the developer.
    """
    errmsg_list = []
    errmsg_list.append("FATAL DEVELOPER ERROR. THIS SHOULD NOT HAPPEN! 🙀")
    errmsg_list.append(string)
    print(format_error_text(errmsg_list))
    raise FatalDeveloperError


class FatalDeveloperError(Exception):
    pass