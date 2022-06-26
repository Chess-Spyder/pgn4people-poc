"""
Methods to traverse the game tree birectionally with output.

See generally pgn4people-poc/docs/game-tree-concepts.md
"""


from pgn4people_poc.error_processing import fatal_developer_error
from . construct_output import print_single_node_to_console
from . import constants
from . pgn_utilities import (assign_player_color_string,
                             fullmovenumber_from_halfmove,
                             is_white_move)

def display_mainline_given_deviation_history(nodedict,
                                             deviation_history,
                                             fullmovenummber_to_node_id_lookup_table = None,
                                             examples_command_triples_white = None,
                                             examples_command_triples_black = None
                                             ):
    """
    Constructs and displays the entire variations table corresponding to deviation_history.

    When present the following three arguments are modified in place:
        fullmovenummber_to_node_id_lookup_table
        examples_command_triples_white
        examples_command_triples_black
    Thus nothing is explicitly returned.
    
    Outputs the mainline path through the game, given the supplied devaition history, line by line.

    nodedict:   Dictionary of (node_id : node) key,value pairs, where node is an instance of class
                GameNode.
    deviation_history:
                Dictionary of of key,value pairs of the form:
                    key = node_id of some_deviation
                    value = choice_id of some_deviation
                where some_deviation is a deviation.
    fullmovenummber_to_node_id_lookup_table:
                A dictionary used as a lookup table to link user input to a chosen node.
    The following are optional here, because they are specific to the CLI version, not the web-app version.
        examples_command_triples_white=None,
        examples_command_triples_black=None
    """

    # Determine whether to update these elements that are required for input validation and user guidance in the CLI
    # version of the app, but won’t be required in the web-app version.
    # Thus these are optional arguments.
    if fullmovenummber_to_node_id_lookup_table is not None:
        do_update_fullmovenummber_to_node_id_lookup_table = True
        fullmovenummber_to_node_id_lookup_table.clear()
    else:
        do_update_fullmovenummber_to_node_id_lookup_table = False

    use_examples_command_triples = ((examples_command_triples_white is not None) and
                                    (examples_command_triples_black is not None))
    
    if use_examples_command_triples:
        examples_command_triples_white.clear()
        examples_command_triples_black.clear()

    # Start at initial node    
    node_id = constants.INITIAL_NODE_ID
    inbound_carryover_white_edge = None

    # Allows print_single_node() to take special action when it prints the first node, e.g.,
    # creating extra vertical white space and printing column headings.
    constants.FIRST_NODE_TO_BE_PRINTED = True

    do_continue = True

    while do_continue:
        # Determine which edge should be treated as the main line
        # Looks whether node_id is a node at which a deviation is prescribed by history
        if node_id in deviation_history.keys():
            # Node node_id has a deviation from the mainline action to deviation_history[node_id]
            choice_id_as_mainline = deviation_history[node_id]
        else:
            # Node node_id doesn't have a deviation; use the mainline action (constants.INDEX_MAINLINE)
            choice_id_as_mainline = constants.INDEX_MAINLINE
        
        node = nodedict[node_id]

        # Conditionally update entities required for CLI interface that aren’t required for the web-app version
        if do_update_fullmovenummber_to_node_id_lookup_table or use_examples_command_triples:
            fullmovenumber = fullmovenumber_from_halfmove(node.halfmovenumber)
            player_color_string = assign_player_color_string(is_white_move(node.halfmovenumber))
            number_of_edges = node.number_of_edges
        if do_update_fullmovenummber_to_node_id_lookup_table:
            update_fullmovenummber_to_node_id_lookup_table(fullmovenummber_to_node_id_lookup_table,
                                                           fullmovenumber,
                                                           player_color_string,
                                                           node_id,
                                                           number_of_edges)
        if use_examples_command_triples and (number_of_edges > 1):
            update_examples_command_triples(examples_command_triples_white,
                                            examples_command_triples_black,
                                            player_color_string,
                                            fullmovenumber,
                                            number_of_edges)

        variations_line = compile_movetext_elements_for_output_for_single_node(node,
                                                                               choice_id_as_mainline,
                                                                               inbound_carryover_white_edge)
        
        # Reset inbound_carryover_white_edge
        inbound_carryover_white_edge = None

        # Extracts useful elements from variations_line to determine whether to call print_single_node_to_console()
        outbound_carryover_white_edge = variations_line.outbound_carryover_white_edge
        is_terminal_node = variations_line.is_terminal_node
        mainline_edge_white = variations_line.mainline_edge_white

        do_continue = not is_terminal_node


        if outbound_carryover_white_edge:
            # Don’t produce a line of output now (because White had only a mainline move, but no alternatives) and
            # instead pass along White’s move to be combined in the next iteration with Black’s move.
            inbound_carryover_white_edge = variations_line.outbound_carryover_white_edge
        elif (not is_terminal_node) or mainline_edge_white:
            # Produce a line of output is either (a) the node is not a terminal node or (b) even if the node is a 
            # terminal node but there was a residual carryover_white_edge that needs to be flushed.
            print_single_node_to_console(variations_line)

        # Finds the next node in the main line
        if do_continue:
        # if True:
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



def compile_movetext_elements_for_output_for_single_node(node,
                                                         choice_id_as_mainline,
                                                         inbound_carryover_white_edge):
    """
    Compiles the movetext elements to be output for a single line of the variations table,
    where the line corresponds to a single node.

    If inbound_carryover_white_edge is not None (this should occur only when node belongs to Black),
    inbound_carryover_white_edge is used as mainline_edge_white on the same line as Black’s move.

    If node belongs to White, and there is only one edge (i.e., no non-mainline alternatives), then
    outbound_carryover_white_edge is set to White’s move and function returns without compiling any output.

    Returns:
        is_terminal_node
        has_carryover_White_edge
        carryover_white_edge
        mainline_edge_white
        mainline_edge_black
        list_of_alternative_edges_to_display
    """
    number_of_edges = node.number_of_edges

    halfmovenumber = node.halfmovenumber
    fullmovenumber = fullmovenumber_from_halfmove(halfmovenumber)
    is_player_white = is_white_move(halfmovenumber)
    player_color_string = assign_player_color_string(is_white_move)

    # Case: Terminal node case
    if number_of_edges == 0:
        # IS a terminal node. Either there is nothing to print and we stop, or we still need to flush a residual
        # carryover_white_edge left over from last iteration.
        is_terminal_node = True

        if inbound_carryover_white_edge is not None:
            if is_player_white:
                fatal_developer_error(f"inbound_carryover_white_edge is not None but player is White.")
            else:
                # Though player is Black, Black has no moves, so we revert to player is White, playing the carry-over
                # move.
                is_player_white = True
                mainline_edge_white = inbound_carryover_white_edge
                variations_line = Variations_Table_Line(is_terminal_node,
                                                        is_player_white = is_player_white,
                                                        fullmovenumber = fullmovenumber,
                                                        mainline_edge_white = mainline_edge_white,
                                                        mainline_edge_black = None,
                                                        outbound_carryover_white_edge = None,
                                                        list_of_alternative_edges_to_display = None)
        else:
            # Terminal node with no carryover move to print. Thus we print nothing and stop.
            variations_line = Variations_Table_Line(is_terminal_node)
        return variations_line

    # Case: NOT a terminal node. Thus we proceed to print a line
    is_terminal_node = False

    # Constructs lists of indices reflecting a reordered list of edges to display
    construct_display_order_of_node_edges(node, choice_id_as_mainline)

    # The following is a list of indices
    display_order_of_edges = node.display_order_of_edges

    # Gets mainline edge for the player with non-mainline alternatives
    mainline_edge = node.edgeslist[display_order_of_edges[0]]

# Case: White to move, but White has only a mainline move and no alternatives.
    if is_player_white and (number_of_edges == 1):
        # We defer any output in order to combine the next halfmove (of Black’s) on the same line.

        outbound_carryover_white_edge = mainline_edge
        variations_line = Variations_Table_Line(is_terminal_node,
                                                outbound_carryover_white_edge = outbound_carryover_white_edge)
        return variations_line
    
    # Case: (a) Either Black to move, regardless whether Black has alternatives, or (b) White to move and has
    # alternatives. Thus we output a line.

    # Assign mainline movetext for White and Black
    if is_player_white:
        # We’ve already established that White has alternatives, therefore Black’s halfmove is deferred until next line.
        mainline_edge_white = mainline_edge
        mainline_edge_black = None
    else:
        # Black’s move
        mainline_edge_black = mainline_edge

        # Decide how to populate mainline_edge_white depending on whether there was a carryover White edge
        if inbound_carryover_white_edge:
            # White’s last move was deferred, so we carry it over here, and present it along with Black’s move
            mainline_edge_white = inbound_carryover_white_edge
        else:
            # There’s no inbound carryover White edge because White’s earlier halfmove was printed on the previous 
            # line. Thus White gets an ellipsis (“…”)
            mainline_edge_white = None

    # Construct list of alternative (i.e., non-mainline) edges for the given player
    if number_of_edges > 1:
        list_of_alternative_edges_to_display = []
        # We’ve already assigned the index=0 mainline edge. Now we start the alternatives with index=1
        for index in display_order_of_edges[1::]:
            list_of_alternative_edges_to_display.append(node.edgeslist[index])
    else:
        list_of_alternative_edges_to_display = None
    
    variations_line = Variations_Table_Line(is_terminal_node,
                                            is_player_white=is_player_white,
                                            fullmovenumber=fullmovenumber,
                                            mainline_edge_white=mainline_edge_white,
                                            mainline_edge_black=mainline_edge_black,
                                            list_of_alternative_edges_to_display=list_of_alternative_edges_to_display)
    return variations_line


def construct_display_order_of_node_edges(node, choice_id_as_mainline):
    """
    For (a) a node (an instance of class GameNode) and (b) choice_id_as_mainline, an integer, constructs
        node.display_order_of_edges

        where node.display_order_of_edges is a list of INDICES (not edges)

        such that
            len(node.display_order_of_edges) = node.number_of_edges
            node.display_order_of_edges[0] = choice_id_as_mainline
            if choice_id_as_mainline != 0,
                node.display_order_of_edges[1] = 0
            and the remaining slots in node.display_order_of_edges are filled with remaining edges in node.edgeslist and
            in that order. I.e., the sequence: for j=2,…,len-1, node.display_order_of_edges[j] is the same as
            for k = 1,…,len-1 (k≠choice_id_as_mainline)
            In other words, (a) choice_id_as_mainline becomes the 0th element, (b) the previously mainline move
            edgeslist[0] becomes the first alternative,  and (c) the original indices of all the other elements of
            edgeslist are imported into display_order_of_edges in numerical order.
    
    This function does NOT return anything. It adds a property to an existing instance of class Edge.
    """

    node.display_order_of_edges = []

    # Assigns index of designated non-mainline edge to zero-th element of .display_order_of_edges
    node.display_order_of_edges.append(choice_id_as_mainline)

    for jindex in range(0, node.number_of_edges):
        if jindex != choice_id_as_mainline:
            node.display_order_of_edges.append(jindex)
        else:
            # When jindex == choice_id_as_mainline, that element should not be copied to display_order_of_edges
            # because it was already copied in the first step.
            pass
    # end for
    
    if len(node.display_order_of_edges) != node.number_of_edges:
        fatal_developer_error(
          f".display_order_of_edges had {len(node.display_order_of_edges)} elements rather than {node.number_of_edges}."
        )


class Variations_Table_Line():
    def __init__(self,
                 is_terminal_node,
                 fullmovenumber = None,
                 is_player_white = None,
                 mainline_edge_white = None,
                 mainline_edge_black = None,
                 outbound_carryover_white_edge = None,
                 list_of_alternative_edges_to_display = None):
        self.is_terminal_node = is_terminal_node
        self.fullmovenumber = fullmovenumber
        self.is_player_white = is_player_white
        self.mainline_edge_white = mainline_edge_white
        self.mainline_edge_black = mainline_edge_black
        self.outbound_carryover_white_edge = outbound_carryover_white_edge
        self.list_of_alternative_edges_to_display = list_of_alternative_edges_to_display


def update_fullmovenummber_to_node_id_lookup_table(fullmovenummber_to_node_id_lookup_table,
                                                   fullmovenumber,
                                                   player_color_string,
                                                   node_id,
                                                   number_of_edges):
    """
    Update fullmovenummber_to_node_id_lookup_table dictionary in place.
    Nothing is explicitly returned.
    """
    key_for_lookup_dictionary = (fullmovenumber, player_color_string)
    value_for_lookup_dictionary = (node_id, number_of_edges - 1)
    fullmovenummber_to_node_id_lookup_table[key_for_lookup_dictionary] = value_for_lookup_dictionary


def update_examples_command_triples(examples_command_triples_white,
                                    examples_command_triples_black,
                                    player_color_string,
                                    fullmovenumber,
                                    number_of_edges):
    """
    Updates lists of White and Black examples of valid user choices.
    Each of examples_command_triples_white and examples_command_triples_black is a dictionary of 2-tuples of
    (fullmovenumber, number_of_edges) that is modified in place. 
    Thus nothing is explicitly returned.
    """
    if player_color_string == constants.WHITE_PLAYER_COLOR_STRING:
        examples_command_triples_white.append((fullmovenumber, number_of_edges))
    elif player_color_string == constants.BLACK_PLAYER_COLOR_STRING:
        examples_command_triples_black.append((fullmovenumber, number_of_edges))
    else:
        error_string = f"Unrecognized player_color_string “{player_color_string}” to update_examples_command_triples()."
        fatal_developer_error(error_string)
