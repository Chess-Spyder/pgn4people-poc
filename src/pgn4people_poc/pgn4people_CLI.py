"""
Module Docstring
"""


from . build_tree import buildtree
from . import constants
from . compile_and_output_report import (characterize_gametree,
                                         output_GameTreeReport,
                                         output_node_report)
from . construct_output import print_header_for_variations_table
from . get_process_user_CLI_input import get_node_id_move_choice_for_next_line_to_display
from . process_pgn_file import (get_string_read_from_file_CLI_package,
                                clean_and_parse_string_read_from_file)
from . traverse_tree import (deviation_history_of_node,
                             display_mainline_given_deviation_history)


def main():
    """ Main entry point of CLI app """


    # Get string of PGN from either (a) file specified by user in command line or (b) a built-in PGN file,
    string_read_from_file, pgn_source = get_string_read_from_file_CLI_package()

    # Grab the movetext from game #1 by stripping headers and stripping textual annotations; then tokenize that string.
    tokenlist = clean_and_parse_string_read_from_file(string_read_from_file, pgn_source)

    # Builds tree from pgn file
    nodedict = buildtree(tokenlist)

    fullmovenummber_to_node_id_lookup_table = {}

    examples_command_triples_white = []
    examples_command_triples_black = []

    # Starts by showing the main line
    target_node_id = 0

    #  Traverses the tree and displays the variations table to the console
    do_keep_exploring = True
    while do_keep_exploring: 
        # Computes the deviation history required to achieve the specified target_node_id
        deviation_history = deviation_history_of_node(nodedict, target_node_id)

        print_header_for_variations_table(target_node_id, deviation_history, pgn_source)

        # Displays to console the new mainline and first halfmove of each deviation from this new mainline
        display_mainline_given_deviation_history(nodedict,
                                                 deviation_history,
                                                 fullmovenummber_to_node_id_lookup_table,
                                                 examples_command_triples_white,
                                                 examples_command_triples_black)
        
        # Seeks user’s desire of what line to explore next and computes next target_node_id
        node_id_chosen, move_choice = \
            get_node_id_move_choice_for_next_line_to_display(fullmovenummber_to_node_id_lookup_table,
                                                             examples_command_triples_white,
                                                             examples_command_triples_black)
        if node_id_chosen != constants.STOP_SIGN:
            if node_id_chosen == constants.RESET_COMMAND:
                target_node_id = constants.INITIAL_NODE_ID
                print("Tree reset to original starting point.")
            elif node_id_chosen == constants.REPORT_COMMAND:
                characterize_gametree(nodedict)
                output_GameTreeReport()
            elif node_id_chosen == constants.NODEREPORT_COMMAND:
                output_node_report(nodedict)
            else:
                target_node_id = nodedict[node_id_chosen].reordered_edgeslist[move_choice].destination_node_id
                print(f"\n\nType: {type(nodedict[node_id_chosen].reordered_edgeslist[move_choice])}")
        else:
            do_keep_exploring = False
            print("You have told me to stop 🛑. I obey.")
    # End of while keep_exploring


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
