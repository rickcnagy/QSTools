"""Messages for command prompt input in replace_template_colors"""

import os

ask_file_path = "Drag and drop the raw data dump into this window. If you are making multiple changes to the file (such as changing changing color a to color b and changing color c to color d), use the output from the previous run."
valid_file = "Nice - that looks like a valid raw data dump!\n"
ask_colored_identifier = "What is the identifier of an element with the color you'd like to replace? For example, type \"att-tardy\" to replace the color of the att-tardy element over the whole report card. Be sure that the identifier is unique."
ask_replacement_color = "What color would you like to replace the color with? Input the value in hex format (i.e. \"#ffffff\"). Leave blank to leave the elements with this color as they are."
ask_change_text_color = "Would you like to change the text color of all text fields that are children of a box with this color (i.e. text with this background color)? If you are changing from a light to dark background (or vice-versa), it's often good to invert the text color. For a light text color, usually a light gray - such as #f0f0f0 - works better than white. Leave this blank to leave the text colors as they are."
didnt_find_elems = "Didn't find any elements with that identifier. Try a different one...\n"
invalid_file = "The input file doesn't look like a valid XML file or raw data dump."
invalid_hex = "That doesn't look like a valid hex value - try again."


def found_elements(colored_elements):
    return ("Great! Found an element with that identifier and {} total elements with the same color "
    "".format(len(colored_elements)))

def successful_save(new_file_path):
    return ("\n\nSuccess! Saved the replaced raw data dump as \"{}\"! To change another color on the template, run this script again and use the new file as the base raw data dump. When you're done changing colors, upload the raw data dump to the template on Control."
    "".format(os.path.basename(new_file_path)))
