#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Replace colors on a Zeus template"""

import os
import sys
import string
import textwrap
from xml.etree.ElementTree import ElementTree
import qs
import messages


def main():
    file_path = get_file_path()
    xml = qs.validate_xml(file_path)

    tree = ElementTree()
    tree.parse(xml)

    colored_elem_id = qs.ask(messages.ask_colored_identifier)
    matching_colored_elements = find_colored_elements(colored_elem_id, tree)

    print matching_colored_elements

    # new_bg_color_hex = qs.ask(messages.ask_replacement_color)
    # new_bg_color_decimal = decimal(new_bg_color_hex)
    # new_text_color_hex = qs.ask(messages.ask_change_text_color)
    # new_text_color_decimal = decimal(new_text_color_hex)
    #
    # make_color_replacements(
    #     matching_colored_elements,
    #     new_bg_color_decimal,
    #     new_text_color_decimal
    # )
    #
    # save_tree(tree, file_path)


def find_colored_elements(identifier, tree):
    """Finds elements with the matching color.

    Finds all the elements with the same color as the first one in the template
    with that identifier.

    Args:
        identifier: the identifier to search on.

    Returns:
        a list of matching elements
    """
    match_element = None
    for element in tree.iter('FO'):
        if qs.element_data(element, tree).get('elementId') == identifier:
            match_element = element
            break

    if match_element is None:
        find_colored_elements(qs.ask(messages.didnt_find_elems), tree)

    match_color = qs.element_data(element, tree)['backgroundColor']
    match_list = []
    for element in tree.iter():
        element_data = qs.element_data(element, tree)
        if element_data.get('backgroundColor') == match_color:
            match_list.append(element)

    qs.w_print(messages.found_elements(match_list))
    return match_list


def get_file_path():
    file_path = qs.ask(messages.ask_file_path)
    return file_path.replace('\\', '')

if __name__ == '__main__':
    main()
