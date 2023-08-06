import os
import time

from spelltinkle.view import View
from spelltinkle.history import History
from spelltinkle.color import Color

import subprocess

from spelltinkle.search import Search
from spelltinkle.exceptions import StopSession
from spelltinkle.utils import tolines

                    
class Document:
    def __init__(self, session=None):
        self.lines = ['']
        self.modified = False
        self.changes = None
        self.view = View(self)
        self.history = History()
        self.filename = None
        self.name = '[no name]'
        self.mode = 'Unknown'
        self.timestamp = -1000000000
        self.color = Color(self)
        self.handler = None
        self.session = None
        if session:
            self.set_session(session)
            
    def set_session(self, session):
        self.session = session
        self.view.set_screen(session.scr)
        
    def set_filename(self, name):
        self.filename = name
        self.name = os.path.basename(name)
    
    def build(self, w):
        lines = []
        for r, line in enumerate(self.lines):
            c = len(line)
            for i in range(1 + c // w):
                lines.append((r, i * w, min((i + 1) * w, c)))
        return lines
        
    def change(self, r1, c1, r2, c2, lines, remember=True):
        if c1 == c2 and r1 == r2 and lines == ['']:
            return
        self.color.stop()
        c3 = c1
        r3 = r1
        if c1 != c2 or r1 != r2:
            oldlines = self.delete_range(c1, r1, c2, r2)
        else:
            oldlines = ['']
        if lines != ['']:
            self.insert_lines(c1, r1, lines)
            r3 = r1 + len(lines) - 1
            if r3 == r1:
                c3 = c1 + len(lines[0])
            else:
                c3 = len(lines[-1])

        self.modified = True
        if remember:
            change = (c1, r1, c2, r2, c3, r3, lines, oldlines)
            self.history.append(change)
        self.color.update(c1, r1, c2, r2, lines)
        self.changes = (r1, r2, r3)
        self.view.move(r3, c3)
        return oldlines
        
    def insert_lines(self, c, r, lines):
        start = self.lines[r][:c]
        end = self.lines[r][c:]
        self.lines[r] = start + lines[0]
        self.lines[r + 1:r + 1] = lines[1:]
        self.lines[r + len(lines) - 1] += end

    def delete_range(self, c1, r1, c2, r2):
        start1 = self.lines[r1][:c1]
        end1 = self.lines[r1][c1:]
        start2 = self.lines[r2][:c2]
        end2 = self.lines[r2][c2:]
        if r1 == r2:
            oldlines = [start2[c1:]]
            self.lines[r1] = start1 + end2
        else:
            oldlines = [end1]
            oldlines.extend(self.lines[r1 + 1:r2])
            oldlines.append(start2)
            self.lines[r1] = start1
            del self.lines[r1 + 1:r2 + 1]
            self.lines[r1] += end2
        return oldlines

    def read(self, filename, positions={}):
        if ':' in filename:
            filename, r = filename.split(':')
            r = int(r) - 1
            c = 0
        else:
            r, c = positions.get(os.path.abspath(filename), (0, 0))
        self.set_filename(filename)
        try:
            with open(filename, encoding='UTF-8') as fd:
                lines = tolines(fd)
        except FileNotFoundError:
            return
        self.change(0, 0, 0, 0, lines, remember=False)
        self.modified = False
        self.timestamp = os.stat(filename).st_mtime
        self.view.move(r, c)

    def enumerate(self, r=0, c=0, direction=1):
        if direction == 1:
            while r < len(self.lines):
                yield r, c, self.lines[r][c:]
                r += 1
                c = 0
        else:
            yield r, 0, self.lines[r][:c]
            while r >= 1:
                r -= 1
                yield r, 0, self.lines[r]
                
    def get_range(self, r1, c1, r2, c2):
        lines = []
        for r, c, line in self.enumerate(r1, c1):
            if r == r2:
                lines.append(line[:c2 - c])
                return lines
            lines.append(line)

    def up(self):
        self.view.move(max(0, self.view.r - 1), None)

    def down(self):
        self.view.move(self.view.r + 1, None)

    def down1(self):
        view = self.view
        if len(view.lines) > view.y + 1:
            r, c1, c2 = view.lines[view.y + 1]
            c = c1 + view.x
            if c > c2:
                
                c = None
            self.view.move(r, c)

    def scroll_up(self):
        y1 = self.view.y1
        if y1 == 0:
            return
        r = self.view.r
        if self.view.y == y1 + self.view.text.h - 1:
            r -= 1
            if r < 0:
                return
        self.view.y1 -= 1
        self.view.move(r, None)
        
    def scroll_down(self):
        y1 = self.view.y1
        if y1 == len(self.view.lines) - 1:
            return
        r = self.view.r
        if self.view.y == y1:
            r += 1
        self.view.y1 += 1
        self.view.move(r, None)
        
    def left(self):
        self.view.move(*self.view.prev())

    def right(self):
        self.view.move(*self.view.next())

    def ctrl_up(self, dir='up'):
        if self.view.mark:
            mark = self.view.mark
            pos = self.view.pos
            if (mark > pos) ^ (dir in ['down', 'right']):
                getattr(self, dir)()
            else:
                self.mark()
                self.view.move(*mark)
        else:
            self.mark()
            getattr(self, dir)()
        
    def ctrl_down(self):
        self.ctrl_up('down')
        
    def ctrl_left(self):
        self.ctrl_up('left')
        
    def ctrl_right(self):
        self.ctrl_up('right')
        
    def mark_word(self):
        r, c = self.view.pos
        line = self.lines[r]
        n = len(line)
        if n == 0:
            return
        if c == n:
            c -= 1
        
        for c1 in range(0, c + 1):
            if line[c1:c + 1].isidentifier():
                break
        else:
            return
            
        for c2 in range(c + 1, n + 1):
            if not line[c1:c2].isidentifier():
                c2 -= 1
                break
                
        if c2 > c1:
            self.view.mark = r, c1
            self.view.move(r, c2, later=False)
            self.copy()
            
    def mouse1_clicked(self):
        x, y = self.session.scr.position
        if y == 0:
            for i, c in enumerate(self.view.tabcolumns):
                if c > x:
                    if i > 1:
                        docs = self.session.docs
                        docs.append(docs.pop(-i))
                        docs[-1].view.set_screen(self.session.scr)
                        docs[-1].changes = 42
                    break
        else:
            self.view.mouse(x, y)
        
    mouse1_pressed = mouse1_clicked
    
    def mouse1_released(self):
        x, y = self.session.scr.position
        if y > 0:
            self.mark()
            self.view.mouse(x, y)
            self.xselect()
            
    def xselect(self):
        r1, c1, r2, c2 = self.view.marked_region()
        lines = self.get_range(r1, c1, r2, c2)
        p = subprocess.Popen(['xsel', '--input'], stdin=subprocess.PIPE)
        p.communicate('\n'.join(lines).encode())
        
    def home(self):
        self.view.move(None, 0)

    def homehome(self):
        self.view.move(0, 0)

    def end(self):
        self.view.move(None, len(self.lines[self.view.r]))
    
    def endend(self):
        self.view.move(len(self.lines) - 1, len(self.lines[-1]))

    def page_up(self):
        self.view.move(max(0, self.view.r - self.view.text.h), None)
        
    def page_down(self):
        self.view.move(self.view.r + self.view.text.h, None)

    def copy(self):
        if not self.view.mark:
            return
        r1, c1, r2, c2 = self.view.marked_region()
        self.color.stop()
        lines = self.delete_range(c1, r1, c2, r2)
        self.insert_lines(c1, r1, lines)
        self.session.memory = lines
        self.xselect()
        
    def search_forward(self):
        self.handler = Search(self)

    def search_backward(self):
        self.handler = Search(self, -1)

    def view_files(self):
        from spelltinkle.filelist import FileList
        return FileList()

    def write(self):
        if self.filename is None:
            return self.write_as()
            
        try:
             t = os.stat(self.filename).st_mtime
        except FileNotFoundError:
            pass
        else:
            if 0:  # t > self.timestamp:
                pass
            """
                from spelltinkle.choise import Choise
                lines = ['diff'
                         'overwrite',
                         'cancel',
                         'rename']
                self.handler = Choise(self, lines)
                i = yield
                yield self.write_as()
            """
        with open(self.filename, 'w') as f:
            for line in self.lines[:-1]:
                print(line, file=f)
            if self.lines[-1]:
                print(self.lines[-1], file=f, end='')
        self.modified = False
        self.timestamp = os.stat(self.filename).st_mtime
        self.changes = 42

    def write_as(self):
        from spelltinkle.fileinput import FileInputDocument
        filename = self.filename or ''
        return FileInputDocument(filename, action='write as')

    def open(self):
        from spelltinkle.fileinput import FileInputDocument
        if self.filename:
            dir = os.path.split(self.filename)[0]
            if dir:
                dir += '/'
        else:
            dir = ''
        return FileInputDocument(dir)

    def help(self):
        from spelltinkle.help import HelpDocument
        return HelpDocument()

    def esc(self):
        self.view.mark = None
        self.changes = 42
        
    def mark(self):
        self.view.mark = self.view.pos

    def quit(self):
        if self.modified and self.filename is not None:
            self.write()
        self.color.stop()
        self.session.save()
        self.session.docs.remove(self)
        if len(self.session.docs) == 0:
            self.session.loop.stop()
        else:
            self.session.docs[-1].changes = 42
            self.session.update()

    def quit_all(self):
        for doc in self.session.docs[:]:
            doc.quit()

    def game(self):
        from spelltinkle.game import Game
        return Game(self.session)
