#########################################################################
#  The MIT License (MIT)
#
#  Copyright (c) 2014~2015 CIVA LIN (林雪凡)
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files
#  (the "Software"), to deal in the Software without restriction, including
#  without limitation the rights to use, copy, modify, merge, publish,
#  distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so,
#  subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##########################################################################


import subprocess
import datetime as DT
import cmd
import sys
import math
import re


class Note():
    """A note info warper"""
    def __init__(self, path, rootpath):
        self.path = path
        self.rootpath = rootpath

    @property
    def title(self):
        return self.path.stem

    @property
    def filename(self):
        return self.path.name

    @property
    def parent_dirname(self):
        return self.path.parent.name

    @property
    def grandparent_dirname(self):
        return self.path.parent.parent.name

    @property
    def absolute_path(self):
        return str(self.path.resolve())

    @property
    def absolute_parent_dirpath(self):
        return str(self.path.parent.resolve())

    @property
    def root_relative_path(self):
        return str(self.path.relative_to(self.rootpath))

    @property
    def root_relative_dirname(self):
        return str(self.path.relative_to(self.rootpath).parent)

    @property
    def top_dirname(self):
        return self.path.relative_to(self.rootpath).parts[0]

    @property
    def mtime(self):
        return DT.datetime.fromtimestamp(self.path.stat().st_mtime)

    @property
    def atime(self):
        return DT.datetime.fromtimestamp(self.path.stat().st_atime)

    def get_properties(self):
        return {
            'title': self.title,
            'filename': self.filename,
            'parent_dirname': self.parent_dirname,
            'absolute_path': self.absolute_path,
            'root_relative_path': self.root_relative_path,
            'root_relative_dirname': self.root_relative_dirname,
            'top_dirname': self.top_dirname,
            'mtime': self.mtime,
            'atime': self.atime,
            }


class NotePager():
    def __init__(self, notes, show_reverse,
                 editor, file_browser, page_size, output_format):
        self.notes = notes
        self.show_reverse = show_reverse
        self.editor = editor
        self.file_browser = file_browser
        self.page_size = page_size
        self.output_format = output_format
        self.page = 1

    def get_page_count(self):
        return int(len(self.notes) / self.page_size) + 1

    def set_page(self, page):
        def restrict_page(want_page):
            max_page = self.get_page_count()
            min_page = 1
            return min(max(min_page, want_page), max_page)

        self.page = restrict_page(page)

    def set_page_size(self, page_size):
        def restrict_page_size(want_page_size):
            min_page_size = 1
            return max(want_page_size, min_page_size)

        page_size = restrict_page_size(page_size)
        first_item_number = self.page_size * (self.page - 1) + 1
        new_page = math.ceil(first_item_number / page_size)
        self.page_size = page_size
        self.set_page(new_page)

    def get_notes(self):
        startindex = (self.page - 1) * self.page_size
        endindex = ((self.page - 1) + 1) * self.page_size
        return self.notes[startindex:endindex]

    def get_page_content(self):
        notes = self.get_notes()
        notes_with_index = list(enumerate(notes, start=1))
        if self.show_reverse:
            notes_with_index.reverse()
        texts = [('{index:>2}) ' + self.output_format).format(
                 index=index, **note.get_properties())
                 for index, note in notes_with_index]
        texts.append('[page {}/{}]'.format(self.page, self.get_page_count()))
        result = '\n'.join(line for line in texts)
        return result

    def get_note(self, open_number):
        notes = self.get_notes()
        max_number = len(notes)
        min_number = 1
        corrected_open_number = min(max(min_number, open_number), max_number)
        return notes[corrected_open_number - 1]

    def open_editor(self, note, editor=None):
        if editor is None:
            editor = self.editor
        try:
            subprocess.call([editor, note.absolute_path])
        except FileNotFoundError:
            print('editor: "{}" not found. cancel.'.format(editor))

    def open_file_browser(self, note, file_browser=None):
        if file_browser is None:
            file_browser = self.file_browser
        try:
            subprocess.call([file_browser, note.absolute_parent_dirpath])
        except FileNotFoundError:
            print('file_browser: "{}" not found. cancel.'.format(file_browser))


class NoteListSelector2(cmd.Cmd):
    prompt = 'open> '

    def __init__(self, note_pager):
        super().__init__()
        self.note_pager = note_pager
        self.intro = ('Loli Note Selector (press "help" for usage)\n'
                      '===========================================\n' +
                      self.note_pager.get_page_content())

    def print_page(self):
        print(self.note_pager.get_page_content())

    def postcmd(self, stop, line):
        if all([line.split()[0] not in ('help', ),
                not line.startswith('?'),
                not line.startswith('!')]):
            self.print_page()

    def exit(self):
        '''Exit program'''
        sys.exit(0)

    def emptyline(self):
        self.exit()

    def default(self, line):
        '''default oparation'''
        items = [item.strip() for item in re.split('[/@]', line, 1)
                 if item != '']

        try:
            number = int(items[0])
        except:
            print('command not found: try "help" or "help usage"'
                  ' for more detail.')
            return
        note = self.note_pager.get_note(number)

        if len(items) == 1:
            executable = None
        elif len(items) == 2:
            executable = items[1]
        else:
            print('command not found: try "help" or "help usage"'
                  ' for more detail.')
            return

        if '/' in line:
            self.note_pager.open_file_browser(note, executable)
            self.exit()
        else:
            self.note_pager.open_editor(note, executable)
            self.exit()

    def do_next(self, arg):
        '''Go to next page(s)
        example: next [page_count]'''
        try:
            number = max(int(arg), 1)
        except:
            number = 1
        self.note_pager.set_page(self.note_pager.page + number)

    def do_prev(self, arg):
        '''Go to previous page(s)
        example: previous [page_count]'''
        try:
            number = max(int(arg), 1)
        except:
            number = 1
        self.note_pager.set_page(self.note_pager.page - number)

    def do_first(self, arg):
        '''Go to first page
        example: first'''
        self.note_pager.set_page(1)

    def do_last(self, arg):
        '''Go to last page
        example: last'''
        self.note_pager.set_page(99999999)

    def do_goto(self, arg):
        '''Go to a special page.
        example: goto <page_number>'''
        try:
            number = max(int(arg), 1)
        except:
            return
        self.note_pager.set_page(number)

    def do_size(self, arg):
        '''Set the page size.
        It's will change page and try to keep first item still in list.
        example: size <item_count>'''
        try:
            number = max(int(arg), 1)
        except:
            return
        self.note_pager.set_page_size(number)

    def help_usage(self):
        print('Open a note:\n'
              '    <number>\n'
              '    <number> @\n'
              '        - open one file with default editor\n'
              '    <number> @ <editor>\n'
              '        - open one file with special editor\n'
              'Open a note directory:\n'
              '    <number> /\n'
              '        - open folder with default filebrowser\n'
              '    <number> / <file_browser>\n'
              '        - open folder with special filebrowser\n'
              'Example:\n'
              '    5\n'
              '    5@gedit\n'
              '    5/\n'
              '    5/nautilus\n')


def start_selector(notes, show_reverse,
                   editor, file_browser, page_size, output_format):
    note_pager = NotePager(notes, show_reverse,
                           editor, file_browser, page_size, output_format)
    nls = NoteListSelector2(note_pager)
    nls.cmdloop()
