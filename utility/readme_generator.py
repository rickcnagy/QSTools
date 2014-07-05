#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Generate README from docstrings in files in folder passed in via stdin

Command Line Args (in order):
    path to README directory
    (optional) title of Markdown document
"""

import os
import sys


def main():
    folder = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) >= 3 else None
    md = generate_markdown(folder, title)
    with open('{}/README.md'.format(folder), 'w') as f:
        f.write(md)


def generate_markdown(folder_path, title):
    sys.path.append(folder_path)
    walk = next(i for i in os.walk(folder_path))
    filenames = walk[2]
    py_files = [os.path.splitext(i)[0] for i in filenames if '.py' in i]
    py_files = list(set(py_files))
    py_files.sort()

    markdown = '{}\n===\n'.format(title) if title else ''
    for file in py_files:
        filename = file + '.py'
        docstring = __import__(file).__doc__
        markdown += '---\n`{}`\n\n{}\n\n'.format(filename, docstring)
    markdown.strip('---')
    return markdown


def test():
    generate_markdown(
        '/Users/Rick/Dropbox/code/QuickSchools/QSTools/api',
        'API Scripts',
    )


if __name__ == '__main__':
    main()
