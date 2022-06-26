"""
Defines the GameNode and Edge classes

See generally pgn4people-poc/docs/game-tree-concepts.md
"""

from . import constants

class GameNode:
    """
    The class of which each node (position) is an instance.

    See pgn4people-poc/docs/game-tree-concepts.md
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