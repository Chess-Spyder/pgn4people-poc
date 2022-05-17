""" Utilities more general than those found in more-targeted utility modules """


from . utilities import ( is_even_number,
                          is_odd_number)

def ismovetext(string):
    """
    If the string is neither an open parenthesis, “(”, nor a closed parenthesis, “)”, it is deemed movetext.
    """

    logical_result = (string != "(") and (string != ")")
    return logical_result


def is_White_move(halfmovenumber):
    """
    Returns true if argument halfmovenumber is odd, and hence it corresponds to a move by White.
    """
    return is_odd_number(halfmovenumber)


def is_Black_move(halfmovenumber):
    """
    Returns true if argument halfmovenumber is even, and hence it corresponds to a move by Black.
    """
    return is_even_number(halfmovenumber)


def fullmovenumber_from_halfmove(halfmovenumber):
#   Given a halfmove number, returns fullmovenumber
#       “//” returns closest integer value that is ≤ the actual value
#       See https://www.geeksforgeeks.org/division-operator-in-python/
    fullmovenumber = (halfmovenumber + 1) // 2
    return fullmovenumber