"""
Construct and output report characterizing the current game tree in terms of
number of lines, length of lines, and hierarchical depth.
"""

from yachalk import chalk

from . classes_arboreal import (GameNode,
                                GameTreeReport)
from . import constants
from . utilities import (conditionally_clear_console,
                         wait_for_any_user_input)


def characterize_gametree(nodedict):
    """
    Takes nodedict as representation of the tree as {node_id: node} key:value pairs, where node is an instance of the
    GameNode class.

    Records the results in class attributes of the GameTreeReport class;
        number_of_nodes: Number of positions
        number_of_lines: Number of terminal nodes
        max_halfmove_length_of_a_line : The halfmove length of the longest line (measured in halfmoves)
            The length of a line is the halfmove number associated with the line’s terminal node MINUS 1, because the
            halfmove associated with the terminal node corresponds to a move never made (since it’s a terminal mode).
        max_depth_of_a_line: The maximum depth associated with a terminal node. (The number of deviations from the
            mainline required to reach that terminal node.)
        halfmove_length_histogram: A collections.Counter dict of {halfmove_length: frequency} key:value pairs, where
            frequency is the number of terminal nodes with halfmove equal to the given halfmove_length.
        depth_histogram: A collections.Counter dict of {depth: frequency} key:value pairs, where frequency is the number
            of terminal nodes with depth equal to the given depth.

    There is a one-to-one relationship between (a) a “line” and (b) a terminal node.

    The set of terminal nodes (set_of_terminal_nodes) is a class attribute of the GameNode class and can be accessed
    (read) via any node: node.set_of_terminal_nodes.
        However, .set_of_terminal_nodes shouldn't be changed when referenced as node.set_of_terminal_nodes, because
        then .set_of_terminal_nodes would become an instance attribute. (That said, I apparently was getting away with
        it. But since I didn't understand why, I changed it to self.__class__.set_of_terminal_nodes,)

    However, while set_of_nodes and set_of_nonterminal_nodes are both compiled during the buildtree() process, 
    set_of_terminal_nodes is not and must be derived from set_of_nodes and set_of_nonterminal_nodes.
    """

    #Derive set_of_terminal_nodes

    # Compute number of nodes (i.e., number of positions)
    GameTreeReport.number_of_nodes = len(nodedict)

    # Calculates set of terminal nodes from previously calculated set of all nodes and set of all nonterminal nodes
    GameNode.set_of_terminal_node_IDs = GameNode.set_of_node_IDs.difference(GameNode.set_of_nonterminal_node_IDs)
    GameTreeReport.number_of_lines = len(GameNode.set_of_terminal_node_IDs)

    # Initialized counters and histograms
    GameTreeReport.max_halfmove_length_of_a_line = 0
    GameTreeReport.max_depth_of_a_line = 0
    GameTreeReport.depth_histogram = {}
    GameTreeReport.halfmove_length_histogram = {}
    
    # Loops througn terminal nodes
    for terminal_node_ID in GameNode.set_of_terminal_node_IDs:

        terminal_node = nodedict[terminal_node_ID]

        # Process depth
        depth = terminal_node.depth

        if depth > GameTreeReport.max_depth_of_a_line:
            GameTreeReport.max_depth_of_a_line = depth
        
        if depth in GameTreeReport.depth_histogram.keys():
            GameTreeReport.depth_histogram[depth] += 1
        else:
            GameTreeReport.depth_histogram[depth] = 1
    
        # Process halfmove_length
        # The length of a line is the halfmove number associated with the line’s terminal node MINUS 1, because the
        # halfmove number associated with the terminal node corresponds to a move never made (since it’s a terminal
        # mode).
        halfmove_length = terminal_node.halfmovenumber - 1

        if halfmove_length > GameTreeReport.max_halfmove_length_of_a_line:
            GameTreeReport.max_halfmove_length_of_a_line = halfmove_length
        
        if halfmove_length in GameTreeReport.halfmove_length_histogram.keys():
            GameTreeReport.halfmove_length_histogram[halfmove_length] += 1
        else:
            GameTreeReport.halfmove_length_histogram[halfmove_length] = 1


def output_GameTreeReport():
    """
    Outputs the results stored in class attributes of class GameTreeReport
    """
    # For formatting with f-strings, see Eric Leung, “Print fixed fields using f-strings in Python,”
    # dev.to, August 18, 2020. https://dev.to/erictleung/print-fixed-fields-using-f-strings-in-python-26ng

    conditionally_clear_console()

    header_summary = chalk.magenta("\nSUMMARY OF STATISTICS FOR THIS GAME TREE\n")
    print(header_summary)
    description_number_of_lines = "Number of lines: "
    description_number_of_positions = "Number of positions: "
    description_longest_line = "Longest line (halfmoves): "
    description_max_depth = "Greatest depth: "

    # Number of lines
    print_string_1 = f"{description_number_of_lines:>{constants.KEY_STAT_DESCRIPTION_WIDTH}}"
    print_string_2 = f"{GameTreeReport.number_of_lines:{constants.KEY_STAT_VALUE_WIDTH}}"
    print(print_string_1, print_string_2)

    # Number of positions
    print_string_1 = f"{description_number_of_positions:>{constants.KEY_STAT_DESCRIPTION_WIDTH}}"
    print_string_2 = f"{GameTreeReport.number_of_nodes:{constants.KEY_STAT_VALUE_WIDTH}}"
    print(print_string_1, print_string_2)

    # Longest line
    print_string_1 = f"{description_longest_line:>{constants.KEY_STAT_DESCRIPTION_WIDTH}}"
    print_string_2 = f"{GameTreeReport.max_halfmove_length_of_a_line:{constants.KEY_STAT_VALUE_WIDTH}}"
    print(print_string_1, print_string_2)

    # Greatest depth
    print_string_1 = f"{description_max_depth:>{constants.KEY_STAT_DESCRIPTION_WIDTH}}"
    print_string_2 = f"{GameTreeReport.max_depth_of_a_line:{constants.KEY_STAT_VALUE_WIDTH}}"
    print(print_string_1, print_string_2)

    print("\n(“Depth” of a line is the number of deviations from mainline")
    print("continuations required to arrive at the line’s terminal position.)")

    # Print depth histogram
    print("\nDEPTH HISTOGRAM")
    print("Depth     Frequency")
    for depth in sorted(GameTreeReport.depth_histogram):
        print_string_1 = f"{depth:{constants.KEY_WIDTH_IN_CHARACTERS}} "
        print_string_2 = f"{GameTreeReport.depth_histogram[depth]:{constants.FREQ_WIDTH_IN_CHARACTERS}}"
        print(print_string_1, print_string_2)
    
    print("\n(The length of a line is the number of halfmoves from and")
    print("including White’s first move to the last move of the line.)")

    # Print halfmove length histogram
    print("\nHALFMOVE-LENGTH HISTOGRAM")
    print("Length     Frequency")
    for halfmove_length in sorted(GameTreeReport.halfmove_length_histogram):
        print_string_1 = f"{halfmove_length:{constants.KEY_WIDTH_IN_CHARACTERS}} "
        print_string_2 = f"{GameTreeReport.halfmove_length_histogram[halfmove_length]:{constants.FREQ_WIDTH_IN_CHARACTERS}}"
        print(print_string_1, print_string_2)

    # Wait for user input (of any kind) before dismissing the summary table and moving forward
    wait_for_any_user_input()


def output_node_report(nodedict):
    """
    For testing/debug purposes: output each node and selected of its attributes.
    Typically, only for SMALL trees, because otherwise the number of nodes printed is very large.
    """

    conditionally_clear_console()

    header_summary = chalk.magenta("\nNODE REPORT\n")
    print(header_summary)

    print_end = ""
    print("NOTES:")
    print("\nThe halfmove number (“½#”) of a node is the halfmove number that")
    print("would be associated with a move made from that node. The halfmove")
    print("number of a line is the halfmove number of the corresponding terminal")
    print("node, MINUS ONE (because the halfmove number associated with a")
    print("terminal node is one greater than the halfmove number of the corresponding")
    print("line).")
    print("\nThe depth of a line is the number of deviations from mainline")
    print("continuations required to arrive at the line’s terminal position.")
    print("\nEach ‘edge’ is described by a pair: (a) the movetext of a move, e.g.,")
    print("“e4”, and (b) the ID of the destination node, i.e., the node that would be")
    print("reached if that move were played.")
    print("\nNode #   ½#   Depth  #edges   Edges")

    sorted_node_ids = sorted(GameNode.set_of_node_IDs)
    for node_id in sorted_node_ids:
        node = nodedict[node_id]
        value_list = [
                     f"{node_id:5}",
                     f"{node.halfmovenumber:5}",
                     f"{node.depth:7}",
                     f"{node.number_of_edges:7}   ",
                     ]

        for value in value_list:
            print(value, end=print_end)
        print("   ", end=print_end)
        for edge in node.edgeslist:
            print(f"({edge.movetext:5}, {edge.destination_node_id:3}) ", end=print_end)
        print("")


    # Wait for user input (of any kind) before dismissing the summary table and moving forward
    wait_for_any_user_input()
