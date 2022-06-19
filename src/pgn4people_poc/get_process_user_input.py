"""
Asks for, receives, parses, and iterates until satisfactory input from user
"""


import random

from yachalk import chalk

from . import constants
from . error_processing import print_nonfatal_error
from . utilities import (lowercase_alpha_from_num,
                         num_from_alpha)


def get_node_id_move_choice_for_next_line_to_display(fullmovenummber_to_node_id_lookup_table,
                                                     examples_command_triples_white,
                                                     examples_command_triples_black):
    """
    Ask user to supply (a) a (fullmovenumber, player color, move-choice letter) triple for the next line to explore or
    (b) one of several one-word keywords.

    If the user’s input isn’t valid, a report of the error(s) is output and the user is invited to try again.

    When valid input is provided by the user, this function returns (a) a flag for a chosen one-word keyword or (b) the
    node_id and the numeric index (zero-index) of the chosen move at that node.
    """


    # Determines whether there are any non-mainline moves for either player to choose
    if len(examples_command_triples_white) + len(examples_command_triples_black) > 0:
        is_some_mainline_move_available = True
    else: 
        is_some_mainline_move_available = False
    
    if not is_some_mainline_move_available:
        warning_string = ("\nHey! Your PGN doesn’t have alternatives for any player.\n"
                          f"{constants.entry_point_name} has nothing to offer for this PGN.\n"
                          f"{constants.entry_point_name} shines with more-complex games.\n"
                          "I hope you’ll try a different—and more interesting—PGN, so I can show my stuff!\n")
        print_nonfatal_error(warning_string)
    else:
        # Create sample command string to include in user prompt
        example_command_string = synthesize_combined_example_command_string(examples_command_triples_white,
                                                                            examples_command_triples_black)
 
        user_prompt_1 = ("\nEnter on one line, each separated by a space:\n"
                        "(a) move number,\n(b) player color, ‘W’ or ‘B’, "
                        "and\n(c) move choice (e.g., ‘a’, ‘b’, ‘c’, etc.),\n\n"
                        f"For example: {example_command_string}\n\n"
                        "OR "
                        )
    
    user_prompt_2 = "one of ‘reset’, ‘report’, ‘nodereport’, or ‘stop’:\n"

    if is_some_mainline_move_available:
        user_prompt = user_prompt_1 + user_prompt_2
    else:
        user_prompt = "Enter " + user_prompt_2

    # Eligible answers for player-color response are expressed only in lowercase, because user input is
    # lower-cased prior to validating
    white_player_color_response_string_set = {"w", "white"}
    black_player_color_response_string_set = {"b", "black"}

    # Initialize booleans for checking validity of user input
    request_pending = True

    is_valid_key = False
    is_valid_alpha_move_choice = False
    is_fullmovenumber_integer = False
    is_valid_player_color = False
    is_a_single_alpha = False

    # Get user input, parse it while checking its validity
    while request_pending:
        # Pose request to user and get user response
        user_response_string = input(user_prompt)
        response_list = user_response_string.split()

        number_of_fields_in_response = len(response_list)
        if number_of_fields_in_response > 0:
            lowercase_response = response_list[0].lower()
            # Test whether user wants to stop
            if lowercase_response.startswith(constants.STOP_SIGN):
                return constants.STOP_SIGN, None
            # Test whether user wants to reset to the initial node
            if lowercase_response.startswith(constants.RESET_COMMAND):
                return constants.RESET_COMMAND, None
            # Test whether user wants a report characterizing the size and complexity of the tree
            if lowercase_response.startswith(constants.REPORT_COMMAND):
                return constants.REPORT_COMMAND, None
            # Test whether user wants a node-by-node report of its attributes
            if lowercase_response.startswith(constants.NODEREPORT_COMMAND):
                return constants.NODEREPORT_COMMAND, None
        # User didn't request to stop, reset, or produce a report
        if number_of_fields_in_response != 3:
            # When the number of fields supplied is wrong, we don't even try to assess the validity of the first three.
            report_input_errors_to_user(response_list,
                                        is_fullmovenumber_integer,
                                        is_valid_player_color,
                                        is_a_single_alpha,
                                        is_valid_key,
                                        is_valid_alpha_move_choice)
        else:
            # Parse components from user's response
            fullmovenumber, player_color, alpha_move_choice  = response_list

            # Validate that first field is at least numeric
            is_fullmovenumber_integer = fullmovenumber.isdigit()

            # Validate player color (only to extent that input expresses a player color, not to whether
            # that particular color is appropriate in the full context)
            player_color_lower = player_color.lower()
            if player_color_lower in black_player_color_response_string_set:
                player_color_string = constants.BLACK_PLAYER_COLOR_STRING
                is_valid_player_color = True
            elif player_color_lower in white_player_color_response_string_set:
                player_color_string = constants.WHITE_PLAYER_COLOR_STRING
                is_valid_player_color = True
            else:
                is_valid_player_color = False

            # Validate that third field is a single alpha character
            is_a_single_alpha = (len(alpha_move_choice) == 1) and (alpha_move_choice.isalpha())

            # Validate that (fullmovenumber, player_color) is a valid key
            if is_valid_player_color and is_fullmovenumber_integer:

                # NOTE: Absent wrapping fullmovenumber within int(…), it appeared as a string in the query, and thus
                # didn't match the actual keys in the dictionary, where the first element of the key's tuple was
                # an integer
                key_to_query_lookup_table = int(fullmovenumber) , player_color_string
                # NOTE: is_valid_key was already initialized to False above because the following calculation occurs
                # only when both is_valid_player_color and is_fullmovenumber_numeric were found to be true.
                is_valid_key = key_to_query_lookup_table in fullmovenummber_to_node_id_lookup_table.keys()

            # Validates user's choice of move                
            if is_valid_key and is_a_single_alpha:
                numeric_move_choice = num_from_alpha(alpha_move_choice)
                node_id_selected, number_of_choices = fullmovenummber_to_node_id_lookup_table[key_to_query_lookup_table]
                # Checks that single-char alpha is not above the range available at this node
                is_valid_alpha_move_choice = numeric_move_choice <= number_of_choices

            # Assesses whether user response was satisfactory
            if is_valid_alpha_move_choice:
                # This was the last hurdle. User response was satisfactory.
                request_pending = False
            else:
                # Informs user there are errors in her input and invites her to try again
                report_input_errors_to_user(response_list,
                                            is_fullmovenumber_integer,
                                            is_valid_player_color,
                                            is_a_single_alpha,
                                            is_valid_key,
                                            is_valid_alpha_move_choice)

            # End of while loop to successfully obtain valid user input

    # Return the node_id and numeric_move_choice (adjusted to zero-index)
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
        print_nonfatal_error("Empty response. Enter ‘stop’ if you want to stop.")
    elif number_of_fields_in_response == 1:
        print_nonfatal_error(
            "Your one-field response was not one of the permitted keywords.\n"
            "(If you were trying to enter a (move number, player color, move choice) triple,\n"
            "use a space between each adjacent component, e.g., “3 W c” or “5 B a”.)")
    elif number_of_fields_in_response != 3:
        good_grammar_string = "field" if number_of_fields_in_response == 1 else "fields"
        error_message_1 = f"I expected 3 fields (or one of the permitted keywords) but "
        error_message_2 = f"you entered {number_of_fields_in_response} {good_grammar_string}."
        print_nonfatal_error(error_message_1 + error_message_2)
    else:
        # There were exactly three fields but nonetheless there is at least one error.
        # Tabulates number of errors
        # Note: Calculation relies on fact that True == 1.
        number_of_errors = (not is_fullmovenumber_numeric) + (not is_valid_player_color) + (not is_a_single_alpha)

        # An invalid key is a separate error only if the individual components of the key were each valid on its own.
        # (Otherwise the invalidity of the key is just a consequence of one or both of the component invalidities.)
        is_invalid_key = (not is_valid_key) and is_fullmovenumber_numeric and is_valid_player_color
        if is_invalid_key:
            number_of_errors += 1

        # If key is valid and is_a_single_alpha, checks is_valid_alpha_move_choice (i.e., that alpha supplied is in
        # permissible range for the key)
        is_alpha_out_of_range = is_valid_key and is_a_single_alpha and (not is_valid_alpha_move_choice)
        if is_alpha_out_of_range:
            number_of_errors += 1

        # Construct grammatically correct characterization of number of errors
        at_least_qualifier = "at least "
        if number_of_errors == 1:
            string_number_of_errors = f"was {at_least_qualifier}one error"
        else:
            string_number_of_errors = f"were {at_least_qualifier}{number_of_errors} errors"
        
        number_of_errors_message = "There " + string_number_of_errors + " in your input:"
        print_nonfatal_error(number_of_errors_message)

        # Itemize errors to user
        if not is_fullmovenumber_numeric:
            not_numeric_message = f"The first field, “{response_list[0]}”, was not an integer, but should have been."
            print_nonfatal_error(not_numeric_message)
        
        if not is_valid_player_color:
            bad_color_message = (
                f"The second field, “{response_list[1]}”, did not indicate a valid player color. "
                "Should be “W” or “B”."
                )
            print_nonfatal_error(bad_color_message)
        
        if not is_a_single_alpha:
            not_single_alpha_message = f"The third field, “{response_list[2]}”, should have been a single letter."
            print_nonfatal_error(not_single_alpha_message)

        if is_invalid_key:
            not_valid_key_message_part_1 = f"The combination of fullmovenumber {response_list[0]} "
            not_valid_key_message_part_2 = f"and player color {response_list[1]} was not a valid combination here."
            print_nonfatal_error(not_valid_key_message_part_1 + not_valid_key_message_part_2)

        if is_alpha_out_of_range:
            alpha_out_of_range_message_part_1 = f"The move choice “{response_list[2]}” is not available for this "
            alpha_out_of_range_message_part_2 = f"combination of move # ({response_list[0]}) and "
            alpha_out_of_range_message_part_3 = f"color ({response_list[1]})."
            print_nonfatal_error(alpha_out_of_range_message_part_1
                                                + alpha_out_of_range_message_part_2
                                                + alpha_out_of_range_message_part_3)
#   End of branches. Now invite user to try again.
    print_nonfatal_error("Please try again.")


def example_commmand_string_for_each_player(examples_command_triples_white,
                                            examples_command_triples_black):
    """
    Randomly chooses an example command triple for each player, if one exists, e.g.,
    "6 W c" or "15 B a".

    Return a 2-tuple: white_command_string, black_command_string

    If either doesn't exist, its value is returned as None.
    """

    def randomly_chosen_movenumber_and_choice_letter(examples_list):
        """
        Inner function:
            Takes list of (fullmovenumber, number_of_edges) and randomly chooses a command order pair:
                fullmovenumber, letter_of_alphabet
            Argument examples_list:
                A list for a particular player of ordered pairs
                    fullmovenumber of the position with specified player to move
                    number_of_edges at the position
        """
        length_of_list = len(examples_list)

        if length_of_list > 0:
            random_index = random.randint(0, length_of_list - 1)
            random_fullmovenumber = examples_list[random_index][0]

            number_of_edges_for_random_index = examples_list[random_index][1]

            # Randomly choose an edge, and convert its index to a single-character alpha
            # The number of *alternatives to the mainline* is one less than the number of edges
            random_edge_numeric = random.randint(1, number_of_edges_for_random_index - 1)
            random_edge_alpha = lowercase_alpha_from_num(random_edge_numeric)

            return (random_fullmovenumber, random_edge_alpha)
        else:
            return None
    
    def random_command_triple_string_for_given_player(examples_list_for_player, color_string_for_player):
        """
        Inner function:
            Returns string such as "6 W c" or "15 B a", where:
            examples_list_for_player is examples list for given player
            color_string_for_player is "W" or "B"
        """
        random_fullmovenumber_and_edge_label = randomly_chosen_movenumber_and_choice_letter(examples_list_for_player)
        if random_fullmovenumber_and_edge_label is not None:
            chosen_fullmovenumber, chosen_alpha = random_fullmovenumber_and_edge_label
            command_string = f"{chosen_fullmovenumber} {color_string_for_player} {chosen_alpha}"
            return command_string
        else:
            return None

    white_command_string = random_command_triple_string_for_given_player(examples_command_triples_white,
                                                                         constants.WHITE_PLAYER_COLOR_STRING)
    black_command_string = random_command_triple_string_for_given_player(examples_command_triples_black,
                                                                         constants.BLACK_PLAYER_COLOR_STRING)
    return white_command_string, black_command_string


def synthesize_combined_example_command_string(examples_command_triples_white, examples_command_triples_black):
    """
    Return composite example command string of form:
        “6 W c” or “13 B a”
    if both White and Black examples exist. Otherwise returns either only a White example or only a Black example:
        “6 W c”
    or
        “13 B a”
    """

    def format_a_sample_command(string):
        return chalk.blue_bright(string)

    # Create sample command string to include in user prompt
    white_command_string, black_command_string = example_commmand_string_for_each_player(examples_command_triples_white,
                                                                                         examples_command_triples_black)
    example_command_string = ""
    if white_command_string is not None:
        white_command_string = format_a_sample_command(white_command_string)
        example_command_string += f"“{white_command_string}”"
        if black_command_string is not None:
            example_command_string += " or "
    if black_command_string is not None:
        black_command_string = format_a_sample_command(black_command_string)
        example_command_string += f"“{black_command_string}”"
    return example_command_string







