"""
Asks for, receives, parses, and iterates until satisfactory input from user

"""

from . import constants
from . utilities import (format_nonfatal_error_text,
                         num_from_alpha)


def get_node_id_move_choice_for_next_line_to_display(fullmovenummber_to_node_id_lookup_table):
    """
    Ask user to supply a (fullmovenumber, player color, move-choice letter) triple for the next line to explore.

    Returns the node_id and the numeric index (zero-index) of the chosen move at that node
    """

#   Eligible answers for player-color response are expressed only in lowercase, because user input is
#   lower-cased prior to validating
    white_player_color_response_string_set = {"w", "white"}
    black_player_color_response_string_set = {"b", "black"}

#   Construct long string by concatenation
    request_to_user_part_1 = "\nEnter on one line, each separated by a space:\n"
    request_to_user_part_2 = "(a) move number,\n(b) player color, ‘W’ or ‘B’, "
    request_to_user_part_3 = "and\n(c) move choice (e.g., ‘a’, ‘b’, ‘c’, etc.),\nor 'reset', 'report', 'nodereport' or 'stop':\n"
    request_to_user = request_to_user_part_1 + request_to_user_part_2 + request_to_user_part_3

#   Initialize booleans for checking validity of user input
    request_pending = True

    is_valid_key = False
    is_valid_alpha_move_choice = False
    is_fullmovenumber_numeric = False
    is_valid_player_color = False
    is_a_single_alpha = False

#   Get user input, parse it while checking its validity
    while request_pending:
#       Pose request to user and get user response
        user_response_string = input(request_to_user)
        response_list = user_response_string.split()
        number_of_fields_in_response = len(response_list)
        if number_of_fields_in_response > 0:
            lowercase_response = response_list[0].lower()
#           Test whether user wants to stop
            if lowercase_response.startswith(constants.STOP_SIGN):
                return constants.STOP_SIGN, None
#           Test whether user wants to reset to the initial node
            if lowercase_response.startswith(constants.RESET_COMMAND):
                return constants.RESET_COMMAND, None
#           Test whether user wants a report characterizing the size and complexity of the tree
            if lowercase_response.startswith(constants.REPORT_COMMAND):
                return constants.REPORT_COMMAND, None
#           Test whether user wants a node-by-node report of its attributes
            if lowercase_response.startswith(constants.NODEREPORT_COMMAND):
                return constants.NODEREPORT_COMMAND, None
#       User didn't request to stop, reset, or produce a report
        if number_of_fields_in_response != 3:
#           When the number of fields supplied is wrong, we don't even try to assess the validity of the first three.
            report_input_errors_to_user(response_list,
                                        is_fullmovenumber_numeric,
                                        is_valid_player_color,
                                        is_a_single_alpha,
                                        is_valid_key,
                                        is_valid_alpha_move_choice)
        else:
#           Parse components from user's response
            fullmovenumber, player_color, alpha_move_choice  = response_list

#           Validate that first field is at least numeric
            is_fullmovenumber_numeric = fullmovenumber.isdigit()

#           Validate player color (only to extent that input expresses a player color, not to whether
#           that particular color is appropriate in the full context)
            player_color_lower = player_color.lower()
            if player_color_lower in black_player_color_response_string_set:
                player_color_string = "B"
                is_valid_player_color = True
            elif player_color_lower in white_player_color_response_string_set:
                player_color_string = "W"
                is_valid_player_color = True
            else:
                is_valid_player_color = False

#           Validate that third field is a single alpha character
            is_a_single_alpha = (len(alpha_move_choice) == 1) and (alpha_move_choice.isalpha())

#           Validate that (fullmovenumber, player_color) is a valid key
            if is_valid_player_color and is_fullmovenumber_numeric:

#               NOTE:   Absent wrapping fullmovenumber within int(…), it appeared as a string in the query, and thus
#               didn't match the actual keys in the dictionary, where the first element of the key's tuple was
#               an integer
                key_to_query_lookup_table = int(fullmovenumber) , player_color_string
#               NOTE: is_valid_key was already initialized to False above because the following calculation occurs only
#               in when both is_valid_player_color and is_fullmovenumber_numeric were found to be true.
                is_valid_key = key_to_query_lookup_table in fullmovenummber_to_node_id_lookup_table.keys()

#           Validates user's choice of move                
            if is_valid_key and is_a_single_alpha:
                numeric_move_choice = num_from_alpha(alpha_move_choice)
                node_id_selected, number_of_choices = fullmovenummber_to_node_id_lookup_table[key_to_query_lookup_table]
#               Checks that single-char alpha is not above the range available at this node
                is_valid_alpha_move_choice = numeric_move_choice <= number_of_choices

#           Assesses whether user response was satisfactory
            if is_valid_alpha_move_choice:
#               This was the last hurdle. User response was satisfactory.
                request_pending = False
            else:
#               Informs user there are errors in her input and invites her to try again
                report_input_errors_to_user(response_list,
                                            is_fullmovenumber_numeric,
                                            is_valid_player_color,
                                            is_a_single_alpha,
                                            is_valid_key,
                                            is_valid_alpha_move_choice)


#           End of while loop to successfully obtain valid user input

#   Return the node_id and numeric_move_choice (adjusted to zero-index)
    return node_id_selected, numeric_move_choice

def report_input_errors_to_user(response_list,
                                is_fullmovenumber_numeric,
                                is_valid_player_color,
                                is_a_single_alpha,
                                is_valid_key,
                                is_valid_alpha_move_choice):
    """
    Takes errors identified in get_node_id_move_choice_for_next_line_to_display() and reports them to user
    and invites her to try again.
    """
    number_of_fields_in_response = len(response_list)
    if number_of_fields_in_response == 0:
        print(format_nonfatal_error_text("Empty response. Enter ‘stop’ if you want to stop."))
    elif number_of_fields_in_response != 3:
        good_grammar_string = "field" if number_of_fields_in_response == 1 else "fields"
        error_message = f"I expected 3 fields. You entered {number_of_fields_in_response} {good_grammar_string}."
        print(format_nonfatal_error_text(error_message))
    else:
#       There were exactly three fields but nonetheless there is at least one error.
#       Tabulates number of errors
#       Note: Calculation relies on fact that True == 1.
        number_of_errors = (not is_fullmovenumber_numeric) + (not is_valid_player_color) + (not is_a_single_alpha)

#       An invalid key is a separate error only if the individual components of the key were each valid on its own.
#       (Otherwise the invalidity of the key is just a consequence of one or both of the component invalidities.)
        is_invalid_key = (not is_valid_key) and is_fullmovenumber_numeric and is_valid_player_color
        if is_invalid_key:
            number_of_errors += 1

#       If key is valid, checks is_valid_alpha_move_choice (i.e., that alpha supplied is in permissible range for
#       the key)
        is_alpha_out_of_range = is_valid_key and (not is_valid_alpha_move_choice)
        if is_alpha_out_of_range:
            number_of_errors += 1

#               Construct grammatically correct characterization of number of errors
        string_number_of_errors = "was one error" if number_of_errors == 1 else f"were {number_of_errors} errors"
        
        number_of_errors_message = "There " + string_number_of_errors + " in your input:"
        print(format_nonfatal_error_text(number_of_errors_message))

#               Itemize errors to user
        if not is_fullmovenumber_numeric:
            not_numeric_message = f"The first field, “{response_list[0]}”, was not numeric, but should have been."
            print(format_nonfatal_error_text(not_numeric_message))
        
        if not is_valid_player_color:
            bad_color_message = f"The second field, “{response_list[1]}”, did not indicate a valid player color."
            print(format_nonfatal_error_text(bad_color_message))
        
        if not is_a_single_alpha:
            not_single_alpha_message = f"The third field, “{response_list[2]}”, should have been a single letter."
            print(format_nonfatal_error_text(not_single_alpha_message))

        if is_invalid_key:
            not_valid_key_message_part_1 = f"The combination of fullmovenumber {response_list[0]} "
            not_valid_key_message_part_2 = f"and player color {response_list[1]} was not a valid combination here."
            print(format_nonfatal_error_text(not_valid_key_message_part_1 + not_valid_key_message_part_2))

        if is_alpha_out_of_range:
            alpha_out_of_range_message_part_1 = f"The move choice “{response_list[2]}” is not available for this "
            alpha_out_of_range_message_part_2 = f"combination of move # ({response_list[0]}) and "
            alpha_out_of_range_message_part_3 = f"color ({response_list[1]})."
            print(format_nonfatal_error_text(alpha_out_of_range_message_part_1
                                                + alpha_out_of_range_message_part_2
                                                + alpha_out_of_range_message_part_3))
#   End of branches. Now invite user to try again.
    print(format_nonfatal_error_text("Please try again."))







