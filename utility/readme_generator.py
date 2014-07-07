#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Generate README from docstrings in files in folder passed in via stdin

Command Line Args (in order):
    path to README directory
    (optional) title of Markdown document
"""

import os
import sys
import re

file_extensions = ['py', 'js']


def main():
    folder = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) >= 3 else None
    md = generate_markdown(folder, title)
    with open('{}/README.md'.format(folder), 'w') as f:
        f.write(md)


def generate_markdown(folder_path, title):
    sys.path.append(folder_path)
    walk = next(i for i in os.walk(folder_path))
    folder_path = walk[0]
    dirs = walk[1]
    filenames = walk[2]
    filenames = list(set(filenames))
    py_files = [i for i in filenames if i[-2:] == 'py']
    js_files = [i for i in filenames if i[-2:] == 'js']

    # {filename: docstring}
    doc = {}
    def set_docstring(filename, docstring):
        docstring = docstring or ''
        doc[filename] = docstring

    for dirname in dirs:
        doc[dirname] = 'folder'
    for filename in py_files:
        set_docstring(filename, parse_py(filename))
    for filename in js_files:
        set_docstring(filename, parse_js(filename, folder_path))

    if not doc: return ''

    markdown = '{}\n===\n\n'.format(title) if title else ''
    for filename in sorted(doc.keys()):
        docstring = doc[filename]
        if docstring == 'folder':
            filename = filename + '/'
            docstring = ''
        markdown += '####`{}`\n\n{}\n\n'.format(filename, docstring)
    markdown = markdown.strip()
    return markdown


def parse_py(filename):
    mod_name = filename.replace('.py', '')
    return __import__(mod_name).__doc__


def parse_js(filename, folder_path):
    """Matches javadocs like: /** this is a javadoc! */"""
    with open(folder_path + '/' + filename) as f:
        match = re.findall(r'/\*\*\s+(.+)\s+\*\/', f.read(), flags=re.DOTALL)
        if match:
            javadoc = match[0]
            javadoc = javadoc.replace('*', '')
            javadoc = re.sub(r'\n\s+ ', '\n ', javadoc).strip()
            return javadoc


def test():
    print generate_markdown(
        '/Users/Rick/code/QuickSchools/QSTools/gui',
        'GUI Scripts',
    )


if __name__ == '__main__':
    main()
