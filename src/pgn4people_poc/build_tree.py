""" Exports the buildtree() function """

from . classes_arboreal import Edge
from . classes_arboreal import GameNode
from . import constants
from . error_processing import fatal_pgn_error
from . import pgn_utilities


def buildtree(tokenlist):
    """
    Build the game tree—as a dictionary (“gamenodes”) of game nodes—from supplied list of PGN tokens. Return gamenodes.

    See generally pgn4people-poc/docs/game-tree-concepts.md
    """

    ###############   Initializations  ###############
    # Initialize empty dictionaries
    # gamenodes is indexed by a node_id
    gamenodes = {}
    # current_halfmovenumber is indexed by depth
    current_halfmovenumber = {}
    # current_originatingnode_id is indexed by depth
    current_originatingnode_id = {}
    # latest_mainline_destination is indexed by depth
    latest_mainline_destination = {}
 
    # Initializations to begin the looping through tokens
    # The first movetext token is necessarily the main line and thus depth=0
    depth = 0
    # The first movetext token is White's first move, which has halfmovenumber=1, and depth=0
    current_halfmovenumber[depth] = 1

    # Create the id=constants.INITIAL_NODE_ID=0 node corresponding to the initial position (and to White's first move)
    originating_node_id_of_initial_node = constants.UNDEFINED_TREEISH_VALUE
    newnode = GameNode(depth = depth,
                       halfmovenumber = current_halfmovenumber[depth],
                       originating_node_id = originating_node_id_of_initial_node,
                       node_id = constants.INITIAL_NODE_ID)
    # Adds this new node as the first node in the gamenodes dictionary
    gamenodes[constants.INITIAL_NODE_ID] = newnode

    lastcreated_node_id = constants.INITIAL_NODE_ID

    # The next node at current depth (0) will be spawned from node with id zero.
    current_originatingnode_id[depth]=constants.INITIAL_NODE_ID
    # Node_id for the next node to be created
    current_node_id = 1

    # Initializes boolean variables that are meant to be true only if the current movetext was immediately
    # preceded by a closed/open parenthesis, respectively
    is_preceded_by_open_paren = False
    is_preceded_by_closed_paren = False

    for token in tokenlist:
        # Branches based on whether current token is (a) movetext, (b) “(”, or (c) “)”.
        if pgn_utilities.ismovetext(token):
            # Token is movetext, which defines an edge that connects (a) the node with id
            # current_originatingnode_id[depth] to a node about to be created with id current_node_id.
            # Processing now branches based on whether the immediately preceding token was (a) “(’, (b) “)”,
            # or (c) movetext.
            # This fact is communicated here from the previous iteration via the two Boolean variables
            # is_preceded_by_open_paren and is_preceded_by_closed_paren
            if is_preceded_by_open_paren:
                # A “(” begins a new variation at a depth one greater than the movetext immediately before the “(”.
                #   Thus, we increase the depth.
                #   The first move of this new variation should have the same halfmove number as the immediately
                #   preceding movetext, because both of these are alternatives of the same node.
                # The depth and halfmovenumber were already adjusted when the “(” was encountered, so no further
                #   adjustment is necessary at this point.
                #   (You may ask: So what’s the purpose of setting is_preceded_by_open_paren=True, if all we do is do
                #   nothing? That’s precisely the point. If is_preceded_by_open_paren had not been set to True, we would 
                #   have done something when we shouldn’t have.)

                # Resets flags for beginning of new variation
                is_preceded_by_open_paren = False
                is_preceded_by_closed_paren = False
            elif is_preceded_by_closed_paren:
                # A “)” ends the current variation and reverts to either (a) a previous line with depth one less or
                # (b) a new variation of the same depth that begins immediately. (This occurs when a node has two or
                # more alternatives in addition to the main line.)
                current_halfmovenumber[depth] += 1
                current_originatingnode_id[depth] = latest_mainline_destination[depth]

                # Resets flags for beginning of new variation
                is_preceded_by_open_paren = False
                is_preceded_by_closed_paren = False

            else:
                # Current movetext token was immediately preceded by another movetext token (not a parenthesis), or by
                #   initial node.
                # The depth is unchanged.
                # The halfmovenumber for this depth is incremented.
                current_halfmovenumber[depth] += 1

                # Because the current token is reached directly via the previous movetext, that movetext's node is the 
                # originating node for the currently constructed new node.
                current_originatingnode_id[depth] = lastcreated_node_id

            # Define new edge corresponding to this token
                # new_edge.movetext = token
                # new_edge.destination_node_id = current_node_id
            new_edge = Edge(token, current_node_id)

            latest_mainline_destination[depth] = current_node_id

            # Update originating node about the existence of this node
            originating_node_id = current_originatingnode_id[depth]

            # Install new edge on originating node; add originating node to set of nonterminal nodes
            gamenodes[originating_node_id].install_new_edge_on_originating_node(new_edge, originating_node_id)

            # Computes index of new_edge at originating node that led to the current new node. This will be stored in
            # the new node corresponding to the current token.
            # NOTE: For any list, len(somelist)-1 is the index of most recently appended item
            index_of_edge_at_originating_node = len(gamenodes[originating_node_id].edgeslist) - 1

            # Create new node corresponding to the destination reached if the current token's move is chosen
            # newnode = GameNode(depth = depth,
            #                    halfmovenumber = current_halfmovenumber[depth],
            #                    originating_node_id = current_originatingnode_id[depth],
            #                    node_id = current_node_id)

            # newnode.choice_id_at_originatingnode = index_of_edge_at_originating_node

            newnode = GameNode(depth = depth,
                               halfmovenumber = current_halfmovenumber[depth],
                               originating_node_id = current_originatingnode_id[depth],
                               choice_id_at_originatingnode = index_of_edge_at_originating_node,
                               node_id = current_node_id)

            
            # Add node to gamesnodes dictionary
            gamenodes[current_node_id] = newnode

            # Adjusts current_originatingnode_id[depth] and current_node_id for next node to be created
            lastcreated_node_id = current_node_id
            current_node_id += 1

        elif token == "(":
            # Check that this isn't the first token (which should not be “(”).
            if current_node_id == 1:
                fatal_pgn_error("“(” encountered on first token after headers.")

            # A “(” begins a new variation at a depth one greater than the movetext immediately before the “(”.
            #   Thus, we increase the depth.
            depth += 1

            # The first move of this new variation should have the same halfmove number as the immediately
            # preceding movetext, because both of these are alternatives of the same node.
            # Thus we retain the halfmove number from the previous mainline move.
            current_halfmovenumber[depth] = current_halfmovenumber[depth - 1]

            # Retain same originating node as the previous mainline move
            current_originatingnode_id[depth] = current_originatingnode_id[depth - 1]

            # Sets flag to indicate that next token is immediately preceded by a closed parenthesis
            is_preceded_by_open_paren = True
    
        elif token == ")":
            # Check that this isn't the first token (which should not be “)”).
            if current_node_id == 1:
                fatal_pgn_error("“)” encountered on first token after headers.")

            # A “)” ends the current variation and reverts to either (a) a previous line with depth one less or
            # (b) a new variation of the same depth that begins immediately. (This occurs when a node has two or
            # more alternatives in addition to the main line.)

            # We decrement the depth in case we’re continuing a previous line. (However, if it turns out that the “)”
            # is immediately followed by a “(”, the next time through the loop the “elif token == "("” branch will
            # un-do this decrementing by incrementing the depth.)
            depth -= 1


            # Sets flag to indicate that next token is immediately preceded by an open parenthesis
            is_preceded_by_closed_paren = True

        else:
            # It’s not that obvious what would trigger this branch, because currently any token not a “(” or “)” *IS*
            # by definition movetext.
            fatal_pgn_error(f"First token, “{token}”,  is not movetext.")

    return gamenodes



