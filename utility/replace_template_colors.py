#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import os
from textwrap import *
import sys
from xml.etree.ElementTree import ElementTree
import string

wrapper = TextWrapper()


def main():
    global f
    global tree
    print '\n'
    file_path = raw_input(wrapper.fill("Drag and drop the raw data dump into this window. If you are making multiple changes to the file (such as changing changing color a to color b and changing color c to color d), use the output from the previous run.") + '\n').strip().replace('\\', '')
    validate_and_format_xml(file_path)
    print "Nice - that looks like a valid raw data dump!\n"
    
    # now that it's been validated and formatted, actually parse
    tree = ElementTree()
    tree.parse(f)
    colored_elements = find_colored_elements(raw_input(wrapper.fill("What is the identifier of an element with the color you'd like to replace? For example, type \"att-tardy\" to replace the color of the att-tardy element over the whole report card. Be sure that the identifier is unique.") + '\n').strip())
    
    s = 's' if len(colored_elements) else ''
    print(wrapper.fill("Great! Found an element with that identifier and {} element{} with the same color ".format(len(colored_elements), s)))
    
    new_elem_dec = get_decimal_value(raw_input('\n' + wrapper.fill("What color would you like to replace the color with? Input the value in hex format (i.e. \"#ffffff\"). Leave blank to leave the elements with this color as they are.") + '\n'))
    
    new_text_dec = get_decimal_value(raw_input('\n' + wrapper.fill("Would you like to change the text color of all text fields that are children of a box with this color (i.e. text with this background color)? If you are changing from a light to dark background (or vice-versa), it's often good to invert the text color. For a light text color, usually a light gray - such as #f0f0f0 - works better than white. Leave this blank to leave the text colors as they are.") + '\n'))
    
    replace_colored_elements_and_children(colored_elements, new_elem_dec, new_text_dec)
    new_file_path = iterative_file_name(file_path)
    tree.write(new_file_path)
    print '\n\n' + wrapper.fill("Success! Saved the replaced raw data dump as \"" + os.path.basename(new_file_path) + "\"! To change another color on the template, run this script again and use the new file as the base raw data dump. When you're done changing colors, upload the raw data dump to the template on Control." )

def validate_and_format_xml(file_path):
    global f
    try:
        f = open(file_path)
        contents = f.read()
        f.seek(0)
        if contents[0] != '<':
            raise NotXMLError
        # add the xml version if it isn't already there (which sometimes it isn't)
        if not '<?xml version=' in contents:
            f.close()
            f = open(file_path, 'w')
            f.write('<?xml version="1.0"?>\n\n' + contents)
            f.close()
            f = open(file_path)
    except IOError:
        sys.exit("Couldn't open file at " + file_path)
    except NotXMLError:
        sys.exit("Couldn't parse. It doesn't look like " + os.path.basename(file_path) + " is a raw data dump.")

def find_colored_elements(identifier):
    colored_element = None
    
    # find the first element with that identifier
    for elem in tree.iter():
        for attrib in elem.findall('s'):
            if attrib.text == identifier:
                colored_element = elem
    if colored_element is None:
        return find_colored_elements(raw_input("Didn't find any elements with that identifier. Try a different one...\n").strip())
    else:
        colored_elements = [colored_element]
        
        # find all the elements with the same color
        old_color = colored_element.find('i').text
        for elem in tree.iter():
            color = elem.find('i')
            if (color is not None and color.text == old_color):
                colored_elements.append(elem)
                
        return colored_elements
        
def get_decimal_value(hex):
    hex = hex.strip().lstrip('#')
    try:
        if (hex == ''): return hex
        hex = '0x' + hex
        dec = int(hex, 0)
        return str(dec)
    except:
        return get_decimal_value(raw_input("That doesn't look like a valid hex value. Try again...\n"))
        
def replace_colored_elements_and_children(colored_elements, new_color, new_text_color):
    elem_replace_count = 0
    text_replace_count = 0
    try:
        # change all text
        for elem in colored_elements:
            if new_color != '':
                elem.find('i').text = new_color 
                elem_replace_count += 1
        
            # work with children elements if it's a box
            elem_name = elem.attrib.get('n')
            if (elem_name is not None and elem_name == 'Box' and new_text_color != ''):
                for child in elem.iter():
                    child_name = child.attrib.get('n')
                    if (child_name and child_name == 'Text'):
                        child.find('i').text = new_text_color
                        text_replace_count += 1
        print (wrapper.fill('Successfully changed the color on {} parent element{} and {} child text box{}\n'.format(
            elem_replace_count,
            's' if not elem_replace_count == 1 else '',
            text_replace_count,
            'es' if not text_replace_count == 1 else ''
        )))
    except:
        sys.exit("There was an issue replacing the colors on the template. Try again.")

def iterative_file_name(old_path):
    filename = os.path.splitext(old_path)[0]
    file_number = 0
    if not '_changed' in filename:
        filename += '_changed(0).xml'
    else:
        # this is /.../../file_changed(1)
        try:
            file_number = int(filename[-2])
        except:
            pass
        file_number += 1
        filename = filename[0:-2] + str(file_number) + ').xml'
    return filename
                         
class NotXMLError(Exception):
    pass

if __name__ == '__main__':
    main()