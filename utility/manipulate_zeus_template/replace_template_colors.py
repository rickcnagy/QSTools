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
    file_path = ask_file_path()
    xml = qs.validate_xml(file_path)

    tree = ElementTree()
    tree.parse(xml)

    colored_elem_id = qs.ask(messages.ask_colored_identifier)
    matching_colored_elements = find_colored_elements(colored_elem_id, tree)

    new_bg_color = ask_decimal(messages.ask_replacement_color)
    new_text_color = ask_decimal(messages.ask_replacement_color)

    # make_color_replacements(
    #     matching_colored_elements,
    #     new_bg_color_decimal,
    #     new_text_color_decimal
    # )

    save_tree(file_path, tree)


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


def save_tree(file_path, tree):
    output_path = qs.unique_path(file_path, extension='xml')
    tree.write(output_path)
    qs.w_print(messages.successful_save(output_path))


def ask_file_path():
    file_path = qs.ask(messages.ask_file_path)
    return file_path.replace('\\', '')


def ask_decimal(message):
    try:
        return qs.hex_to_dec(qs.ask(message))
    except ValueError:
        return ask_hex_converted_to_decimal(messages.invalid_hex)


if __name__ == '__main__':
    main()
