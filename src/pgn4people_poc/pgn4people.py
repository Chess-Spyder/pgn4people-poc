"""
Module Docstring
"""

__author__ = "Jim Ratliff"
__version__ = "0.0.1"
__license__ = "MIT"

from get_process_user_input import get_node_id_move_choice_for_next_line_to_display
from process_pgn_file import read_pgnfile_into_string
from process_pgn_file import build_tree_from_pgnstring
from construct_output import print_header_for_variations_table
from traverse_tree import deviation_history_of_node
from traverse_tree import display_mainline_given_deviation_history
import constants

import os

def main():
    """ Main entry point of the app """

    # Which of the available sample PGNs is to be read
    pgnfilepath = constants.PGNFILE6

    # Branches depending on whether sample PGN file is to be read (a) from the file system or (b) as a resource
    if constants.do_read_pgn_from_file_system:
        # Get string of PGN from built-in PGN file or other source
        pgnstring = read_pgnfile_into_string(constants.PATH_TO_CHOSEN_SAMPLE_PGN_FILE)
    else:
        pass

#   Defines name of raw PGN file
    # current_working_directory = os.getcwd()
    # print(f"The current working directory is: {current_working_directory}.")
    # print(f"Path to chosen sample PGN file: {constants.PATH_TO_CHOSEN_SAMPLE_PGN_FILE}.")
    # print(f"The current working directory contains the following: \n{os.listdir(current_working_directory)}.")

   

#   Builds tree from pgn file
    nodedict = build_tree_from_pgnstring(pgnstring)

    fullmovenummber_to_node_id_lookup_table = {}

#   Starts by showing the main line
    target_node_id = 0

    keep_exploring = True
    while keep_exploring: 
#       Traverses the tree and displays the main line (with halfmove alternatives)  

#       Computes the deviation history required to achieve the specified target_node_id
        deviation_history = deviation_history_of_node(nodedict, target_node_id)

        print_header_for_variations_table(target_node_id, deviation_history)
#       Displays to terminal the new mainline and first halfmove of each deviation from this new mainline
        display_mainline_given_deviation_history(nodedict, deviation_history, fullmovenummber_to_node_id_lookup_table)
#       Seeks user’s desire of what line to explore next and computes next target_node_id
        node_id_chosen, move_choice = \
            get_node_id_move_choice_for_next_line_to_display(fullmovenummber_to_node_id_lookup_table)
        if node_id_chosen != constants.STOP_SIGN:
            if node_id_chosen == constants.RESET_COMMAND:
                target_node_id = constants.INITIAL_NODE_ID
                print("Tree reset to original starting point.")
            else:
                target_node_id = nodedict[node_id_chosen].reordered_edgeslist[move_choice].destination_node_id
        else:
            keep_exploring = False
            print("You have told me to stop. I obey.")
#   End of while keep_exploring


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
