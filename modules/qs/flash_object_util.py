#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""
Utility for working with FlashObject tools. This is great for manipulating Raw
Data Dumps, such as in the Templates module in Control.

Originally developed for replace_template_colors

Functions require that everything is based off of xml.etree.ElementTree
(normally abbreviated as tree) and xml.etree.Element (abbreviated as element)

Any functions/methods that use this module should be passing in and working
with ElementTrees or Elements.
"""

from xml.etree.ElementTree import ElementTree
import qs


def element_data(element, tree, str_when_possible=True):
    """Return the data that's encoded into the element in schema form

    This unpacks the element and returns a dictionary where the key is the
    schema name from foSchemas, and the val is the element representing
    that data point.

    If the data point is a text field like uniqueId, just the text value is
    included in the data dict. Otherwise, the element itself is included.

    So, to get the pageHeight val of a page element, due something like this:

    element_data(page_elem, tree)['pageHeight']

    if the element isn't a normal element like Box or Page, an empty dictionary
    is returned (since that means there's no data)

    Args:
        str_when_possible: if True, return the string value from any text-based
            elements

    Returns:
        the data dict or an empty dict
    """
    if element.tag != 'FO':
        return {}

    elem_type = element_type(element)
    if elem_type is None:
        return {}

    element_schemas = schemas(tree)[elem_type]
    elem_data = {
        element_schemas[i]: val
        for i, val in enumerate(element)
    }

    for key, data in elem_data.iteritems():
        if str_when_possible is True and data.tag in ['d', 's', 'i', 'se']:
            elem_data[key] = data.text

    return elem_data


def schemas(tree):
    """Gets the FlashObject schemas for the tree.

    Returns:
        a dictionary of lists of schemas, such as:

        {
            "Border": ["level", "color", width", ...],
            "Page": ["elementId", ...],
            ...
        }
    """
    schemas = {}
    for schema in tree.findall('foSchemas/sch'):
        schema_name = schema.attrib['n']
        schema_values = [i.text for i in schema]
        schemas[schema_name] = schema_values
    return schemas


def element_type(element):
    """Return the element type for a FlashObject tree, such as Box or Border"""
    return element.attrib.get('n')


def get_file_path_and_tree(message):
    """Get the tree from an XML raw data dump. Asks for file path from user.

    Returns:
        a tuple: (file_path, tree)
    """
    file_path = qs.ask(message)
    file_path = file_path.replace('\\', '')

    try:
        xml = qs.validate_xml(file_path)
        tree = ElementTree()
        tree.parse(xml)
        qs.print_wrapped(qs.messages.valid_file)
        return file_path, tree
    except (ValueError, IOError):
        return get_file_path_and_tree(qs.messages.invalid_file)


def save_tree(file_path, tree):
    """Save the tree at a unique path based on file_path"""
    output_path = qs.unique_path(file_path, extension='xml')
    tree.write(output_path)
    qs.print_wrapped(qs.messages.successful_save(output_path))


def find_by_scheme_type(schema_type, tree_or_elem):
    """Find any contained elements by schema type string in tree_or_elem"""
    return [
        i for i in tree_or_elem.iter('FO')
        if i.attrib.get('n') == schema_type
    ]


def find_by_elem_data(key, value, tree_or_elem, multiple=True):
    """Find any contained elements by data key value, such as matching a
    specific backgroundColor val.

    If multiple is True, return a list. Else, return the first match
    """
    matches = [
        i for i in tree_or_elem.iter('FO')
        if element_data(i, tree_or_elem).get(key) == value
    ]
    if not matches:
        return None
    elif multiple is False:
        return matches[0]
    else:
        return matches


def ask_decimal_as_hex(message):
    """Ask for a hex value and return the decimal version."""
    try:
        hex_value = qs.ask(message)
        return None if not hex_value else qs.hex_to_dec(hex_value)
        if not hex_value.strip():
            return None
        else:
            return qs.hex_to_dec()
    except ValueError:
        return ask_decimal(messages.invalid_hex)


def find_elements_with_user_input_color(tree):
    """Finds elements with the matching color.

    Finds all the elements with the same color as the first one in the template
    with that identifier.

    Args:
        identifier: the identifier to search on.

    Returns:
        a list of matching elements
    """
    match_element = qs.find_by_elem_data(
        'elementId',
        qs.ask(qs.messages.ask_colored_identifier),
        tree,
        multiple=False)
    while match_element is None:
        match_element = qs.find_by_elem_data(
            'elementId',
            qs.ask(qs.messages.didnt_find_elem),
            tree,
            multiple=False)

    match_elem_data = qs.element_data(match_element, tree)
    if 'backgroundColor' in match_elem_data:
        match_color = match_elem_data['backgroundColor']
    else:
        match_color = match_elem_data['color']

    match_list = qs.find_by_elem_data('backgroundColor', match_color, tree)
    match_list = match_list or []
    match_list += qs.find_by_elem_data('color', match_color, tree) or []
    qs.print_wrapped(qs.messages.found_elements(match_list))
    return match_list
