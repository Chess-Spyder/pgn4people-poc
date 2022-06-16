"""
Defines the GameNode and Edge classes
"""

from . import constants

class GameNode:
    """
    An object of class GameNode has at least the following attributes:
        .originatingnode_id
            The node_id of the node from which the most-recent move was made that arrived at this node.
            NOTE:   The node corresponding to the initial position has no originating node that precedes it.
                    This initial-position node's .originatingnode_id is set by convention to 0.
                    Thus the node_id for the initial position itself must be 1 (because 0 is reserved).
        .choice_id_at_originatingnode
            The choice_id at .originatingnode that leads to this node.
        .number_of_edges
            Number of edges available at this node. 
            This value is initialized to be zero at the time the node is created.
            Only later (i.e., as subsequent tokens are processed) is this value incremented to reflect the discovery
            of later immediate-successor nodes.
                    This occurs when a branch occurs in the main line, e.g., when a movetext token is immediately
                    followed by a ”(”.
                    The movetext immediately following this ”(” will be the first non-mainline alternative.
                    However, this may be immediately followed by yet another non-mainline alternative, e.g.,
                        e4 ( d4 ) ( c4 ) e5
                    All of these subsequent variations must be traced to their end, i.e., until—after all
                    parenthesis-balanced strings are resolved and the next token is movetext, before it's possible
                    to know the final number of options available at this node.
            When the ultimate value of this attribute  is 0, then this is a terminal node.
        .edgeslist
            A list of edges (instances of class Edge), which are (movetext, destination_node_id) pairs.
            The first-listed edge (index = 0) is the main line beginning at this node.
        .reordered_edgeslist
            For later use, after the tree has been built, when the user explores paths off the main line. When the 
            user selects choice m at a node, original .edgeslist can be reordered so that
            (a) .reordered_edgeslist[0] = .edgeslist[m], (b) .reordered_edgeslist[1] = .edgeslist[0], and (c) the
            remaining elements from .edgeslist fill the spots of .reordered_edgeslist in the same order they exist
            in .edgeslist.
        .map_reordered_to_original_edgeslist
            A list such that .map_reordered_to_original_edgeslist[i] = j means that
                .reordered_edgeslist[i] = edgeslist[j]
                E.g., if user clicks on the ith index of reordered movetexts, that corresponds to the j-th
                original movetext.
        .halfmovenumber
            The halfmove number that applies to any move made from this node.
        .depth
            The hierarchy depth when this node is reached.
                If the mainline option is chosen, the hierarchy depth is unchanged.
                If any other option is chosen, the hierarchy depth increases by one (corresponding to an increase
                in net open parentheses).
                The hierarchy depth of White's actual first move in a game is zero.
                The depth of any move on the game's main line is zero.
            The depth of a node can change if the edges at its immediate predecessor are reordered.

    NOTE:   Although the above fully specifies the node (in particular because its .originatingnode_id and
            .choice_id_at_originatingnode attributes uniquely determines which node this is), for speedier lookup nodes
            are stored in a dictionary where the key value is an integer ID of the node, and the value is object of
            class GameNode.
    """
   
   # Define/initialize class attributes to support reporting statistics on the gametree
    set_of_node_IDs = set()
    set_of_nonterminal_node_IDs = set()
    # set_of_terminal_node_IDs = set()  # Will be computed later, so doesn't need to be initialized
    max_variation_depth = 0
    max_halfmove_length_of_line = 0
    
    
    def __init__(self, depth, halfmovenumber, originating_node_id, node_id):
        # Note that node_id is NOT an attribute of the node object; it is passed to the constructor for information
        self.depth = depth
        self.halfmovenumber = halfmovenumber
        self.originatingnode_id = originating_node_id

        self.number_of_edges = 0
        self.edgeslist = []
        self.reordered_edgeslist = []
        self.map_reordered_to_original_edgeslist = []

        self.choice_id_at_originatingnode = constants.UNDEFINED_TREEISH_VALUE

        self.__class__.set_of_node_IDs.add(node_id)


    def install_new_edge_on_originating_node(self, new_edge, originating_node_id):
        """
        (a) Adds a newly discovered Edge to its originating node, (b) increments number of edges at originating node,
        and (c) add this originating node to the set of nonterminal nodes (since we know it has at least one successor).

        USAGE: method is meant to be called on gamenodes[originating_node_id]

        NOTE: originating_node_id is passed as an argument solely to allow originating_node_id to be added to
        set_of_nonterminal_nodes. (originating_node_id is not needed for the addition of the new edge, because this 
        method is called on the appropriate node.)

        Alternatively, the node could be added to the set of nonterminal nodes only the first time an edge is
        installed. It's not clear that imposing that condition would save time, because evaluating it could take as
        much time as redundantly adding the node to the set of nonterminal nodes.
        """
        self.number_of_edges += 1
        self.edgeslist.append(new_edge)

        self.set_of_nonterminal_node_IDs.add(originating_node_id)


class Edge:
    """
    Characterizes an “edge,” which refers to an option/action at a node, with the following attributes
        .movetext
            A string of movetext, e.g., “e4”, which is the chess characterization of the move when at the position
            corresponding to node.
        .destination_node_id
            The id of the node at which play arrives if the .movetext move is chosen at the current node.
    
    An edge might be thought to fully determine a “move,” by its specification of .destination_node_id, because there is
    a unique move that arrives at .destination_node_id. However, knowledge of the edge alone doesn't provide an easy way
    to trace backward from .destination_node_id to the originating node of this edge.

    More properly, an edge requires as well the specification of its originating node. That is provided implicitly,
    since instances of edge (at this point, anyway) always exist as constituent objects associated with a particular
    originating node.
    """
    def __init__(self, movetext, destination_node_id):
        self.movetext = movetext
        self.destination_node_id = destination_node_id


class GameTreeReport:
    """
    Set of data characterizing a game tree in terms of number of lines, length
    of lines, and hierarchical depth.

    Object attributes:
        number_of_nodes: Total number of all nodes, both terminal and nonterminal
        number_of_lines: Number of terminal nodes
        max_halfmove_length_of_a_line : The halfmove length of the longest line (measured in halfmoves)
        max_depth_of_a_line: The maximum depth associated with a terminal node. (The number of deviations from the
            mainline on the path that is required to reach that terminal node.)
        halfmove_length_histogram: A collections.Counter dict of {halfmove_length: frequency} key:value pairs, where
            frequency is the number of terminal nodes with halfmove equal to the given halfmove_length.
        depth_histogram: A collections.Counter dict of {depth: frequency} key:value pairs, where frequency is the number
            of terminal nodes with depth equal to the given depth.
    
    Used by characterize_gametree() in compile_and_output_report.py.
    """
    # def __init__(self,
    #              number_of_nodes,
    #              number_of_lines,
    #              max_halfmove_length_of_a_line,
    #              max_depth_of_a_line,
    #              halfmove_length_histogram,
    #              depth_histogram):
    #     self.number_of_lines = constants.UNDEFINED_TREEISH_VALUE
    #     self.max_halfmove_length_of_a_line = constants.UNDEFINED_TREEISH_VALUE
    #     self.max_depth_of_a_line = constants.UNDEFINED_TREEISH_VALUE
    #     self.halfmove_length_histogram = {}
    #     self.depth_histogram = {}