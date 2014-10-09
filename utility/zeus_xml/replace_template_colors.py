#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Replace colors on a Zeus template"""

import qs


def main():
    file_path, tree = qs.get_file_path_and_tree(qs.messages.ask_file_path)
    qs.print_break()

    matching_colored_elements = qs.find_elements_with_user_input_color(tree)
    qs.print_break()

    new_bg_color = qs.ask_decimal_as_hex(qs.messages.ask_replacement_color)
    qs.print_break()
    new_text_color = qs.ask_decimal_as_hex(qs.messages.ask_replacement_color)
    qs.print_break()

    make_color_replacements(
        matching_colored_elements,
        new_bg_color,
        new_text_color,
        tree
    )

    qs.save_tree(file_path, tree)


def make_color_replacements(matching_elements, new_bg_color, new_text_color,
        tree):
    for element in matching_elements:
        if new_bg_color:
            element_data = qs.element_data(
                element,
                tree,
                str_when_possible=False)
            element_data['backgroundColor'].text = str(new_bg_color)

        if new_text_color:
            for text_box in qs.find_by_scheme_type('Text', tree):
                element_data = qs.element_data(
                    text_box,
                    tree,
                    str_when_possible=False)
                element_data['color'].text = str(new_text_color)


if __name__ == '__main__':
    main()
