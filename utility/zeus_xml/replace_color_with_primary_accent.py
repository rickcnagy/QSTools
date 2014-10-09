#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Replace a given color in a template with a primary accent in the template"""

import qs


def main():
    file_path, tree = qs.get_file_path_and_tree(qs.messages.ask_file_path)
    qs.print_break()

    elems_to_change = qs.find_elements_with_user_input_color(tree)
    qs.print_break()

    primary_accent_id = ask_primary_accent(tree)
    qs.print_break()

    replace_colors_with_primary_accent(
        elems_to_change,
        primary_accent_id,
        tree)

    qs.save_tree(file_path, tree)


def ask_primary_accent(tree):
    """Get the primary accent to convert to, based on user input"""
    primary_accents = {
        str(i): qs.element_data(primary_accent, tree)
        for i, primary_accent
        in enumerate(qs.find_by_scheme_type('PrimaryAccent', tree))
    }

    qs.print_wrapped(qs.messages.ask_for_primary_accent)

    for number in sorted(primary_accents.keys()):
        print '({}) - {}'.format(number, primary_accents[number]['name'])
    print
    chosen_num = raw_input("Choice: ").strip()
    return primary_accents[chosen_num]['metaId']


def replace_colors_with_primary_accent(elems_to_change, primary_accent_id,
    tree):
    """Change all the elems in elems_to_change to not have a color but instead
    have primary_accent_id.
    """
    for elem in elems_to_change:
        elem_data = qs.element_data(elem, tree, str_when_possible=False)
        if 'color' in elem_data:
            elem_data['color'].text = '-2'
        if 'backgroundColor' in elem_data:
            elem_data['backgroundColor'].text = '-2'
        if 'primaryAccentMetaId' in elem_data:
            elem_data['primaryAccentMetaId'].text = primary_accent_id
            elem_data['primaryAccentMetaId'].tag = 's'

if __name__ == '__main__':
    main()
