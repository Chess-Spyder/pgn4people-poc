"""
Defines the GameNode and Edge classes
"""

from . import constants

class GameNode:
    """ An object of class GameNode has at least the following attributes:
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
                .choice_id_at_originatingnode attributes fully determines which node this is), for speedier lookup nodes
                are stored in a dictionary where the key value is an integer ID of the node, and the value is object of
                class GameNode.
    """
    def __init__(self):
        self.originatingnode_id = constants.UNDEFINED_TREEISH_VALUE
        self.choice_id_at_originatingnode = constants.UNDEFINED_TREEISH_VALUE
        self.number_of_edges = 0
        self.edgeslist = []
        self.reordered_edgeslist = []
        self.map_reordered_to_original_edgeslist = []
        self.halfmovenumber = constants.UNDEFINED_TREEISH_VALUE
        self.depth = constants.UNDEFINED_TREEISH_VALUE


class Edge:
    """
    Characterizes an “edge,” which refers to option/action at a node, with the following attributes
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
    def __init__(self):
        self.movetext = "UNDEFINED MOVETEXT"
        self.destination_node_id = constants.UNDEFINED_TREEISH_VALUE
