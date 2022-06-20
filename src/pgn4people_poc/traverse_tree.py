"""
Methods to traverse the game tree birectionally with output.

Any path can be expressed as a set of (node_id, choice_id) pairs
"""


from . construct_output import print_single_node
from . import constants

def display_mainline_given_deviation_history(nodedict,
                                             deviation_history,
                                             fullmovenummber_to_node_id_lookup_table,
                                             examples_command_triples_white,
                                             examples_command_triples_black
                                             ):
    """
    Outputs the main-line path through the game, given the supplied devaition history, line by line.

    nodedict:   Dictionary of (node_id : node) key,value pairs, where node is an instance of class
                GameNode.
    deviation_history:
                Dictionary of of key,value pairs of the form:
                    key = node_id of somedeviation
                    value = choice_id of somedeviation
                where some_deviation is a deviation.
    fullmovenummber_to_node_id_lookup_table:
                A dictionary used as a lookup table to link user input to a chosen node.
    """
    # Start at initial node    
    node_id = constants.INITIAL_NODE_ID
    carryover_white_movetext = None
    carryover_id_of_original_edge = None

    # Allows print_single_node() to take special action when it prints the first node, e.g.,
    # creating extra vertical white space and printing column headings.
    constants.FIRST_NODE_TO_BE_PRINTED = True

    fullmovenummber_to_node_id_lookup_table.clear()
    examples_command_triples_white.clear()
    examples_command_triples_black.clear()

    is_terminal_node = False

    while not is_terminal_node:
        # Determine which edge should be treated as the main line
        # Looks whether node_id is a node at which a deviation is prescribed by history
        if node_id in deviation_history.keys():
            # Node node_id has a deviation from the mainline action to deviation_history[node_id]
            choice_id_as_mainline = deviation_history[node_id]
        else:
            # Node node_id doesn't have a deviation; use the mainline action (constants.INDEX_MAINLINE)
            choice_id_as_mainline = constants.INDEX_MAINLINE

        result = print_single_node( node_id,
                                    nodedict,
                                    choice_id_as_mainline,
                                    fullmovenummber_to_node_id_lookup_table,
                                    examples_command_triples_white,
                                    examples_command_triples_black,
                                    carryover_white_movetext,
                                    carryover_id_of_original_edge)

        if result == constants.NODE_IS_TERMINAL_NODE:
            # This causes the while loop to terminate.
            is_terminal_node = True
        else:
            if result is None:
                # print_single_node() returns None if NOT (this is White’s move and .number_of_edges==1)
                carryover_white_movetext = None
                carryover_id_of_original_edge = -1
            else:
                # print_single_node() returns result = (white_movetext_for_next_line, id_of_original_edge)
                carryover_white_movetext, carryover_id_of_original_edge = result

            # Finds the next node in the main line
            next_node_id = nodedict[node_id].edgeslist[choice_id_as_mainline].destination_node_id
            node_id = next_node_id
    # End of while not is_terminal_node loop


def deviation_history_of_node(nodedict, target_node_id):
    """
    Returns the deviation history of node_id (with respect to the node dictionary nodedict)).
    Arguments:
        nodedict: a dictionary of (node_id, node) pairs, where node is an instance of the GameNode class.
        target_node_id : The node of nodedict whose deviation history is desired.
    
    Background:
    A deviation is a (node_id, choice_id) pair, where choice_id is assumed not equal to zero.
    According to this deviation, at node node_id, the action choice_id ≠ 0 is chosen rather than the main line
    choice_id=0.

    In other words, the default action at any node is the zero-th index, i.e., the mainline choice. A deviation exists
    only when the chosen action is different from the mainline choice.

    A deviation history is a collection of deviations.
    Specifically, a deviation history is a dictionary all of whose (key, value) items are of the form:
        key = node_id of somedeviation
        value = choice_id of somedeviation
    where some_deviation is a deviation.

    To any target node there corresponds a unique deviation history (modulo recognition that a dictionary is unordered)
    that brings the play to that node.

    """
    deviation_history = {}

    # Start at the target node and traverse the tree backward to the origin, recording the
    # (node_id, choice_id) at every immediate-predecessor node at which a non-mainline choice was made.
    # By "record," means add (node_id, choice_id) as a key/value pair to the history dictionary.

    current_node_id = target_node_id
    while current_node_id != constants.INITIAL_NODE_ID:
        # This loop stops when it reaches the original node (id=0), which has no predecessor.

        immediate_predecessor_node_id = nodedict[current_node_id].originatingnode_id
        choice_at_predecessor = nodedict[current_node_id].choice_id_at_originatingnode

        if choice_at_predecessor != constants.INDEX_MAINLINE:
            # Action other than zero implies deviation from the mainline at the predecessor.
            deviation_history[immediate_predecessor_node_id] = choice_at_predecessor
        current_node_id = immediate_predecessor_node_id

    return deviation_history

