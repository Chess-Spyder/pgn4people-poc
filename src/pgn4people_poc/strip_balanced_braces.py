"""
Module for strip_balanced_braces_from_string()
"""

from . error_processing import fatal_pgn_error

def strip_balanced_braces_from_string(string_to_strip):
    """
    Take a string and remove all balanced-braced expressions and return the new stripped string.

    Methodology:
        Search for a first left brace.
        Save the substring from the beginning of the string until just before the first left brace to
            list_of_substrings.
        Starting immediately after the first left brace, iterate over each next brace (whether left brace or right
        brace), incrementing/decrementing the brace-imbalance counter, until brace neutrality is restored.
        Now that brace neutrality is restored, start searching for the next left brace immediately after the end of the
        just found brace-balanced expression.
        Rinse/repeat.
        When the supplied string is exhausted, join list_of_substrings into a new string and return. 
    """

    list_of_substrings = []
    left_brace = "{"
    right_brace = "}"

    def save_current_substring(start, end):
        """
        Appends substring of string_to_strip defined by start and end to list_of_substrings.

        Operates on string_to_strip in the enclosing scope.
        """
        # if end < start, returns with no action
        if end >= start:
            substring = string_to_strip[start:end:]
            list_of_substrings.append(substring)
    

    def skip_over_remainder_of_balanced_expression(index_after_first_left_brace):
        """
        Operates on string_to_strip in the enclosing scope.

        Returns index_end_of_brace_balanced_expression.
        
        Called (a) from an immediately previously brace-balanced state and (b) immediately after encountering a
        left-brace.

        When the left-brace was encountered at index n, this function should be called with
        argument index_after_first_left_brace=n+1; i.e., start is the index of the second character of the
        brace-enclosed expression, immediately after its first left brace.

        Raise ValueError if brace-balance is not restored before reaching the end of string_to_strip.
        """

        # By assumption, (a) braces were balanced (net_left_braces = 0) until (b) a left brace was just 
        # encountered. Thus we set net_left_braces = 1 to reflect the imbalance.
        net_left_braces = 1

        base_index_for_search = index_after_first_left_brace

        while net_left_braces > 0:
            # Scans for next occurrence of a left brace or a right brace
            search_result = scan_for_next_brace(string_to_strip, base_index_for_search, left_brace, right_brace)
            index_found, is_right_brace, is_left_brace = search_result
            if index_found == -1:
                # No additional brace is found. Thus the left brace that triggered the call to this function is
                # an unmatched left brace
                error_message_pt_1 = f"PGN terminated with a still-unmatched left brace, “{{”, "
                error_message_pt_2 = f"encountered at index {index_after_first_left_brace-1}."
                fatal_pgn_error(error_message_pt_1 + error_message_pt_2)
            if is_right_brace:
                # A right brace decreases the brace imbalance
                net_left_braces -= 1
            elif is_left_brace:
                # A left brace increases the brace imbalance
                net_left_braces += 1

            # Sets the index for next brace search to the character immediately after the brace just found
            base_index_for_search = index_found + 1
        
        # Reached after falling through while loop and thus brace balance has been restored.
        # This can occur only when the just-found character was a right brace.
        return index_found
        
    ####################################################################################################################
    # Main loop of function.    
    beginning_of_current_substring = 0
    while beginning_of_current_substring < len(string_to_strip):
        # This is reached only in a balanced-brace state
        # Search for a left brace that begins a brace-enclosed expression
        search_result = scan_for_next_brace(string_to_strip, beginning_of_current_substring, left_brace, right_brace)
        index_found, is_right_brace, is_left_brace = search_result
        if is_right_brace:
            fatal_pgn_error(f'Unexpected excess right brace, “}}”, encountered at index {index_found}.')
        if index_found == -1:
            # No more braces in the string. Save the current substring to the end.
            # Set end_of_current_substring to trigger the end of this while loop
            end_of_current_substring = len(string_to_strip)
            save_current_substring(beginning_of_current_substring, end_of_current_substring)
            break
        if is_left_brace:
            # Beginning of a brace-enclosed expression.
            # Save the substring leading up to the brace-enclosed expression.
            # Note that end_of_current_substring is used as the second element in a slice specification, thus the
            # slice ends at index one less than end_of_current_substring. This is why
            # end_of_current_substring = index_found, i.e., so that the slice ends the character before the left brace
            # was found.
            end_of_current_substring = index_found
            save_current_substring(beginning_of_current_substring, end_of_current_substring)

            # Skip to the end of the brace-balanced expression (if it is indeed brace balanced).
            # Start the scan at the character after the just-found left brace.
            # Set beginning_of_current_substring to the character after the end of this brace-balanced expression.
            # If the brace-enclosed expression is NOT brace balanced, skip_over_remainder_of_balanced_expression
            # throughs a PGN fatal error, and exits rather than returning here.
            beginning_of_current_substring = skip_over_remainder_of_balanced_expression(index_found + 1) + 1

    # Reached after falling through while loop. Thus every brace-enclosed expression was resolved as brace balanced
    # by the end of the string.
    stripped_string = "".join(list_of_substrings)
    return stripped_string


def scan_for_next_brace(string_to_scan, index_to_start_scan, left_brace, right_brace):
    """
    Search for the next brace, whether right or left, beginning at string_to_strip(index_to_start_scan).

    Arguments:
        string_to_scan
        index_to_start_scan: index to begin looking for a brace
        left_brace: string: character for left brace
        right_brace: string: character for right brace

    Returns a 3-tuple:
        (a) the index at which the next brace (left or right, whichever occurs first) is found
            If no brace is found, this is returned as -1.
        (b) is_right_brace = True iff the first-found brace is a right brace
        (c) is_left_brace = True iff the first-found brace is a left brace
    
    If both is_right_brace and is_left_brace are False, then there was no brace of any kind in this slice.
    """
    value_if_no_brace_found = -1

    index_left_brace_found = string_to_scan.find(left_brace, index_to_start_scan)
    index_right_brace_found = string_to_scan.find(right_brace, index_to_start_scan)

    if index_right_brace_found == -1:
        is_right_brace = False
        if index_left_brace_found == -1:
            is_left_brace = False
            index_found = value_if_no_brace_found
        else:
            is_left_brace = True
            index_found = index_left_brace_found
    else:
        if index_left_brace_found == -1:
            is_left_brace = False
            is_right_brace = True
            index_found = index_right_brace_found
        elif index_right_brace_found < index_left_brace_found:
            is_right_brace = True
            is_left_brace = False  
            index_found = index_right_brace_found
        else:
            is_right_brace = False
            is_left_brace = True  
            index_found = index_left_brace_found       

    return index_found, is_right_brace, is_left_brace