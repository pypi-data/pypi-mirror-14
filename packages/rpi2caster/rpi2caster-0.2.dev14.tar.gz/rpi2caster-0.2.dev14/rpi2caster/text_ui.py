# -*- coding: utf-8 -*-
"""Command-line interface functions for rpi2caster"""

# IMPORTS for text user interface
import io
import os
import readline
import glob
from . import exceptions as e
from . import constants

# Whether the debug mode is on (can be changed by setting module's attribute)
DEBUG_MODE = False
# Style modifiers for displaying bold, italic, smallcaps, inferior, superior
STYLE_MODIFIERS = {'roman': ' ',
                   'bold': '*',
                   'italic': '/',
                   'smallcaps': '#',
                   'subscript': '_',
                   'superscript': '^'}
# Some standard prompts
MSG_MENU = '[Enter] to go back to main menu...'
MSG_CONTINUE = '[Enter] to continue...'


def menu(options, header='', footer='', no_debug=False):
    """menu(options=[(name1, long1, func1), (name2, long2, func2)...],
                    header=foo,
                    footer=bar,
                    no_debug=False):

    A menu which takes four arguments:
    options list - contains tuples for each option:
        (description, long_description, function)
    header - string to be displayed above,
    footer - string to be displayed below,
    no_debug - True if we don't want to tell the user
        that the program is in debugging mode.

    After choice is made, return the command.

    Set up vars for conditional statements,
    and lists for appending new items.

    choices - options to be entered by user
    """
    # Clear the screen, display header and add two empty lines
    clear()
    if header:
        print(header, end='\n\n')
    # Get the first option - this will be listed last
    try:
        (zero_function, zero_desc, zero_long_desc) = options[0]
        functions = [zero_function]
    except IndexError:
        raise e.ExitProgram
    # Display all the options
    # Tab indent, option number, option name (not processing option 0 yet!)
    for i, (function, desc, long_desc) in enumerate(options):
        if i > 0:
            functions.append(function)
            print('\t %i : %s \n\t\t %s \n' % (i, desc, long_desc))
    # Option 0 is displayed last, add some whitespace around it
    print('\n\t %i : %s \n\t\t %s \n' % (0, zero_desc, zero_long_desc))
    # Print footer, if defined
    if footer:
        print(footer, end='\n\n')
    if DEBUG_MODE and not no_debug:
        print('The program is now in debugging mode!', end='\n\n')
    # Add an empty line to separate prompt
    print('\n')
    # Ask for user input
    choice_number = -1
    # Get only available options and exclude non-numeric strings
    while choice_number not in range(len(options)):
        # Wait until user enters proper data
        your_choice = input('Your choice: ')
        try:
            choice_number = int(your_choice)
        except ValueError:
            # Entered anything non-digit - repeat
            your_choice = ''
    # At last, we have chosen a valid option...
    # Return a corresponding value - which is option
    return functions[choice_number]


def clear():
    """Clears the screen"""
    os.system('clear')


def display(*args, **kwargs):
    """Displays info for the user - print all in one line"""
    print(*args, **kwargs)


def display_header(text, symbol='-'):
    """Displays a header banner"""
    dash_line = symbol * len(text)
    print('\n\n' + dash_line + '\n' + text + '\n' + dash_line + '\n')


def display_parameters(data):
    """Displays the parameters by section (given as a dictionary):
    {header1: [(param1_val1, param1_desc1), (param1_val2, param1_desc2)...],
     header2: [(param2_val1, param2_desc1), (param2_val2, param2_desc2)...]...}
     a section will be displayed if there are parameters to display;
     a parameter will be displayed if its value evaluates to True."""
    # {header: [(par1, desc1), (par2, desc2)], header2: [(...)]}
    for key in data:
        parameters = '\n'.join(['%s: %s' % (desc, value)
                                for (value, desc) in data[key] if value])
        if parameters:
            display_header(key)
            print(parameters)


def debug_info(*args, **kwargs):
    """Prints debug messages to screen if in debug mode"""
    if DEBUG_MODE:
        print('DEBUG: ', *args, **kwargs)


def debug_enter_data(prompt):
    """For debug-specific data"""
    if DEBUG_MODE:
        return input('DEBUG: ' + prompt)


def debug_pause(msg1='', msg2=MSG_CONTINUE):
    """For debug confirmations"""
    if DEBUG_MODE:
        input('DEBUG: ' + msg1 + ' - ' + msg2)


def pause(msg1='', msg2=MSG_CONTINUE):
    """Waits until user presses return"""
    input(msg1 + '\n' + msg2)


def enter_data(prompt, datatype=str):
    """Enter a value and convert it to the specific datatype"""
    value = ''
    while not value:
        value = input(prompt)
        try:
            value = datatype(value)
        except ValueError:
            print('Incorrect value or data type!')
            value = ''
    return value


def enter_data_or_blank(prompt, datatype=str):
    """enter_data_or_blank:

    Enter a value or leave blank, try to convert to the specified datatype
    """
    while True:
        value = input(prompt)
        if not value:
            return value
        try:
            return datatype(value)
        except ValueError:
            print('Incorrect value or data type!')


def _format_display(character, style):
    """format_display:

    Uses ANSI escape sequences to alter the appearance of the character
    displayed in the matrix case layout.

    Temporarily unused - until bugfix for 24574.
    """
    style_codes = {'roman': 0,
                   'bold': 1,
                   'italic': 33,
                   'smallcaps': 34,
                   'subscript': 35,
                   'superscript': 36}
    closing_sequence = '\033[0m'
    starting_sequence = '\033[' + str(style_codes.get(style, 0)) + 'm'
    character = starting_sequence + character + closing_sequence
    print(character)
    return character


def format_display(character, style):
    """This is a placeholder to be used until Python bug 24574 is fixed"""
    return STYLE_MODIFIERS.get(style, '') + character


def tab_complete(text, state):
    """tab_complete(text, state):

    This function enables tab key auto-completion when you
    enter the filename.
    """
    return (glob.glob(text+'*')+[None])[state]


def enter_input_filename():
    """Allows to enter the input filename and checks if it is readable"""
    # Set readline parameters
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind('tab: complete')
    readline.set_completer(tab_complete)
    # Enter the input filename; check if the file is readable
    while True:
        prompt = '\nEnter the input file name (leave blank to abort): '
        filename = enter_data_or_blank(prompt)
        if not filename:
            return False
        filename = os.path.realpath(filename)
        try:
            with io.open(filename, 'r'):
                return filename
        except (IOError, FileNotFoundError):
            print('Wrong filename or file not readable!\n')


def enter_output_filename():
    """Allows user to enter output filename (without checking if readable)"""
    # Set readline parameters
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind('tab: complete')
    readline.set_completer(tab_complete)
    # Enter the output filename; no check here
    prompt = '\nEnter the input file name (leave blank to abort): '
    filename = enter_data_or_blank(prompt)
    if filename:
        return os.path.realpath(filename)
    else:
        return False


def simple_menu(message, options):
    """Simple menu:

    A simple menu where user is asked what to do.
    Wrong choice points back to the menu.

    Message: prompt - string displayed on screen;
    options: a dict {ans1:opt1, ans2:opt2...}.
    """
    ans = ''
    while True:
        ans = input(message)
        if ans in options:
            return options[ans]
        elif ans.lower() in options:
            return options[ans.lower()]
        elif ans.upper() in options:
            return options[ans.upper()]
        else:
            pass


def confirm(question):
    """Asks a simple question with yes or no answers.
    Returns True for yes and False for no."""
    return simple_menu('%s [Y / N]: ' % question, {'Y': True, 'N': False})


def display_diecase_layout(diecase):
    """display_diecase_layout:

    Shows a layout for a given diecase ID.
    Allows to specify a stopbar/wedge unit arrangement for this diecase,
    or uses the typical S5 if not specified.
    """
    # Define subroutines
    def process_matrix(mat):
        """Modifies matrix for displaying"""
        # Mat is defined as (char, (style1, style2...), column, row, units)
        (character, styles, column, row, units) = mat
        # Display different spaces as symbols
        spaces_symbols = {'_': '▣', ' ': '□', '': ' '}
        # Low space
        if character in spaces_symbols:
            character = spaces_symbols[character]
        # Otherwise we have a character - modify how it's displayed
        # based on style(s)
        else:
            for style in styles:
                character = format_display(character, style)
        # Add column and row to sets
        cols_set.add(column)
        rows_set.add(row)
        # Finish
        return (character, styles, column, row, units)
    # Initialize columns and rows sets
    cols_set = rows_set = set()
    # Build a list of all characters
    all_mats = [process_matrix(mat) for mat in diecase.layout]
    # Build rows and columns to iterate over
    col_numbers = ((16 in rows_set or 'NI' in cols_set or 'NL' in cols_set) and
                   constants.COLUMNS_17 or constants.COLUMNS_15)
    # If row 16 found - generate 16 rows; else 15
    row_numbers = [x for x in range(1, 16 in rows_set and 17 or 16)]
    # Arrange matrices for displaying
    # Generate a header with column numbers
    header = ('|Row|' + ''.join([col.center(4) for col in col_numbers]) +
              '|Units|Shift|')
    # "-----" line in the table
    separator = '—' * len(header)
    # A row with only spaces and vertical lines in it
    empty_row = ('|' + ' ' * 3 + '|' +
                 ' ' * 4 * len(col_numbers) + '|' +
                 ' ' * 5 + '|' + ' ' * 5 + '|')
    # Initialize the displayed layout
    displayed_layout = [separator, header, separator, empty_row]
    # Process each row
    for row_number in row_numbers:
        # Get unit width value of the wedge for this row
        units = diecase.wedge.unit_arrangement[row_number] or ''
        shifted_units = diecase.wedge.unit_arrangement[row_number-1] or ''
        # Start with row number...
        row = ['|' + str(row_number).center(3) + '|']
        # Add only characters and styles, center chars to 4
        row.extend([mat[0].center(4)
                    for column_number in col_numbers for mat in all_mats
                    if mat[2] == column_number and mat[3] == row_number])
        row.append('|' + str(units).center(5) + '|')
        row.append(str(shifted_units).center(5) + '|')
        displayed_layout.append(''.join(row))
        displayed_layout.append(empty_row)
    # Add the header at the bottom
    displayed_layout.extend([separator, header, separator])
    # We can display it now
    for row in displayed_layout:
        print(row)
    # Explanation of symbols
    print('\nExplanation:', '□ = low space, ▣ = high space',
          '*a = bold, /a = italic, #a = small caps',
          '_a = subscript (inferior), ^a = superscript (superior)',
          sep='\n', end='\n\n')


def edit_diecase_layout(diecase):
    """edit_diecase_layout(diecase):

    Edits a matrix case layout, row by row, matrix by matrix. Allows to enter
    a position to be edited.
    """
    # Deep-copy a diecase to create an independent object to work on
    working_diecase = diecase.copy()

    def get_matrix(column, row):
        """Gets matrix data for given coordinates."""
        mat = [m for m in working_diecase.layout
               if column == m[2] and row == m[3]][0]
        return mat

    def display_matrix_details(mat):
        """Displays details for a given mat"""
        (char, styles, column, row, units) = mat
        print('\nDetails for matrix at %s%s:' % (column, row))
        print('Character: %s' % char)
        print('Styles: %s' % ', '.join([style for style in styles]))
        print('Unit width: %s' % units)
        print()

    def change_parameters(mat):
        """Edits a single mat in the diecase. Returns matrix description."""
        (char, styles, column, row, units) = mat
        # Edit it?
        print('Enter character: " " for low space (typical), "_" for '
              'high space (less common), leave empty to exit...')
        char = (enter_data_or_blank('Character?: ', str) or
                e.menu_level_up())
        available_styles = {'r': 'roman', 'b': 'bold',
                            'i': 'italic', 's': 'smallcaps',
                            'l': 'subscript', 'u': 'superscript'}
        print('Assign all text styles this matrix will be used for. '
              'More than one style is OK - e.g. roman and small caps.\n'
              'Available styles: [r]oman, [b]old, [i]talic, [s]mall caps,\n'
              '[l]ower index (a.k.a. subscript, inferior), '
              '[u]pper index (a.k.a. superscript, superior).\n'
              'Leave blank for roman only.')
        styles = enter_data_or_blank('Styles?: ', str) or 'r'
        styles = [available_styles[char] for char in styles
                  if char in available_styles]
        print('How many units for this character? '
              'Leave blank for normal wedge step value')
        units = enter_data_or_blank('Units?: ', int) or 0
        # Matrix is defined, return the data
        return [char, styles, column, row, units]

    def save_matrix(mat):
        """Updates the diecase layout with the new matrix data"""
        (_, _, column, row, _) = mat
        # Get current matrix data
        old_mat = get_matrix(column, row)
        mat_id = working_diecase.layout.index(old_mat)
        if confirm('Save the matrix in layout?'):
            working_diecase.layout[mat_id] = mat

    def edit_matrix(mat):
        """Displays a matrix info, asks for confirmation, edits the mat"""
        prompt = ('Edit this matrix: [Y]es / [N]o / '
                  '[F]inish editing? ')
        options = {'Y': True, 'N': False, 'F': 'exit'}
        # Display, ask, edit, save - or do nothing
        display_matrix_details(mat)
        decision = simple_menu(prompt, options)
        if decision == 'exit':
            e.menu_level_up()
        elif decision:
            # Edit the mat
            try:
                mat = change_parameters(mat)
                save_matrix(mat)
            except e.MenuLevelUp:
                pass

    def single_cell_mode():
        """Allows to specify a cell by its coordinates and edit it."""
        col_prompt = 'Column [NI, NL, A...O] or [Enter] to exit]? :'
        while True:
            try:
                column = ''
                row = 0
                while column not in constants.COLUMNS_17:
                    column = enter_data_or_blank(col_prompt, str)
                    column = column.upper() or e.menu_level_up()
                while row not in range(1, 17):
                    row = enter_data('Row (1 - 16)?: ', int)
                mat = get_matrix(column, row)
                edit_matrix(mat)
            except e.MenuLevelUp:
                break

    def all_rows_mode():
        """Row-by-row editing - all cells in row 1, then 2 etc."""
        try:
            for mat in working_diecase.layout:
                edit_matrix(mat)
        except e.MenuLevelUp:
            pass

    def all_columns_mode():
        """Column-by-column editing - all cells in column NI, NL, A...O"""
        # Rearrange the layout so that it's read column by column
        try:
            (_,) = [edit_matrix(mat) for col in constants.COLUMNS_17
                    for mat in working_diecase.layout if mat[2] == col]
        except e.MenuLevelUp:
            pass

    def single_row_mode():
        """Edits matrices found in a single row"""
        while True:
            try:
                row = 0
                while row not in range(1, 17):
                    row = enter_data_or_blank('Row (1 - 16)?: ', int)
                    row = row or e.menu_level_up()
                (_,) = [edit_matrix(mat) for mat in working_diecase.layout
                        if mat[3] == row]
            except e.MenuLevelUp:
                break

    def single_column_mode():
        """Edits matrices found in a single column"""
        col_prompt = 'Column [NI, NL, A...O] or [Enter] to exit]? :'
        while True:
            try:
                column = ''
                while column not in constants.COLUMNS_17:
                    column = enter_data_or_blank(col_prompt, str)
                    column = column.upper() or e.menu_level_up()
                (_,) = [edit_matrix(mat) for mat in working_diecase.layout
                        if mat[2] == column]
            except e.MenuLevelUp:
                break
    # Map unit values to rows
    # If the layout is empty, we need to initialize it
    print('\nCurrent diecase layout:\n')
    display_diecase_layout(working_diecase)
    prompt = ('\nChoose edit mode or press [Enter] to quit:\n'
              'AR - all matrices row by row,\n'
              'AC - all matrices column by column,\n'
              'M - single matrix by coordinates,\n'
              'R - all matrices in a specified row,\n'
              'C - all matrices in a specified column.'
              '\nYour choice:')
    options = {'AR': all_rows_mode,
               'AC': all_columns_mode,
               'M': single_cell_mode,
               'R': single_row_mode,
               'C': single_column_mode,
               '': e.menu_level_up}
    while True:
        try:
            simple_menu(prompt, options)()
        except e.MenuLevelUp:
            que = 'Save the changes?'
            if working_diecase.layout != diecase.layout and confirm(que):
                diecase.layout = working_diecase.layout
            break


def exit_program(*_):
    """Exit program:

    All objects call this method whenever they want to exit program.
    This is because we may do something specific in different UIs,
    so an abstraction layer may come in handy.
    """
    print('\n\nGoodbye!\n')
    exit()
