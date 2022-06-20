"""
Constructs output of the variations table.
"""

from ast import Constant
from yachalk import chalk

from pgn4people_poc.error_processing import fatal_developer_error

from . import constants
from . utilities import ( conditionally_clear_console,
                          lowercase_alpha_from_num)
from . pgn_utilities import (fullmovenumber_from_halfmove,
                             is_Black_move,
                             is_White_move )


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


def print_single_node(  node_id,
                        nodedict,
                        choice_id_as_mainline,
                        fullmovenummber_to_node_id_lookup_table,
                        examples_command_triples_white,
                        examples_command_triples_black,
                        carryover_white_movetext,
                        carryover_id_of_original_edge):
    """
    Print a single line of the variations table, where the line corresponds to a single node.
        Arguments:
            node_id:                The node_id of the nod (instance of class GameNode) in nodedict that is the subject
                                    of our printing.
            choice_id_as_mainline:  The edge of this node that should be treated as the main line.
                                    All other alternatives at this node, including the actual mainline edge,
                                    will be reordered accordingly.
            fullmovenummber_to_node_id_lookup_table
                                    A pre-created dictionary into which this function adds an entry for each halfmove
                                    with alternatives.
                                        key: A 2-tuple: (fullmovenumber, player_color), where player color is "W" or "B"
                                            (i.e., constants.WHITE_PLAYER_COLOR_STRING or
                                            constants.BLACK_PLAYER_COLOR_STRING)
                                        value: A 2-tuple: (node_id, number of non-mainline moves for this player at
                                        this movenumber)
                                    Usage:
                                        When user supplies (a) a fullmovenumber, (b) a player color, and (c) a letter
                                        ("a", "b", etc.) to identify the alternative move to treat as mainline, this
                                        dictionary is consulted to figure out (1) the node ID and (2) whether that
                                        letter is in the range of the alternatives.

                                        This dictionary needs to be initialized as empty before the tree is
                                        begun to be traversed.
            carryover_white_movetext:
                        =   movetext for a White move from the previous node when that move had no altnernatives
                            (In that case, printing a line of output is postponed, so that it can be combined with
                             Black's movetext.)
                        =   None, otherwise
            carryover_id_of_original_edge:
                        =   the index White's carry-over move had in the original .edgeslist
                        This is meaningful only in connection with carryover_white_movetext being not None.

        Returns one of three types of entities:
            int         constants.NODE_IS_TERMINAL_NODE
                        Returned if this node is a terminal node and, hence, nothing is to be printed.

            (str, int) (white_movetext_for_next_line, id_of_original_edge)
                        Returned if this is White's move and .number_of_edges == 1.
                        This movetext should be combined with Black's move when the next node is processed.
                        Unlike other movetext, it is not necessary to specify id_of id_of_reordered_edge because that is
                            necessarily zero, since carryover movetext is necessarily mainline.
                        Note: This movetext is unformatted.
                        Note: When this is returned, no output was printed.

            NoneType    None    if none of the above.
    """
    node = nodedict[node_id]
    number_of_edges = node.number_of_edges
    halfmovenumber = node.halfmovenumber
    fullmovenumber = fullmovenumber_from_halfmove(halfmovenumber)

    # If first node, print column header
    if constants.FIRST_NODE_TO_BE_PRINTED:
        print("\n")
        print(7*" ", "MAIN LINE", 8*" ", "ALTERNATIVES")
        print(4*" ", "WHITE", 4*" ", "BLACK")
    constants.FIRST_NODE_TO_BE_PRINTED = False

    if number_of_edges > 0:
        # This is not a terminal node, thus we DO want to print out this node.

        # Reorder the edges in .edgeslist to respect specification of choice_id_as_mainline
        # NOTE: The reordered edges reside in node.reordered_edgeslist. The mapping between the original edgeslist
        # and the reordered edgeslist is stored in node.map_reordered_to_original_edgeslist.
        reordered_edgeslist(node, choice_id_as_mainline)

        this_movetext_mainline = node.reordered_edgeslist[0].movetext
        id_of_reordered_edge = 0
        id_of_original_edge = node.map_reordered_to_original_edgeslist[id_of_reordered_edge]
        
        # Determine the configuration of White and Black mainline movetext(s) to be printed on this line.
        # This depends on (a) whose move it is, (b) if White's, whether White has non-mainline options, 
        # and (c) if Black's, whether the previous node generated White-move carry-over movetext.
        if is_White_move(halfmovenumber):
            # It's White's move
            player_color_string = constants.WHITE_PLAYER_COLOR_STRING
            if number_of_edges == 1:
                # White has only the mainline move, so this output should be deferred in order to combine it with
                # Black's from the next node.
                # For avoidance of doubt: the following return statement also breaks out of the function.
                # NOTE: This returns a 2-element tuple: (white_movetext_for_next_line, id_of_original_edge)
                return this_movetext_mainline, id_of_original_edge
            else:
                # White to move and White has options. Move forward with output of White's move
                white_movetext_to_print = this_movetext_mainline
                white_id_of_original_edge = id_of_original_edge
                black_movetext_to_print = constants.BLACK_MOVE_DEFERRED
                black_id_of_original_edge = -1

        else:
            # It's Black's move
            player_color_string = constants.BLACK_PLAYER_COLOR_STRING
            if carryover_white_movetext is None:
                # White's move info was printed with the last node
                white_movetext_to_print = constants.WHITE_MOVE_ELLIPSIS
                white_id_of_original_edge = -1
            else:
                # The function call supplied White's movetext for deferred printing now
                white_movetext_to_print = carryover_white_movetext
                white_id_of_original_edge = carryover_id_of_original_edge
                # Regardless of whether there's carry-over White movetext, print current movetext as Black's move
            black_movetext_to_print = this_movetext_mainline
            black_id_of_original_edge = id_of_original_edge

        # Determine whether there should be a newline after the mainline movetext(s) are printed
        # If there are no non-mainline moves, put a newline after the mainlines movetext(s).
        # Otherwise, suppress the newline to keep the following non-mainline moves on the same line.
        end_argument = "\n" if (number_of_edges == 1) else ""

        # Print the mainline White and Black movetext
        print_only_mainline_moves_for_node( fullmovenumber,
                                            white_movetext_to_print,
                                            white_id_of_original_edge,
                                            black_movetext_to_print,
                                            black_id_of_original_edge,
                                            end_argument)

        # Update the dictionary fullmovenummber_to_node_id_lookup_table
        key_for_lookup_dictionary = (fullmovenumber, player_color_string)
        value_for_lookup_dictionary = (node_id, number_of_edges - 1)
        fullmovenummber_to_node_id_lookup_table[key_for_lookup_dictionary] = value_for_lookup_dictionary

        # Update the lists of white/black example command-triples
        # examples_command_triples_white is a list of 2-tuples (fullmovenumber, number_of_edges)
        # examples_command_triples_black is a list of 2-tuples (fullmovenumber, number_of_edges)
        # For each list, each element (i.e., ordered pair) exists only when number_of_edges > 1
        if number_of_edges > 1:
            if player_color_string == constants.WHITE_PLAYER_COLOR_STRING:
                examples_command_triples_white.append((fullmovenumber, number_of_edges))
            else:
                examples_command_triples_black.append((fullmovenumber, number_of_edges))

        

        # Check whether there are non-mainline alternatives to process
        if number_of_edges > 1:
            # There are non-mainline alternatives to process

            # Iterate over non-mainline alternative moves
            string_of_additional_moves_movetext = ""
            for moveoption in range(1, number_of_edges):
                movetext_to_print = node.reordered_edgeslist[moveoption].movetext
                # If Black's move, prefixes movetext with constants.BLACK_MOVE_PREFIX (“…”) to help
                # remove any ambiguity of which player owns the alternatives when White's and Black's
                # mainline moves both appears on the same line.
                if is_Black_move(halfmovenumber) and (len(constants.BLACK_MOVE_PREFIX) > 0):
                    movetext_to_print = constants.BLACK_MOVE_PREFIX + movetext_to_print

                id_of_reordered_edge = moveoption
                id_of_original_edge = node.map_reordered_to_original_edgeslist[id_of_reordered_edge]
                formatted_string_to_append = format_movetext(movetext_to_print,
                                                             id_of_reordered_edge,
                                                             id_of_original_edge)
                if constants.DO_PREFIX_MOVETEXT_WITH_ALPHA:
                    index = id_of_reordered_edge
                    alphacharacter = (format_label_of_alternative_halfmoves(lowercase_alpha_from_num(index)))
                    formatted_string_to_append = f"{alphacharacter}: " + formatted_string_to_append
                string_of_additional_moves_movetext += formatted_string_to_append

            print(string_of_additional_moves_movetext)
        else:
            # There are no non-mainline moves
            pass
        return None
    else:
        # This is a terminal node
        # At a terminal node, there are ZERO available moves and thus there is nothing to print for this current node
        # and player.
        # However, if this player is Black, it’s possible there is a carryover move for White that would need to be
        # flushed before the variations table is completed.

        # Check whether there is a carry-over White movetext that needs to be flushed from the buffer.
        if carryover_white_movetext is not None:
            # There is a carry-over White movetext that needs to be printed.
            white_movetext_to_print = carryover_white_movetext
            white_id_of_original_edge = carryover_id_of_original_edge
            black_movetext_to_print = ""
            black_id_of_original_edge = -1
            end_argument = "\n"
            print_only_mainline_moves_for_node(
                fullmovenumber,
                white_movetext_to_print,
                white_id_of_original_edge,
                black_movetext_to_print,
                black_id_of_original_edge,
                end_argument)

        # For avoidance of doubt: the following return statement also breaks out of the function.
        return constants.NODE_IS_TERMINAL_NODE
        # End processing terminal node
        # END OF FUNCTION

def reordered_edgeslist(node, choice_id_as_mainline):
    """
    For (a) a node (an instance of class GameNode) and (b) choice_id_as_mainline, an integer, constructs both
        node.reordered_edgeslist
        node.map_reordered_to_original_edgeslist
    such that:
        node.reordered_edgeslist[0] = node.edgeslist[choice_id_as_mainline]
        node.reordered_edgeslist[1] = node.edgeslist[0]
        The sequence: for j=2,…,len-1, node.reordered_edgeslist[j] is the same as
            for k = 1,…,len-1 (k≠choice_id_as_mainline)
            In other words, (a) choice_id_as_mainline becomes the 0th element, (b) the previously mainline move
            edgeslist[0] becomes the first alternative,  and (c) all the other elements of edgeslist are imported into
            reordered_edgeslist in the same order they existed in edgeslist.
    
        node.map_reordered_to_original_edgeslist[i] is the element of .edgeslist that is now in the location
        reordered_edgeslist[i].

        node.map_reordered_to_original_edgeslist[i] answers the question:
        If the user clicks on the i-th index of the reordered edges, what original edge does that correspond to?
        Thus the value of node.map_reordered_to_original_edgeslist[i] is the index of edgeslist that corresponds to the
        i-th index of reordered edges.
    """
    
    # NOTE: number_of_choice is assumed to be positive, because this function would not be called if
    # node is a terminal node.
    number_of_choices = node.number_of_edges

    # Initializes .reordered_edgeslist and .map_reordered_to_original_edgeslist as empty lists
    node.reordered_edgeslist = []
    node.map_reordered_to_original_edgeslist = []

    # Assigns designated non-mainline move from .edgeslist to zero-th element of .reordered_edgeslist
    node.reordered_edgeslist.append(node.edgeslist[choice_id_as_mainline])
    node.map_reordered_to_original_edgeslist.append(choice_id_as_mainline)

    # Loop over edgeslist, in order, beginning with the 0th-index element, skipping over the
    # choice_id_as_mainline element, and transfer each element into reordered_edgeslist beginning with in the
    # index=1 position.
    for jindex in range(0, number_of_choices):
        if jindex != choice_id_as_mainline:
            node.reordered_edgeslist.append(node.edgeslist[jindex])
            node.map_reordered_to_original_edgeslist.append(jindex)
        else:
            # When jindex == choice_id_as_mainline, that element should not be copied to the reordered edges list
            # because it was already copied in the first step.
            pass
    # End of jindex loop

###############

def print_only_mainline_moves_for_node( fullmovenumber,
                                        white_movetext_to_print,
                                        white_id_of_original_edge,
                                        black_movetext_to_print,
                                        black_id_of_original_edge,
                                        end_argument):
    """
    Prints the fullmovenumber and White's and Black's mainline movetext.

    The formatting of the movetext can be conditioned on white_id_of_original_edge and black_id_of_original_edge.

    end_argument, which is either (a) "" or (b) "\n" is supplied to control whether a newline is appended to the string.
    """

    # id_of_reordered_edge is necessarily zero for mainline movetexts
    id_of_reordered_edge = 0

    # Prints move number, without newline
    print('{:3}. '.format(fullmovenumber), end="")

    # Formats White's and Black's movetext
    formatted_white_movetext_to_print = format_movetext(white_movetext_to_print,
                                                        id_of_reordered_edge,
                                                        white_id_of_original_edge)
    formatted_black_movetext_to_print = format_movetext(black_movetext_to_print,
                                                        id_of_reordered_edge,
                                                        black_id_of_original_edge)

    # Prints the concatenation of the two formatted movetext strings
    print(formatted_white_movetext_to_print + formatted_black_movetext_to_print, end=end_argument)

def format_movetext(movetext_to_print, id_of_reordered_edge, id_of_original_edge):
    """
    Formats movetext_to_print both (a) as to a given fixed width and (b) color.

    The color formatting can be made to depend on either/both of id_of_reordered_edge and/or id_of_original_edge.

    id_of_reordered_edge is included as an argument for flexibility in the future, but is not currently used.
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
        # Because id_of_original_edge < 0, this is not a true movetext, and thus
        # should not get color formatting.
        # This branch (id_of_original_edge==-1) is reached (a) for Black’s move when White has options and (b) White’s
        # move when Black has options (and White had options on the previous halfmove), i.e., when a move is an 
        # ellipsis placeholder.
        pass
    return formatted_string

def format_label_of_alternative_halfmoves(string):
    """
    In the terminal output of the selected mainline and its alternatives, formats the labels of each alternative
    """

    # Dims the intensity of the alphabetic labels so they don’t stand out distractingly
    formatted_string = chalk.dim(string)
    return formatted_string