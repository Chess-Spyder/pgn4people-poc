""" Utilities more general than those found in more-targeted utility modules """

import os

from yachalk import chalk

from . import constants

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
        raise ReportError(f"lowercase_alpha_from_num() says: Index to alphabet, {number}, invalid.")


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
        raise ReportError(f"num_from_alpha() says: String, “{alphacharacter}”, not a single alpha character.")


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
    

def format_nonfatal_error_text(string):
    """
    Formats as red text a string that is intended as an error message that is nonfatal
    and thus does not “raise” an error.
    """

    formatted_string = chalk.red_bright(string)
    return formatted_string


class ReportError(Exception):
    """ Base class for other exceptions """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self):
        error_message = format_nonfatal_error_text('ERROR DETECTED')
        print(error_message)
        if self.message:
            return 'ReportError, {0}, '.format(self.message)
        else:
            return 'ReportError has been raised'
