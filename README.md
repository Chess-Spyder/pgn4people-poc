# pgn4people: A better way to view PGN chess games (proof-of-concept demo)

<img width="1956" alt="Annotated_pgn4people_first_output with traditional" src="https://user-images.githubusercontent.com/8410716/170889780-b5a181ff-5f4f-4751-8f04-197a3058cbe0.png">

## TL;DR
A chess game’s PGN can be very difficult for humans to read, parse, navigate, and edit. It can be a messy maze that is easy to get lost in, particularly when there are long and/or deeply nested variations, subvariations, sub-subvarations, etc. And common chess interfaces don’t help enough. __pgn4people__ provides an alternative paradigm that embraces _just-in-time complexity_: show the user only as much of the mess as is relevant to her _right that moment_.

__pgn4people__ is especially useful for opening repertoires. Currently, players break their repertoires into many (even hundreds) of separate PGN files simply because it’s not feasible to navigate the lines of an entire repertoire from within a single PGN. But that’s due to an _interface failure_, not the inherent complexity of chess. With __pgn4people__, displaying and navigating through the entire repertoire represented by the [Encyclopædia of Chess Openings (ECO)](https://en.wikipedia.org/wiki/Encyclopaedia_of_Chess_Openings) or   Nick De Firmian’s equally encyclopedic [Modern Chess Openings (MCO)](https://www.penguinrandomhouse.com/books/38620/modern-chess-openings-15th-edition-by-nick-de-firmian/) would appear no more complicated to the user than would displaying a single annotated game with variations only one level deep.

Currently, __pgn4people-poc__ is just a demo, just a proof of concept. (That’s what the “-poc” in pgn4people-poc stands for.) And __pgn4people-poc__ is not intended to ever replace any current chess website or application software. Instead, the hope is that __pgn4people-poc__ will inspire the developers of current chess websites and applications to add—as an option— __pgn4people__’s approach to displaying PGN. (Of course, please excuse the crude command-line interface. That is _not_ an intended part of __pgn4people__, it’s just an artifact of this quickly coded demonstration project, __pgn4people-poc__.)

## Overview
In contrast to most repositories, this README will focus much more on the *why* and *what* but much less on the *how*:
* __pgn4people__ proposes a radically different interface for viewing and navigating through PGN. Any proposal for radical change should be accompanied by a clear, comprehensive, and compelling critique of the status quo to be replaced. Thus I spend a lot of time here on the *why*.
* The *what* tells you what using this new interface is like. This is an important consideration. Whether to prefer __pgn4people__ over the status quo is almost solely a question of whether you see the value in this *what*.
* The *how* of __pgn4people__’s implementation is of less relevance. I wrote __pgn4people__ from scratch in Python for this proof of concept, but its interface paradigm would be relevant to any chess app/site regardless of its frontend or backend technologies. __pgn4people__ isn’t meant to inspire primaily *new* apps or websites, it was motivated by wanting to inspire developers of *already existing* apps and websites to *add __pgn4people__ as an electable feature*.
  * Existing apps and websites differ greatly in the details of how they implement their PGN-display/navigation features; I can’t give any useful guidance on incorporating __pgn4people__ into any particular app or website. But there’s no need: After seeing the *what*, any particular developer will see almost instantly how to implement __pgn4people__ in their product. Doing so requires combining only tools and techniques already present in their code.

The next section of this README is [Context](#context), which provides the *why*. It discusses:
* [Portable Game Notation (PGN)](#portable-game-notation-pgn). Since you’re reading this in the first place, you might well know enough about PGN to skip that discussion.
* [The problem addressed: PGN was designed to be read by computers, not people](#the-problem-addressed-pgn-was-designed-to-be-read-by-computers-not-people). Unless you’re already convinced that traditional PGN interfaces kind of suck for navigating complex game trees, I recommend looking at this section. 
* [Survey of the better existing interfaces](#survey-of-the-better-existing-interfaces). In particular, the example of Lichess’s Study facility attempting to display meaningfully a test PGN file is good to keep in mind before you see in [the following section](#the-pgn4people-interface-approach) how very differently __pgn4people__ presents the same file.

The next section after Context is the *what*: [The pgn4people interface approach](#the-pgn4people-interface-approach). If you’re already familiar with status quo PGN interfaces and their frustrations, feel free to jump here directly.

After you read this section, and consider the example of using __pgn4people__ it gives, you’ll understand what the __pgn4people__ paradigm is all about. You don’t need to actually install and run the code to fully understand __pgn4people__. 

However, if you do want to play with the program, everything you need to know is at [Playing around with  __pgn4people-poc__](https://github.com/jimratliff/pgn4people-poc#playing-around-with-pgn4people-poc).

Then what? If you wish that your favorite FILL IN THE ___ chess software or website offered __pgn4people__’s paradigm for navigating PGN:
* If you’re the developer, implement it! I bet that, once you’ve seen the examples here, you’ll know exactly how to implement it in your own code. But of course feel free to [ask me questions](https://github.com/jimratliff).
* If you’re not the developer, email them and point them toward [this README file](https://github.com/jimratliff/pgn4people-poc#readme). Lobby them to implement __pgn4people__ in their application/website. Let them know how helpful you’d find it.

If you have any remaining questions, see the [FAQs](https://github.com/jimratliff/pgn4people-poc#faqs):
* [Why do some rows of the variations table have only a White move or only a Black move, but some rows have both a White move and a Black move?](#why-do-some-rows-of-the-variations-table-have-only-a-white-move-or-only-a-black-move-but-some-rows-have-both-a-white-move-and-a-black-move)
* [What does the color coding of the halfmoves in the output of __pgn4people-poc__ signify?](#what-does-the-color-coding-of-the-halfmoves-in-the-output-of-pgn4people-signify)
* [Why is it important/helpful to promote the chosen alternative to be the new (temporary) main line?](#why-is-it-importanthelpful-to-promote-the-chosen-alternative-to-be-the-new-temporary-main-line)
* [What about text comments (annotations)? Aren’t they just as much a usability disaster as deeply nested variations? But __pgn4people-poc__ doesn’t even consider them?!](#what-about-text-comments-annotations-arent-they-just-as-much-a-usability-disaster-as-deeply-nested-variations-but-pgn4people-doesnt-even-consider-them)
* [How can I substitute my own PGN file for the default PGN file?](#how-can-i-substitute-my-own-pgn-file-for-the-default-pgn-file)
* [How does __pgn4people__ compare to ChessTempo’s PGN Viewer?](#how-does-pgn4people-compare-to-chesstempos-pgn-viewer)
* [How does __pgn4people__ compare to a standard “Opening Explorer” interface?](#how-does-pgn4people-compare-to-a-standard-opening-explorer-interface)

If the FAQs don’t cover it, [contact me](https://github.com/jimratliff).

## Context
### Portable Game Notation (PGN)
The moves of a chess game are recorded and published using [Portable Game Notation](https://en.wikipedia.org/wiki/Portable_Game_Notation) (PGN). In order to specify and/or discuss moves different from those actually played in the game, the PGN standard is enhanced with [Recursive Annotated Variations](http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm#c8.2.5) (RAV), which permits the insertion of alternative strings of moves, possibly nested many levels deep, inside parenthetical strings. Essentially all chess websites (e.g., [Chess.com](https://www.chess.com/analysis) and [lichess](https://lichess.org/analysis)) and apps (e.g., [HIARCS Chess Explorer](https://www.hiarcs.com/), [Scid vs. PC/Mac](http://scidvspc.sourceforge.net/), and [ChessBase](https://shop.chessbase.com/en/products/chessbase_16_premium_package)) allow a user to import PGN for a game or to export PGN from a game.

Chess players do not always deal entirely directly with raw PGN but rather through an interface that hides or suppresses the raw PGN. In many cases, users wanting to [watch a live game](https://lichess.org/games) or [play through a previously played game](https://www.chessgames.com/perl/chessgame?gid=1024991)—even possibly explore its alternative sidelines—can do so without ever interacting directly with the PGN itself by using a graphical interface of the chessboard.

However, when a chess player wants to [analyze and _annotate_  her game](https://www.youtube.com/watch?v=MXYO7j0Vg7A), she needs to be able to understand and navigate through the PGN in order to add text-comment annotations and to enter variations. Another important use case is [developing an opening repertoire](https://www.youtube.com/watch?v=xGdqaXZWZC8), whereby a player specifies her chosen responses to potential moves of opponents in the opening.

[Traditional interfaces](https://lichess.org/study/nEGI6dm9) typically combine both (a) a graphical representation of a chessboard, where the pieces move to reflect progressing through the PGN and on which the user can move the pieces to effect changes to the PGN, and (b) a large-ish text field through which the user views, scrolls, and interacts with the PGN itself. (See graphic immediately below.)

<img width="1409" alt="Traditional_interface_example" src="https://user-images.githubusercontent.com/8410716/170889817-85bdb96c-afe9-4b4c-9276-2b596c394dcf.png">

### The problem addressed: PGN was designed to be read by computers, not people
PGN was developed, first and foremost, for *data interchange*, primarily between nonhumans, in order to address compatibility problems between computer programs. As the [PGN standard](http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm#c2.1) noted in 1994:
> Computer usage among chessplayers has become quite common in recent years and a variety of different programs, both commercial and public domain, are used to generate, access, and propagate chess game data. … Unfortunately, many programs have had serious problems with several aspects of the external representation of chess game data. Sometimes these problems become more visible when a user attempts to move significant quantities of data from one program to another; if there has been no real effort to ensure portability of data, then the chances for a successful transfer are small at best.

[Thus](http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm#c1):
> PGN is proposed as a universal portable representation for data interchange. The idea is to allow the construction of a family of chess applications that can quickly and easily process chess game data using PGN for import and export among themselves.

(OK, saying that “PGN was designed to be read by computers, not people” isn’t quite fair, because I’m cherry picking a little 😉, but it does capture a reality, particularly when the PGN of a game is deeply nested with long variations. The [PGN standard](http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm#c1) does allege that “PGN is structured for easy reading and writing *by human users* and for easy parsing and generation by computer programs.” However, as I illustrate below, readability by humans was a lower priority that is sometimes sacrificed. And that’s OK, because as the standard also states: “PGN is not intended to be a general purpose standard that is suitable for every possible use; no such standard could fill all conceivable requirements.”)

Annotated chess games, and particularly opening repertoires, can be structurally very complex (in a game-tree sense) in that the variations become deeply nested: play at some position can branch off with multiple possible moves and each of those moves may branch off into multiple replies, … , and so on, almost _ad infinitum_. PGN encodes any variation as an _interruption_ of the line from which it sprung. These interruptions can separate—by a great distance in the PGN code—two moves that in a chess sense are actually adjacent. For example, in a Black repertoire where the main line started with the Sicilian Defense, 1.e4 c5, all of the repertoire’s analysis against both 1.d4 and 1.c4 would interrupt the two first halfmoves that in a chess sense are adjacent: 1.e4 1…c5. (See graphic immediately below.)

<img width="1154" alt="Variations_are_interruptions" src="https://user-images.githubusercontent.com/8410716/170889901-f73fb044-4140-4aa0-9f31-57de3ea0c14c.png">

This separation can be yawningly cavernous. See, for example, the next graphic, which is taken from an example PGN that is supplied with __pgn4people-poc__, where the analysis of 1.d4 and 1.c4 separates these two moves by about *80 lines* in a text file. In traditional interfaces, the user would have to navigate through all of those irrelevant variations just to follow the main line.

<img width="1465" alt="Discontinuous_PGNs" src="https://user-images.githubusercontent.com/8410716/170889934-882435c3-31fc-4bb8-8c9e-ceeb4ab34cd7.png">

The usability of traditional interfaces doesn‘t scale well with increases in structural complexity. When the variations, subvariations, and subsubvariations, … are highly nested, it can be very difficult for the user to follow the game, for example:
* To get an overall sense of where a particular move lies in the game tree
* To figure out where in the PGN the resumption of a given line is, when that line is interrupted by one or more—potentially quite long—variations and their subvariations
* To figure out how to find a particular different line that branched off earlier
* To figure out how to get to a particular different variation
* To figure out what the alternative moves are at any point
* To figure out what the path of choices were that led to the current position

The deep-nesting problem is particularly severe when developing an opening repertoire—so much so that players reflexively break what should be a single “game” for a Black repertoire or a White repertoire into numerous—even hundreds of—individual PGN files, just because it would be intractable—with *current* tools—to work with an entire reportoire housed in a single PGN file. I submit, however—and this is the premise of __pgn4people__—that this is an _interface_ problem, not an inevitable result of the inherent complexity of the game of chess.

### Survey of the better existing interfaces
Some of the better interfaces, such as [HIARCS Chess Explorer Pro](https://www.hiarcs.com/mac-chess-explorer-pro.html), [Scid vs. PC/Mac](http://scidvspc.sourceforge.net/), and [Lichess.org’s ‘Study’ facility](https://lichess.org/study), admirably try to deal with the complexity of deeply nested variations by (a) displaying the main line of White’s and Black’s moves as two columns and (b) organizing the nesting of variations with successive levels of indentation. But indentation, while helpful at low levels of hierarchical depth, doesn’t scale well with increased levels of nesting. Each level of indentation squeezes the text into a narrower and narrower column on the right side of the window. Eventually, there’s no room for an additional level of nesting. (See the graphic immediately below showing an example using Lichess’s Study facility.) See also the FAQ [“How does __pgn4people__ compare to ChessTempo’s PGN Viewer?”](#how-does-pgn4people-compare-to-chesstempos-pgn-viewer).

<img width="1932" alt="Lichess_Study_example" src="https://user-images.githubusercontent.com/8410716/170889959-e06dceba-3b39-4746-9596-2879e01bf9f2.png">

# The __pgn4people__ interface approach
In favorable contrast to even the best traditional interfaces, the usability of __pgn4people__ scales essentially perfectly with increased levels of nesting. In fact, the interface for displaying the entire repertoire represented by the [Encyclopædia of Chess Openings (ECO)](https://en.wikipedia.org/wiki/Encyclopaedia_of_Chess_Openings) or Nick De Firmian’s equally encyclopedic [Modern Chess Openings (MCO)](https://www.penguinrandomhouse.com/books/38620/modern-chess-openings-15th-edition-by-nick-de-firmian/) would appear no more complicated to the user than would displaying a single annotated game with variations only one level deep.

The problem with traditional interfaces arises in part because they insist on presenting to the reader the full complexity of the entire game all at once, rather than only that part of the complexity that is relevant to the user at any particular moment, and that unneeded complexity obfuscates the immediately relevant structure of the game. In opposition to that approach, __pgn4people__ can be said to adopt a policy of _just-in-time complexity_.

When the user first opens a new game in __pgn4people__, she sees primarily the _main line_ arranged in two columns (for White’s and Black’s moves, respectively), possibly supplemented at any halfmove by a horizontal list of halfmove alternatives, each representing the beginning of a single variation branching off the main line at that point. (See graphic immediately below highlighting the alternatives White has at her sixth move to the mainline choice 5.Bg5, including the third alternative “c: Bc4”.)

<img width="1334" alt="pgn4people_after_click_1" src="https://user-images.githubusercontent.com/8410716/170890039-fc44f9d0-6838-43a4-b5ed-907b3c73ee23.png">

If she wants to explore off the main line at any given point, she simply clicks on one of the halfmoves available at that point. (In this command-line interface implementation, rather than clicking on one of the halfmove alternatives, the user selects the alternative with a command-line instruction. In the example in the above graphic, that command is “`6 W c`”, corresponding to the 6th move by White and choice of the third alternative labeled “c”. (See §[Interacting with __pgn4people__](#interacting-with-pgn4people) below.) In response (see graphic immediately below):
* The alternative halfmove on which she clicked is temporarily promoted (for purposes of the visualization) to be the mainline move, and the previously mainline halfmove is demoted to the first alternative (and the others are shuffled as necessary, otherwise maintaining their original ordering with respect to all other halfmoves other than the original mainline halfmove and the user-selected halfmove alternative). (See the FAQ [Why is it important/helpful to promote the chosen alternative to be the new (temporary) main line?](#why-is-it-importanthelpful-to-promote-the-chosen-alternative-to-be-the-new-temporary-main-line).)
  * It‘s important to emphasize that this promotion is *temporary* and easily reversible or supercedable; it does not affect the game’s PGN or the application’s internal representation of the original game. __pgn4people__ always retains the original specification of which move is the main line and the order of alternatives to that mainline move.
* The contents of the two columns of mainline moves above that point remains unchanged, because that path remains the mainline path to that point.
* The contents of the two columns _below_ that point are replaced with a new main line, that accepts the user’s click as in effect promoting an originally non-mainline move to be the new main line. For each of the new halfmoves thereby presented, __pgn4people__ again creates the horizontal display of alternative halfmoves when they exist.

See the graphic immediately below for an example where the user chooses to eschew the mainline 6.Bg5 against the Najdorf and explore instead 6.Bc4 (the [Fischer-Sozin Attack](https://www.ichess.net/blog/bobby-fischer-vs-garry-kasparov-sicilian-najdorf/)) at that point.

<img width="1872" alt="pgn4people_after_click_2" src="https://user-images.githubusercontent.com/8410716/170890052-0b40bb82-638b-422b-81b9-9178914bf506.png">

See also the FAQ [What does the color coding of the halfmoves in the output of __pgn4people__ signify?](#what-does-the-color-coding-of-the-halfmoves-in-the-output-of-pgn4people-signify), which presents another, more-extended example of how __pgn4people__ works.

## Goal of __pgn4people__
__pgn4people-poc__ is _not_ meant to replace any existing software or even to be used by any player for any serious chess work. Existing websites and applications have highly developed functionalities that __pgn4people-poc__ has no interest in trying to replicate.

Instead, __pgn4people-poc__ is offered as a demonstration project—a feasibility study—of what an alternative interface could be that would provide greater usability to chess players when studying and analyzing chess games or developing repertoires.

__pgn4people-poc__ is offered in hopes that existing developers will incorporate the underlying interface idea into their existing interfaces.

## Limitations
* __pgn4people-poc__ is a _demonstration_, or _proof of concept_. It is not a mature product able to fulfill any chess-analysis need.
  * There is essentially zero chess-specific logic in __pgn4people-poc__. The PGN is not analyzed from a chess point of view. E.g., the “movetext” “Nf3” means no more to __pgn4people-poc__ than would “xq5r”.
  * Instead, the logic of __pgn4people-poc__ is, more abstractly, an alternative method for visualizing complex trees.
* There is no graphical user interface for __pgn4people-poc__. Instead, __pgn4people-poc__ is configured as a command-line program to:
  * Display its output to the terminal
  * Receive instructions from the user typing into the command line.
    * Thus references above like “she simply clicks on one of the halfmoves available at that point” are aspirational. The ability to click on a move is not currently implemented.
* Any text annotations in the PGN file are ignored.
* Only the first game of a multi-game PGN file is considered.

# Playing around with __pgn4people-poc__
The main point of __pgn4people-poc__ is to serve as a demo of a new paradigm that might well be instantly grasped once the above description is read. (I had to code __pgn4people-poc__ in order to prepare the examples, but now that that is done, the examples themselves do the explaining.) But if you’d like to actually play around with the program, using it to navigate either the included sample PGN file or a PGN file of your own, feel free! This section is for you.


## Installation
### Install or upgrade Python as necessary
__pgn4people-poc__ will run on just about anything with [Python](https://www.python.org/) installed—Mac, Linux, Windows. It does require a very recent version of Python, viz., Python 3.9 or greater. If you want to (a) check whether you already have Python installed, (b) check what version you have, or (c) install or upgrade your Python, see the very clear and well-organized “[Install Python 3](https://realpython.com/installing-python/)” from Real Python.

### Install __pgn4people_poc__ from the Python Package Index (PyPI)

__pgn4people_poc__ is “[open source software](https://opensource.com/resources/what-open-source)” and distributed under the very permissive [MIT License](https://opensource.org/licenses/MIT). You can install it for free from the [Python Package Index](https://pypi.org/) (PyPI) using `pip`, aka the Python Package Installer.

To install __pgn4people_poc__, you’ll need to use a Terminal or Console application. What command you type in to install __pgn4people_poc__ can vary depending on your operating system, how everything is configured, etc. However, there’s a good chance that  one of the following four incantations will do the trick.
```
pip install pgnpeople-poc
pip3 install pgnpeople-poc
python -m pip install pgnpeople-poc
python3 -m pip install pgnpeople-poc
```
For more information about `pip` and installing Python packages from PyPI, see (a) “[Installing Packages](https://packaging.python.org/en/latest/tutorials/installing-packages),” from the PyPA’s Python Packaging User Guide and (b) “[Getting Started With `pip`](https://realpython.com/what-is-pip/#getting-started-with-pip),” from Real Python’s “[Using Python's pip to Manage Your Projects' Dependencies](https://realpython.com/what-is-pip/).”


## Run __pgn4people__
### Using the built-in sample PGN file
Now that you’ve installed __pgn4people__, to run it just enter the following in the Terminal or Console application:
```
pgn4people
```
This will run __pgn4people__ on a built-in sample PGN file that is very robust and designed to put __pgn4people__ through its paces. It has over 600 distinct lines (some reflecting up to 8 departures from the main line) and over 3000 positions. It’s meant to suggest what having an entire repertoire in a single PGN file would be like.

You can also get a little bit of usage information by:
```
pgn4people --help
```
(Note: If there’s any ambiguity, those are *two* consecutive hyphens.)
### Using your own PGN file
Or, if you’d like to supply your own PGN file, it helps if the file is very well behaved, because __pgn4people__ isn’t known for being very tolerant. The PGN file should be consistent with the more-exacting “[export format](http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm#c3.2)” of PGN. The best way to get it into export format is to import the PGN into another chess website/application  (if it’s not already resident in one) and then export the PGN from there.

Then use the path ("in quotes") to that file as an additional argument. For example

```
pgn4people "/Macintosh HD/Users/some user/Desktop/my_game.pgn"
```

The two easiest ways to get the path to your own file into that argument are:
- In your Terminal program, use the `cd` command (“change directory”) to move to the directory your PGN file is already in. Then you can call `pgn4people` with simply the *name* of your file (i.e., without any more path information) like this:
```
cd /path/to/directory/of/my/PGN/file
pgn4people "my pgnfile.pgn"
```
(The quotes around the file name are crucial if the file name has any embedded spaces.)
- At least on a Mac: After you type `pgn4people `, and one more space, but *before* you hit RETURN, drag the file icon of your PGN file from Finder onto the Terminal window. The path to the file will then be entered for you. See “[Drag items into a Terminal window on Mac](https://support.apple.com/guide/terminal/drag-items-into-a-terminal-window-trml106/mac),” Apple Support.

(More generally, on a Mac, see “[How to find the path of a file in macOS](https://www.macworld.com/article/352788/how-to-find-the-path-of-a-file-in-macos.html),” Macworld, August 13, 2021.)

## Interacting with __pgn4people__
If you run `pgn4people` from the command line without providing the path to your own PGN file, __pgn4people__ will use a built-in sample PGN file. If you supply a path to your own PGN file, __pgn4people__ will use that one instead.

__pgn4people__ will read whichever file and then output to the terminal/console the game’s main line and, for each halfmove with alternatives, a horizontal list of those alternatives, each of which is labeled by a lowercase letter (e.g., “a”, “b”, etc.). (See any of the graphics in the section [The pgn4people interface approach](#the-pgn4people-interface-approach).)

Then you can specify one of those alternative moves by typing on a single line a space-separated triple of
1. move number
2. player color (“`W`”, “`B`”). (Any of “`W`”, “`w`”, “`white`”, “`White`”, “`wHiTE`”, and equivalently for Black, works.)
3. the letter of the desired alternative move. For example, for the third alternative to Black's second move, type `2 B c`.

You can keep changing the main line you look at in this way. If you want to reset the main line to the original main line, i.e., as if you were starting over, type “`reset`” instead of a triple.

When you’re done perusing, simply type “`stop`”.

You have other—rather relatively more geeky—options, too:
* Enter `report` to get a statistical summary of the PGN file, including the number of lines, the number of positions, and information about how “deep” the lines are (where the depth of a line is the number of deviations from mainline continuations required to arrive that line’s terminal position).
* Enter `nodereport` to get a (potentially very long) output of __pgn4people__’s internal representation of the game tree, describing each node of the game tree, how many moves (“edges”) lead away from that node, etc.

# FAQs
* [Why do some rows of the variations table have only a White move or only a Black move, but some rows have both a White move and a Black move?](#why-do-some-rows-of-the-variations-table-have-only-a-white-move-or-only-a-black-move-but-some-rows-have-both-a-white-move-and-a-black-move)
* [What does the color coding of the halfmoves in the output of __pgn4people__ signify?](#what-does-the-color-coding-of-the-halfmoves-in-the-output-of-pgn4people-signify)
* [Why is it important/helpful to promote the chosen alternative to be the new (temporary) main line?](#why-is-it-importanthelpful-to-promote-the-chosen-alternative-to-be-the-new-temporary-main-line)
* [What about text comments (annotations)? Aren’t they just as much a usability disaster as deeply nested variations? But __pgn4people__ doesn’t even consider them?!](#what-about-text-comments-annotations-arent-they-just-as-much-a-usability-disaster-as-deeply-nested-variations-but-pgn4people-doesnt-even-consider-them)
* [How can I substitute my own PGN file for the default PGN file?](#how-can-i-substitute-my-own-pgn-file-for-the-default-pgn-file)
* [How does __pgn4people__ compare to ChessTempo's PGN Viewer?](#how-does-pgn4people-compare-to-chesstempos-pgn-viewer)
* [How does __pgn4people__ compare to a standard “Opening Explorer” interface?](#how-does-pgn4people-compare-to-a-standard-opening-explorer-interface)

## Why do some rows of the variations table have only a White move or only a Black move, but some rows have both a White move and a Black move?
At any position where White is to move, and White has alternatives to the main line, the following mainline move by Black is deferred to the next row. That way, the user can read directly horizontally rightward across from White’s mainline move to see the alternatives for White. Only when White has no alternatives (other than the mainline move) are both players’ mainline moves (for a given move number) displayed on the same row.

On any row that has a move for Black, the alternatives on that row are all moves for Black. This is reinforced by prefacing each alternative with an ellipsis (…). See graphic immediately below.

<img width="1697" alt="Printed_variations_table_When_both_players'_moves_are_on_same_row" src="https://user-images.githubusercontent.com/8410716/170890084-308ff14f-6006-4366-8a43-24e3e335e29a.png">

## What does the color coding of the halfmoves in the output of __pgn4people__ signify?
Based on the original PGN, each halfmove is assigned a color depending on how highly it is ranked as an alternative in its position. If the halfmove is the default (mainline) move from that predecessor position, it is colored black. If the halfmove is the first alternative, it is colored red. If it is the second alternative, it is colored green, etc. These original color assignments stick to the halfmove throughout the analysis and are not changed when the user selects a halfmove to be temporarily promoted.

Thus one can, for example, tell the original hierarchical position of a halfmove in one of the two mainline columns by inspecting its color.

See the graphic immediately below for an extended example:

<img width="1958" alt="Color_coding_example" src="https://user-images.githubusercontent.com/8410716/170890121-6423f101-d210-4d38-94ad-4ebbf2701642.png">

## Why is it important/helpful to promote the chosen alternative to be the new (temporary) main line?
The temporary (and reversible and/or supersedable) promotion of the chosen alternative serves two important purposes:
1. This feature is precisely what gives __pgn4people__ the important characteristic of scaling essentially perfectly with increased levels of nesting. Without this temporary promotion of the chosen alternative, each deviation from the original main line would result in an incrementally higher level of nesting of variations and therefore of visual complexity and a reduction in ease of use.
2. This feature makes it much easier for a user, when she’s reached a position after multiple deviations from the original main line, to determine what sequence of moves led her to that position. She can simply look at the moves in the two White/Black mainline moves columns, because those reflect the moves that got her where she is now. In contrast, in a traditional interface, she can traverse the tree backward but there’s no easy way to go forward again along that same path: At every node that requires a choice other than the mainline move, she would once again have to recall and then replicate the choice she made before. The __pgn4people__ approach  makes it easy for the user to replicate that sequence. Because that sequence is the main line, using the up arrow (⬆️) and down arrow (⬇️) keys allows her to traverse forward and backward along that sequence. 

## What about text comments (annotations)? Aren’t they just as much a usability disaster as deeply nested variations? But __pgn4people__ doesn’t even consider them?!
Annotations in the form of text comments *are* a usability disaster when they are displayed inline with the PGN, as done by almost all traditional interfaces. Like variations and subvariations, text annotations are interruptions between moves that in a chess sense should be adjacent. The longer the comment is, the greater the problem this is.

Moreover, inline display of annotations creates a problem for users who want to step through a game using the “VCR controls” (right arrow (▶️) and left arrow (◀️) keys). Even though this user doesn’t otherwise want to refer to the PGN itself, the user needs to constantly scan the PGN with each move to determine whether there is a comment and, if so, to read it.

However, because this is a problem even with traditional interfaces (and because demonstrating its solution is highly specific to each implementation), __pgn4people__ does not deal with it.

That said, this problem has been solved—though its solution is almost never adopted. Text annotations should also follow the principle of just-in-time complexity by being displayed *contextually*. The annotation for a move should (a) appear only when that move is being considered by the user and (b) appear only under, over, or otherwise near the chessboard itself, so that a user isn’t required to divert attention away from the board when advancing through a game.

[RedHotPawn.com](https://www.redhotpawn.com)‘s [PGN viewer](https://www.redhotpawn.com/forum/announcements/pgn-browser--comments-supported-immortal-game-demo.133294) *does* adhere to both of these principles for the display of annotations. (See the graphic immediately below.)
* Textual annotations appear in a text box underneath both the chessboard and the move log.
* When a halfmove has an associated comment, the movetext (e.g., “7.d3”) is styled differently in the move log from halfmoves that do not have a comment. (The background color of halfmoves with comments is “Serenade” (RGB = 251, 231, 209). The background color for halfmoves without a comment is white.) This allows a user to know at a glance which halfmoves have comments and which don’t.
* When the game advances to a halfmove with a comment, that comment is displayed in the comment text box beneath the board/move log. When the game advances to a halfmove without a comment, that text box is cleared.

<img width="862" alt="Example_PGN_Browser_RedHotPawn_comments_displayed_contextually" src="https://user-images.githubusercontent.com/8410716/170890181-cf5a8a08-b006-405e-a638-629a94b7600a.png">

WATCH THE VIDEO to see this in action:

https://user-images.githubusercontent.com/8410716/174521380-0f83d043-8b25-4e67-bce3-39853818beb9.mov

This method would be easily adapted to __pgn4people__.

## How can I substitute my own PGN file for the default PGN file?
See [Using your own PGN file](#using-your-own-pgn-file).

## How does __pgn4people__ compare to ChessTempo's PGN Viewer?
Of special note, among the better traditional interfaces, is [ChessTempo.com’s PGN Viewer](https://chesstempo.com/pgn-viewer/) which is the only existing interface I’m aware of that adopts one of __pgn4people__‘s elements—showing by default only the first halfmove of a variation. (See graphic immediately below.) In effect, ChessTempo brings the concept of [code folding](https://en.wikipedia.org/wiki/Code_folding) to the display of PGN.

Unlike __pgn4people__, however, ChessTempo’s PGN Viewer doesn’t promote the chosen variation to be the temporarily new main line. (See [Why is it important/helpful to promote the chosen alternative to be the new (temporary) main line?](#why-is-it-importanthelpful-to-promote-the-chosen-alternative-to-be-the-new-temporary-main-line).)

And ChessTempo’s PGN Viewer displays the list of alternatives vertically, rather than horizontally as __pgn4people__ does, greatly spreading out vertically the display of the moves, decreasing how many mainline moves can be displayed for a given vertical size of the viewport.

<img width="1846" alt="ChessTempo_PGN_viewer_example" src="https://user-images.githubusercontent.com/8410716/170890188-86112e9d-9bc9-4846-96b9-99db360eeaa4.png">

## How does __pgn4people__ compare to a standard “Opening Explorer” interface?
Many chess sites have some version of an “Opening Explorer” that allows the user to step through opening possibilities, one halfmove at a time, choosing at each halfmove from among a set of common, or not so common, alternatives. For example, see [Lichess’s Opening Explorer](https://lichess.org/analysis#explorer) and [Chess.com’s Opening Explorer](https://www.chess.com/openings).

The Opening Explorer interface has something in common with both __pgn4people__ and with [ChessTempo’s PGN Viewer](#how-does-pgn4people-compare-to-chesstempos-pgn-viewer): alternatives are displayed initially only one halfmove deep. Opening Explorers are similar to ChessTempo’s PGN Viewer as well in deploying the alternative halfmoves vertically downward rather than horizontally to the right like __pgn4people__.

The Opening Explorer interface shares another important characteric with __pgn4people__: When the user clicks on a move to choose it, that move is effectively promoted to be the new main line. (See [Why is it important/helpful to promote the chosen alternative to be the new (temporary) main line?](#why-is-it-importanthelpful-to-promote-the-chosen-alternative-to-be-the-new-temporary-main-line).)

In contrast to both __pgn4people__ and ChessTempo’s PGN Viewer, however, an Opening Explorer is extremely myopic about the main line. On any one screen, you can’t see deeper into the main line than one additional halfmove. Instead, to discover the main line, the user would need to move from screen to screen, each time manually clicking on the top-most (i.e., more popular and therefore mainline) alternative.

(While this is certainly a downside to the Opening Explorer interface, Opening Explorers do have a countervailing benefit with respect to __pgn4people__’s horizontal display of alternatives: An Opening Explorer has the horizontal space to display various statistics for each alternative, such as frequency with which it’s played, the success rate (or W-L-D percentages) for White, the average performance rating of players that choose that move, etc.)

When the focus is more on the moves themselves, rather than these associated statistics, __pgn4people__ would be a desirable alternative to an Opening Explorer interface.


## Version History
* 1.0 6/19/2022
<!--
* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release
-->
## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
