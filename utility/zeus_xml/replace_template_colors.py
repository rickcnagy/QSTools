#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Replace colors on a Zeus template"""

import os
import sys
import string
import textwrap
import qs
import messages


def main():
    file_path, tree = qs.get_file_path_and_tree(messages.ask_file_path)
    qs.print_break()

    matching_colored_elements = find_colored_elements(tree)
    qs.print_break()

    new_bg_color = qs.ask_decimal_as_hex(messages.ask_replacement_color)
    qs.print_break()
    new_text_color = qs.ask_decimal_as_hex(messages.ask_replacement_color)
    qs.print_break()

    # make_color_replacements(
    #     matching_colored_elements,
    #     new_bg_color_decimal,
    #     new_text_color_decimal
    # )

    qs.save_tree(file_path, tree)


def find_colored_elements(tree):
    """Finds elements with the matching color.

    Finds all the elements with the same color as the first one in the template
    with that identifier.

    Args:
        identifier: the identifier to search on.

    Returns:
        a list of matching elements
    """
    match_element = qs.match_element_by_identifier(
        qs.ask(messages.ask_colored_identifier),
        tree)
    while match_element is None:
        match_element = qs.match_element_by_identifier(qs.didnt_find_elem)

    match_color = qs.element_data(match_element, tree)['backgroundColor']
    match_list = []
    for element in tree.iter():
        element_data = qs.element_data(element, tree)
        if element_data.get('backgroundColor') == match_color:
            match_list.append(element)

    qs.print_wrapped(messages.found_elements(match_list))
    return match_list


if __name__ == '__main__':
    main()
