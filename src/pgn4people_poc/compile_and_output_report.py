"""
Construct and output report characterizing the current game tree in terms of number
of lines, length of lines, and hierarchical depth.
"""

from yachalk import chalk

from . classes_arboreal import (GameNode,
                                GameTreeReport)
from . import constants
from . utilities import clear_console


def characterize_gametree(nodedict):
    """
    Takes nodedict as representation of the tree as {node_id: node} key:value pairs, where node is an instance of the
    GameNode class.

    Records the results in class attributes of the GameTreeReport class;
        number_of_nodes: Number of positions
        number_of_lines: Number of terminal nodes
        max_halfmove_length_of_a_line : The halfmove length of the longest line (measured in halfmoves)
        max_depth_of_a_line: The maximum depth associated with a terminal node. (The number of deviations from the
            mainline required to reach that terminal node.)
        halfmove_length_histogram: A collections.Counter dict of {halfmove_length: frequency} key:value pairs, where frequency is 
            the number of terminal nodes with halfmove equal to the given halfmove_length.
        depth_histogram: A collections.Counter dict of {depth: frequency} key:value pairs, where frequency is the number
            of terminal nodes with depth equal to the given depth.


    There is a one-to-one relationship between (a) a “line” and (b) a terminal node.

    The set of terminal nodes (set_of_terminal_nodes) is a class attribute of the GameNode class and can  be accessed
    via any node: node.set_of_terminal_nodes.

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
        halfmove_length = terminal_node.halfmovenumber

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

    if(constants.DO_CLEAR_CONSOLE_EACH_TIME):
        clear_console()

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
    print("continuations required to arrive at that position.)")

    # Print depth histogram
    print("\nDEPTH HISTOGRAM")
    print("Depth     Frequency")
    for depth in sorted(GameTreeReport.depth_histogram):
        print_string_1 = f"{depth:{constants.KEY_WIDTH_IN_CHARACTERS}} "
        print_string_2 = f"{GameTreeReport.depth_histogram[depth]:{constants.FREQ_WIDTH_IN_CHARACTERS}}"
        print(print_string_1, print_string_2)
    
    # Print halfmove length histogram
    print("\nHALFMOVE LENGTH HISTOGRAM")
    print("Length     Frequency")
    for halfmove_length in sorted(GameTreeReport.halfmove_length_histogram):
        print_string_1 = f"{halfmove_length:{constants.KEY_WIDTH_IN_CHARACTERS}} "
        print_string_2 = f"{GameTreeReport.halfmove_length_histogram[halfmove_length]:{constants.FREQ_WIDTH_IN_CHARACTERS}}"
        print(print_string_1, print_string_2)

    # Wait for user input (of any kind) before dismissing the summary table and moving forward
    waiting = input(chalk.red_bright("\nPress <RETURN> to continue.\n"))
