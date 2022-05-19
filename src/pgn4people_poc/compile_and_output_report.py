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
