# Game-tree concepts used in pgn4people

## The game tree is represented by a dictionary of nodes, each of which can spawn multiple edges (moves)
The PGN represents a chess game. The tree of this chess game is represented within pgn4people as a dictionary (`nodedict`) of game “nodes.”
 - The key of the (key, value) pair of the dictionary `nodedict` is the numeric ID of the node.
 - The value of the (key, value) pair of the dictionary `nodedict` is the corresponding node itself.

Each node can spawn zero, one, or multiple edges, each of which corresponds to an available move in the node’s position by the player who has the move in that position.

## A node is an instance of the `GameNode` class
### A node corresponds to a chess position, including the specification of which player has the move in that position
A node corresponds to a position (i.e., not just an arrangement of pieces on the board but, as well, other attributes, such as which player has the move and the players’ castling rights).

We say that a node belongs to the player (i.e., White or Black) that has the move in the node’s position.

A node is an instance of class `GameNode`.

The initial position of the game corresponds to the initial node, which has `node_id = 0`. This node belongs to White. Its halfmove number is 1.

Most fundamentally significant: A node can have attached to it one or more “edges," each edge corresponding to a chess move available at that node to the node’s player. Each edge is an instance of the class `Edge`. See the section on edges below.

### Terminal nodes correspond to “lines” of the game
When the number of available move options (i.e., edges) at a node is zero, that node is a “terminal node.” A terminal node terminates the corresponding “line” or “variation.”

For a given terminal node, there is a unique sequence of moves that connects the initial node with that terminal node.

### Attributes of a node
By design, the data structure of a node, as defined in the dictionary `nodedict`, provides sufficient information for bi-directional (forward and backward) traversal of the tree. Thus, the user can explore the tree forward (i.e., from the initial node) but also then backtrack and choose a different variation at an earlier point. In order to efficiently achieve this bi-directional functionality, the attributes of a node overdetermine the tree in the sense that, even if some of these attributes weren’t present, one could still derive the entire tree by recursively traversing the tree from the initial node. The not-strictly-necessary attributes are included to reduce the amount of computation that would otherwise have to be inefficiently performed to travel backward in the tree.

A new node (instance of `GameNode`) is created during the parsing of the PGN file—every time a new movetext token is parsed—to provide a destination node for that newly found edge (i.e., the new node corresponds to the position that would occur if this new movetext were played in the position in which it was found). At the time of creation, however, not all of the values that will ultimately be attributes of that destination node are known. Thus some of a node’s attribute are assigned at the time of node creation; other attributes can be assigned only retrospectively.

#### Assigned at node creation
The following four attributes of a node are assigned when the node is created:
- `.halfmovenumber`
    - The halfmovenumber is a property of a node; it is the halfmove number of every move (edge) that is spawned directly from that node.
    - The parity of the halfmovenumber determines whether the node belongs to White (if odd) or Black (if even).
- `.depth`
    - The depth of a node is the number of deviations from the local main line that are required to reach the given node from the initial node. (See further discussion of the computation of depth below.)
- `originatingnode_id`
    - This is the `node_id` of the node that uniquely immediately precedes the current node in the sense that one of the edges of that immediately preceding node directly connects the preceding node with the current node.
       - (This uniqueness of the originating node could be relaxed if the focus were on an opening repertoire, rather than an actual game played. Then transpositions could be accounted for.)
    - The initial node (corresponding to the initial position) has no immediate predecessor. For this node (`node_id = 0`), `originatingnode_id` is set to `constants.UNDEFINED_TREEISH_VALUE = -1`.
- `.choice_id_at_originatingnode`
    - This is the index within the originating node’s `.edgeslist` that corresponds to the edge at the originating node that led to the current node.
    - Including this as an instance attribute facilitates the efficient determination of the path from the initial node to any other node. In particular, when backtracking from the node of interest to the initial node, knowledge of the originating node tells you that that node was on the path to the node of interest. But only by also knowing what edge at the originating node was chosen can you determine whether a deviation from the local main line was required and, if so, what that deviation was.

(Note that `node_id` is a value that is also passed—in addition to the four instance attributes above—to the constructor that instantiates each new member node of class `GameNode`. However, `node_id` is *not* a node attribute; rather it’s a key in `nodedict` that facilitates the manipulation and interrogation of nodes. `node_id` is passed to the constructor, not to add it as an instance attribute but rather, to add that value to the *class* attribute `.set_of_node_IDs`, which is a set that keeps track of all created nodes.)

#### Assigned incrementally as edges belonging to this node are discovered
The following two attributes are assigned (a) after creation of the current node and, further, (b) incrementally as each of the node’s edges is discovered (Reason: A node is created when its *first* move is encountered, but further parsing may reveal additional moves that also belong, as alternatives, to the same node.):
- `.edgeslist`
    - A list of edges, i.e., instances of class `Edge`.
    - Initialized to an empty list at the time of node instantiation, so that it acts as an empty vessel into which to add newly discovered edges.
- `.number_of_edges`
    - The number of edges that are spawned from the node.
    - Initialized to zero at the time of node instantiation, so that it acts as a counter as it is incremented each time a new edge is discovered.

When a new edge of the node is discovered: (a) `.number_of_edges`is incremented and (b) the new edge is appended to `.edgeslist`.

#### Attribute assigned dynamically and temporarily when the node is on the current main line
Integral to pgn4people’s innovative display is that the user directs that a particular move at a particular node be temporarily promoted to the main line and the other alternatives at that node are reordered to respect that choice.

The attribute `.display_order_of_edges` is a list of indices that reflect a temporary reordering of a node’s edges for the purposes of displaying the edges on the variations table, such that
- `len(node.display_order_of_edges) = node.number_of_edges`
- `node.display_order_of_edges[0] = choice_id_as_mainline`
- if `choice_id_as_mainline != 0`, then
    - `node.display_order_of_edges[1] = 0`
    - and the remaining slots in node.display_order_of_edges are filled with remaining edges in node.edgeslist and in that order. I.e., the sequence: for j=2,…,len-1, node.display_order_of_edges[j] is the same as for k = 1,…,len-1 (k≠choice_id_as_mainline)
    - In other words, (a) `choice_id_as_mainline` becomes the 0th element, (b) the previously mainline move `edgeslist[0]` becomes the first alternative,  and (c) the original indices of all the other elements of edgeslist are imported into `display_order_of_edges` in numerical order.

This takes place when the node is locally mainline and in response to the user requesting that an edge other than the node’s mainline choice be promoted temporarily for display purposes.

### The position of an edge within `.edgeslist` indicates whether the edge is locally mainline or, if not, what deviation it represents
At each node, the edges available there are indexed 0, 1, … , n-1, within `.edgeslist`, where n is the number of available moves. The position of an edge within `.edgeslist` is an expression of whether the move corresponding to the edge is “locally mainline” or, if not, its hierarchy within the non-mainline alternatives at that node. (The index an edge originally occupies in its node’s `.edgeslist` is also recorded in the edge itself (i.e., in the instance of class `Edge`) in the edge’s `.reference_index` attribute. See the discussion below of the `Edge` class.)

- If the edge occupies the first position in `.edgeslist`, i.e., index zero, the edge (or its corresponding chess move) is said to be locally mainline.
- Otherwise, the edge/move is an alternative to the locally mainline choice.
- By convention, the non-mainline alternatives are listed in decreasing order of some combination of popularity or objective chess goodness.

The “locally” adverb in “locally mainline” is a qualifier to acknowledge that, although there is a unique main line to any game, it nevertheless makes sense to discuss whether, at any off-the-main-line position, the chosen move is the mainline move in that position.
- If the PGN is from an actual game, the unique main line is the alternating sequence of White and Black moves that was actually played in the game.
- If the PGN represents an opening repertoire, in any position the locally mainline move is found in the zero-index position of `.edgeslist`. The unique main line of the repertoire would be the sequence of alternating White and Black moves that results when each player, beginning at the initial position, for each position reached, chooses the locally mainline move in that position.
- Nevertheless, even if we reach a position not on the unique main line, we can construct the mainline *continuation* from that node by similarly constructing the unique mainline continuation that would be the sequence of alternating White and Black moves that results when each player, beginning at the that off-the-main-line position, for each position reached, chooses the locally mainline move in that position. 

## An edge is an instance of the `Edge` class
A move corresponds to the graph-theoretic concept of an “edge.” An edge originates at one node and connects to another node (which latter node then is an “immediate successor” node to the “originating node”).

Here, where an edge belongs to a node (instance of `GameNode`), the edge’s originating node does not need to be specified as part of the edge’s specification itself (because it is implicit).

The following two attributes of each instance of the `Edge` class are assigned when the instance is instantiated:
- `.movetext`
    -  the movetext descriptor of the move (e.g., "Nf3")
- `destination_node_id`
    - This is the id of the node at which play would arrive if this edge were chosen at its node.

The following attribute can be assigned only after instantiation:
- `reference_index`
    - This is the index within the edge’s node’ `.edgeslist` that this edge originally occupies when imported from PGN.  E.g., if this edge were originally the mainline choice at its originating node, the edge's .reference_index is zero.
    - This attribute logically belongs to the originating node, rather than to the edge itself, but it’s useful to have this index replicated as an attribute of the edge because later the edge’s formatting will depend on its .reference_index, and it’s inconvenient to have to first determine its originating node in order to deterine this index.
    - This property cannot be assigned to the edge at the time the edge is instantiated, because this property is determined only when the existence of the edge is disclosed to the originating node, and this occurs after the edge is instantiated (because the edge object must be created before it can be passed to the originating node object). Thus this property can be assigned only separately and later and, thus, it does not appear in the constructor. Instead it is assigned by the `install_new_edge_on_originating_node()` method of the `GameNode` class.

Everytime an edge is added to an originating node, the `node_id` of the originating node is added to the class attribute `.set_of_nonterminal_nodes`. This is a useful set. Compiling it in real time saves having to re-visit all nodes to see whether each is a terminal node. (Instead, the set of terminal nodes is calculated by the set-theoretic difference that produces the nodes in the set of all nodes that are not in the set of non-terminal nodes.)

## The meaning and calculation of “depth”
Depth is a property of a node:
1. Construct the unique path from the 0-index initial node to the target node.
    - This is called the path of the node. The path of the node is an ordered sequence of (node, edge) pairs such that taking the given edge at a node leads to the next node on the path.
    - At each node along this path that precedes the target node, there is a unique edge at that node that
        results in continuing along the path.
    - At each such node, the required edge is either
        1. the mainline edge at that node (the action has a zero index) or
        2. some other edge with a positive-integer index, which constitutes a deviation from the main line
            at that node.
2. The depth of a node is defined to be the number of predecessor nodes along its path at which the required move is a deviation from the mainline action at that node.

For the avoidance of any doubt: The depth of a node is not sensitive to how far away from the mainline choice a deviation is. For example, it does not matter whether at a node the index=1 alternative was picked or whether instead the index=6 alternative was picked. For the calculation of depth, it matters only that at that node an edge otherthan the locally mainline edge was chosen.

## The concept of depth greatly facilitates the parsing of PGN into a game tree

The main line of a game is determined by the unique terminal node that has depth zero.

Although, at any point during the parsing of the PGN tokens, many lines/variations can be in flux, for each hierarchical depth, there is only one line/variation of that depth that is in flux. Reason: for a particular depth, a line at that depth is fully completed before another line of that depth is spawned.

Therefore many parameters of interest can be tracked simply as a function of hierarchical depth (i.e., for any depth, there exists only one value for that parameter):
- `current_halfmovenumber[depth]`, a dictionary
- `current_originatingnode_id[depth]`, a dictionary
    - When a line of depth_1 is interrupted by a variation, this value will freeze, and will be used
        again when the depth returns to depth_1.
- `current_choice_id_at_current_originatingnode[depth]`, a dictionary

NOTE: I choose the above to be dictionaries, rather than lists, because I want to address them by depth, rather than append new items. With a list, I can't assign by addressing by depth unless the list has already been created and populated that far out. (Otherwise I would get "IndexError: list assignment index out of range".)

Each time a movetext token is encountered a new GameNode, "newnode", is created. The `.depth` attribute is either (a) inherited from an immediately previous movetext/node, (b) increased by an immediately preceding “(” token, or (c) decreased by an immediately preceding “)” token.

- When a “(” token is encountered:
    - The immediately following movetext will begin a new variation at a depth one greater than the movetext immediately before the “(”. Thus we increase the depth.
    -  The first move of this new variation should have the same halfmove number as the immediately preceding movetext, because both of these are alternatives of the same node.

- When a “)” token is encountered:
    This ends the current variation and reverts to either (a) a previous line with depth one less or (b) a new
    variation of the same depth that begins immediately. (This occurs when a node has two or more alternatives in
    addition to the main line.)
