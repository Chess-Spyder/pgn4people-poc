"""
Constructs output of the variations table.
"""


from yachalk import chalk

from . import constants
from . utilities import ( conditionally_clear_console,
                          lowercase_alpha_from_num)


def print_header_for_variations_table(target_node_id, deviation_history, pgn_source):
    conditionally_clear_console()
    print("\n", 40*constants.REPEATED_STRING_FOR_TABLE_HEADER, "\n")

    if constants.WELCOME_MESSAGE:
        print(constants.WELCOME_MESSAGE)

    # Assigns string to describe the PGN file being used in order to display that string on the variations-table header.
    # pgn_source is instance of class PGNSource, and contains metadata for the user-supplied PGN file, if one was
    # provided.
    
    if pgn_source.is_sample_pgn:
        pgn_source_string = f"{constants.PUBLIC_BASENAME_SAMPLE_PGN}, v{constants.VERSION_SAMPLE_PGN}"
    else:
        pgn_source_string = pgn_source.filename_of_pgnfile
    
    print(f"PGN analyzed: {pgn_source_string}")
    print(f"Target node: {target_node_id}")
    print(f"Deviation history required to achieve the specified target node: {deviation_history}")


def print_single_node_to_console(variations_line):
    """
    Print a single line of the variations table, where the line corresponds to a single node.
    """

    # If first node, print column headings
    if constants.FIRST_NODE_TO_BE_PRINTED:
        print("\n")
        print(7*" ", "MAIN LINE", 8*" ", "ALTERNATIVES")
        print(4*" ", "WHITE", 4*" ", "BLACK")
    constants.FIRST_NODE_TO_BE_PRINTED = False


    output_string_for_node = ""
    
    # Compile strings for mainline moves
    fullmovenumber = variations_line.fullmovenumber
    fullmovenumber_string = '{:3}. '.format(fullmovenumber)

    formatted_mainline_movetext_white = format_mainline_edge(variations_line.mainline_edge_white, is_white=True)
    formatted_mainline_movetext_black = format_mainline_edge(variations_line.mainline_edge_black, is_white=False)

    output_string_for_node += fullmovenumber_string
    output_string_for_node += formatted_mainline_movetext_white
    output_string_for_node += formatted_mainline_movetext_black

    # Compile strings for non-mainline alternatives

    is_black_move = not variations_line.is_player_white

    list_of_alternative_edges_to_display = variations_line.list_of_alternative_edges_to_display

    if list_of_alternative_edges_to_display:
        for index, edge in enumerate(list_of_alternative_edges_to_display):
            index_of_alternative = index + 1
            prefixed_movetext = prefix_black_alternative_with_ellipsis(edge.movetext, is_black_move)
            original_index = edge.reference_index
            formatted_movetext = format_movetext_based_on_original_index(prefixed_movetext, original_index)
            if constants.DO_PREFIX_MOVETEXT_WITH_ALPHA:
                alphacharacter = (format_label_of_alternative_halfmoves(lowercase_alpha_from_num(index_of_alternative)))
                labeled_movetext = f"{alphacharacter}: " + formatted_movetext
                output_string_for_node += labeled_movetext
            else:
                output_string_for_node += formatted_movetext
    print(output_string_for_node)


def format_mainline_edge(edge, is_white):
    """
    Formats movetext for an edge. If the edge exists, format (color) depends on the original
    reference index of the edge at its edge (edge.reference_index), as given by
    format_movetext_based_on_original_index().

    If the edge is empty, its movetext is replaced by some form of ellipsis, which can depend on the color
    of the player, as specified by argument is_white.

    Returns formatted movetext as string.
    """


    if edge:
        movetext_string = edge.movetext
        reference_index = edge.reference_index
    else:
        movetext_string = constants.WHITE_MOVE_ELLIPSIS if is_white else constants.BLACK_MOVE_DEFERRED
        # The “-1” says: “I’m not a real move. Don’t try to format me as if I were.’
        reference_index = -1
    formatted_movetext = format_movetext_based_on_original_index(movetext_string, reference_index)
    return formatted_movetext
        

def format_movetext_based_on_original_index(movetext_to_print,  id_of_original_edge):
    """
    Formats movetext_to_print both (a) as to a given fixed width and (b) color.
    """


    # Applies fixed-width formatting to all movetext_to_print regardless whether it’s a “real” move or instead
    # an ellipsis placeholder.
    string_of_formatting_instruction = f"{{:{constants.MOVETEXT_WIDTH_IN_CHARACTERS}}}"
    formatted_string = string_of_formatting_instruction.format(movetext_to_print)

    # Applies color formatting to all “real” moves
    if id_of_original_edge >= 0:
        if id_of_original_edge == 1:
            formatted_string = chalk.red_bright(formatted_string)
        elif id_of_original_edge == 2:
            formatted_string = chalk.green(formatted_string)
        elif id_of_original_edge == 3:
            formatted_string = chalk.yellow(formatted_string)
        elif id_of_original_edge == 4:
            formatted_string = chalk.magenta(formatted_string)
        elif id_of_original_edge == 5:
            formatted_string = chalk.cyan(formatted_string)
        elif id_of_original_edge > 5:
            formatted_string = chalk.blue_bright(formatted_string)
    else:
        # Because id_of_original_edge < 0, this is an ellipsis placeholder not a true movetext, and thus should not get
        # color formatting.
        pass
    return formatted_string


def format_label_of_alternative_halfmoves(string):
    """
    In the terminal output of the selected mainline and its alternatives, formats the labels of each alternative
    """

    # Dims the intensity of the alphabetic labels so they don’t stand out distractingly
    formatted_string = chalk.dim(string)
    return formatted_string


def prefix_black_alternative_with_ellipsis (movetext, is_black_move):
    """
    Prefixes alternative black halfmoves with ellipsis.
    """

    if is_black_move:
        prefixed_string = constants.BLACK_MOVE_PREFIX + movetext
        return prefixed_string
    else:
        return movetext
