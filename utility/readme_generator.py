#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Generate README from in files in folder passed in via stdin

Command Line Args (in order):
    path to README directory
    (optional) README title
Example Usage:
./utility/readme_generator.py ./api 'API Scripts'
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

    entries = [ScriptEntry(folder_path, i) for i in filenames]
    entries += [FolderEntry(folder_path, i) for i in dirs]
    entries = [i for i in entries if i.is_valid()]
    entries = sorted(entries, key=lambda x: x.key())
    if not entries: return ''

    markdown = '{}\n===\n\n'.format(title) if title else ''
    for entry in entries:
        markdown += '####{}\n\n'.format(entry.md_title())
        docstring = entry.get_docstring()
        markdown += '{}\n\n'.format(docstring) if docstring else ''
    markdown = markdown.strip()
    return markdown


def test():
    print generate_markdown(
        '/Users/Rick/code/QuickSchools/QSTools/gui',
        'GUI Scripts',)


class ReadmeEntry(object):

    def __init__(self, folder_path, name):
        self.folder_path = folder_path
        self.name = name
        self.docstring = None

    def key(self):
        return ''.join([i.lower() for i in self.name if i.isalnum()])

    def get_docstring(self):
        return self.docstring

    def title(self):
        return self.name

    def md_title(self):
        return '[`{}`]({})'.format(self.title(), self.repo_link())

    def repo_link(self):
        return './{}'.format(self.name)

    def docstring(self):
        pass

    def is_valid(self):
        return True


class FolderEntry(ReadmeEntry):

    def title(self):
        return self.name + '/'


class ScriptEntry(ReadmeEntry):

    def is_valid(self):
        return self.is_valid_file() and self.is_valid_docstring()

    def is_valid_file(self):
        return self.is_py() or self.is_js()

    def is_valid_docstring(self):
        return (self.get_docstring() is not None
                and ('#NOT TESTED' not in self.get_docstring()))

    def is_py(self):
        return self.name[-3:] == '.py'

    def is_js(self):
        return self.name[-3:] == '.js'

    def get_docstring(self):
        if not self.docstring:
            if self.is_py():
                self.docstring = self.py_docstring()
            elif self.is_js():
                self.docstring = self.javadoc()
        return self.docstring

    def py_docstring(self):
        mod_name = self.name.replace('.py', '')
        self.docstring = __import__(mod_name).__doc__
        return self.docstring

    def javadoc(self):
        """Matches javadocs like: /** this is a javadoc! */"""
        with open(self.folder_path + '/' + self.name) as f:
            match = re.findall(r'/\*\*\s+(.+)\s+\*\/', f.read(), flags=re.DOTALL)
            if match:
                javadoc = match[0]
                javadoc = javadoc.replace('*', '')
                javadoc = javadoc.replace('#', '\#')
                javadoc = re.sub('\s+', ' ', javadoc)
                self.docstring = javadoc
        return self.docstring


if __name__ == '__main__':
    main()
