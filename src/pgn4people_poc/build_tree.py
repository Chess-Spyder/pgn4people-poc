""" Exports the buildtree() function """

from . classes_arboreal import Edge
from . classes_arboreal import GameNode
from . import constants
from . error_processing import fatal_pgn_error
from . import pgn_utilities


def buildtree(tokenlist):
    """
    Build the game tree—as a dictionary (“gamenodes”) of game nodes—from supplied list of PGN tokens. Return gamenodes.

    The key of the (key, value) pair of the dictionary gamenodes is the numeric ID of the node.

    The game tree is made up of nodes. A node is an instance of class GameNode.
        At each node, a nonnegative number of move options is available.
            When the number of available move options at a node is zero, that node is a “terminal node.”

    A move corresponds to the graph-theoretic concept of an “edge.” An edge originates at one node and connects
        to another node (which latter node then is an “immediate successor” node to the “originating node”).
        Here, where the originating node is already specified, an edge (which is an instance of class Edge) refers to
        a pair of (a) the movetext descriptor of the move (e.g., "Nf3") and (b) the id of the destination node.

    The initial node corresponds to the initial position, where White is to move.
    It has node_id = constants.INITIAL_NODE_ID = 0.

    At each node, the alternative moves available there are indexed 0, 1, … , n-1, where n is the number of 
    available moves.

    By convention: At any node, the first move is the mainline move at, and conditional on,  that node and has
    index 0.

    The data structure of a node, as defined in the dictionary gamenodes, by design provides sufficient information
    for bi-directional (forward and backward) traversal of the tree. Thus, the user can explore the tree forward
    but also then backtrack and choose a different variation at an earlier point.

    Each node ν contains the specification of:
        Its (unique) immediate-predecessor node.
            This uniqueness could be relaxed if the focus were on an opening repertoire, rather than an actual game
            played. Then transpositions could be accounted for.
        The action (identified by that action’s index) at the immediate-predecessor node that led to the current node ν.
        The number of edges that emanate from this node ν.
        A list of those edges; i.e., of (movetext, id of destination node) pairs.
        The halfmove number that applies to all the moves emanating from this node ν.
    
    Because the initial node logically precedes the first movetext encountered, this initial node is created
    prior to processing the tokenlist.

    Every time a new movetext token is encountered:
        Its originating node is updated in the following way:
            The originating node’s .number_of_edges is incremented.
            The new edge (movetext, id of destingation node) is appended to the originating node’s .edgeslist.
        A new node is created, corresponding to the position reached after this new movetext’s move is taken.
            This new node may turn out to be a terminal node.
        The node_id of the new node is added to the GameNode-class attribute .set_of_nodes.
    
    The halfmovenumber is a property of a node; it is the halfmove number of every action that is spawned
    directly from that node.

    Depth is a property of a node.
        Construct the unique path from the 0-index initial node to the target node.
            This is called the path of the node.
            The path of the node is an ordered sequence of (node, action) pairs such that taking the given action
            at a node leads to the next node on the path.
        At each node along this path that precedes the target node, there is a unique action at that node that
            results in continuing along the path.
        At each such node, the required action is either
            (a) the mainline action at that node (the action has a zero index) or
            (b) some other action with a positive-integer index, which constitutes a deviation from the main line
                at that node.
        The depth of a node is defined to be the number of predecessor nodes along its path at which
            the required move is a deviation from the mainline action at that node.

    The main line of a game is determined by the unique terminal node that has depth zero.
    
    Although, at any point during the parsing of the PGN tokens, many lines/variations can be in flux,
    for each hierarchical depth, there is only one line/variation of that depth that is in flux.
    Reason: for a particular depth, a line at that depth is fully completed before another line of that depth
    is spawned.

    Therefore many parameters of interest can be tracked simply as a function of hierarchical depth (i.e., for 
    any depth, there exists only one value for that parameter):
        current_halfmovenumber[depth], a dictionary
        current_originatingnode_id[depth], a dictionary
            When a line of depth_1 is interrupted by a variation, this value will freeze, and will be used
            again when the depth returns to depth_1.
        current_choice_id_at_current_originatingnode[depth], a dictionary
        NOTE: I choose the above to be dictionaries, rather than lists, because I want to address them by depth,
        rather than append new items. With a list, I can't assign by addressing by depth unless the list has already
        been created and populated that far out. (Otherwise I would get "IndexError: list assignment index out of
        range".)

    Each time a movetext token is encountered
        A new GameNode, "newnode", is created
            The following attributes are initialized by the class definition when an instance is created:
                .depth
                    .depth is either (a) inherited from an immediately previous movetext/node, (b) increased by
                    an immediately preceding “(” token, or (c) decreased by an immediately preceding “)” token.
                .halfmovenumber, from current_halfmovenumber[depth]
                .number_of_edges = 0 (I.e., initializing this attribute as a counter.)
            The following attributes are assigned immediately
                .originatingnode_id, from current_originatingnode_id[depth]
            The following attribute can be assigned only after the originating node's .edgeslist
            is updated about the existence of this node:
                .choice_id_at_originatingnode
            The following attributes can be assigned only retrospectively/iteratively, awaiting further discovery
            through continued parsing of the tokens:
                .edgeslist
                .number_of_edges
            (Reason: A node is created when its *first* move is encountered, but further parsing may reveal
            additional moves that also belong, as alternatives, to the same node.)
        
        
    Everytime an edge is added to an originating node, the node_id of the originating node is added to
    the class attribute .set_of_nonterminal_nodes.
        This is a useful set. Compiling it in real time saves having to re-visit all nodes to see whether each 
        is a terminal node.

    When a “(” token is encountered:
        The immediately following movetext will begin a new variation at a depth one greater than the movetext
        immediately before the “(”. Thus we increase the depth.

        The first move of this new variation should have the same halfmove number as the immediately preceding movetext,
        because both of these are alternatives of the same node.

    When a “)” token is encountered:
        This ends the current variation and reverts to either (a) a previous line with depth one less or (b) a new
        variation of the same depth that begins immediately. (This occurs when a node has two or more alternatives in
        addition to the main line.)
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
    newnode = GameNode( depth, current_halfmovenumber[depth],
                        originating_node_id_of_initial_node, constants.INITIAL_NODE_ID)
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
            newnode = GameNode(depth, current_halfmovenumber[depth], current_originatingnode_id[depth], current_node_id)

            newnode.choice_id_at_originatingnode = index_of_edge_at_originating_node
            
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



