import subprocess
import textwrap

from spelltinkle.document import Document
from spelltinkle.replace import Replace
from spelltinkle.keys import aliases, typos
from spelltinkle.fromimp import complete_import_statement
from spelltinkle.complete import complete_word
from spelltinkle.utils import tolines, f, findword


class TextDocument(Document):
    completions = None
    
    def insert_character(self, char):
        r, c = self.view.pos
        for key in typos:
            if self.session.chars.endswith(key):
                self.change(r, c - len(key) + 1, r, c, [typos[key]])
                self.session.chars = ''
                return
                
        self.change(r, c, r, c, [char])
        
    def mouse2_clicked(self):
        x, y = self.session.scr.position
        if y == 0:
            return
        r, c = self.view.mouse(x, y)
        txt = subprocess.check_output(['xsel', '--output'])
        lines = tolines(line + '\n' for line in txt.decode().split('\n'))
        self.change(r, c, r, c, lines[:-1])
        self.view.mark = None
        
    def bs(self):
        r2, c2 = self.view.pos
        if self.lines[r2][:c2].isspace():
            c1 = (c2 - 1) // 4 * 4
            r1 = r2
        else:
            r1, c1 = self.view.prev()
        self.change(r1, c1, r2, c2, [''])
        
    def upper(self, f=str.upper):
        if self.view.mark:
            r1, c1, r2, c2 = self.view.marked_region()
            self.view.mark = None
        else:
            r1, c1 = self.view.pos
            r2, c2 = self.view.next()
        lines = self.change(r1, c1, r2, c2, [''])
        self.change(r1, c1, r1, c1, [f(line) for line in lines])
                
    def lower(self):
        self.upper(str.lower)

    def delete(self):
        if self.view.mark:
            r1, c1, r2, c2 = self.view.marked_region()
            lines = self.change(r1, c1, r2, c2, [''])
            self.session.memory = lines
            self.view.mark = None
        else:
            r1, c1 = self.view.pos
            r2, c2 = self.view.next()
            self.change(r1, c1, r2, c2, [''])

    def rectangle_delete(self):
        r1, c1, r2, c2 = self.view.marked_region()
        if c1 == c2:
            return
        if c2 < c1:
            c1, c2 = c2, c1
        lines = []
        for r in range(r1, r2 + 1):
            line = self.lines[r]
            n = len(line)
            if c1 >= n:
                continue
            c3 = min(n, c2)
            line = self.change(r, c1, r, c3, [''])[0]
            lines.append(line)
            
        self.session.memory = lines
        self.view.mark = None
        self.changed = 42
        
    def rectangle_insert(self):
        r1, c1, r2, c2 = self.view.marked_region()
        if c2 < c1:
            c1, c2 = c2, c1
        line = self.session.memory[0]
        for r in range(r1, r2 + 1):
            n = len(self.lines[r])
            if n >= c2:
                self.change(r, c1, r, c2, [line])
        
        self.view.mark = None
        self.changed = 42
        
    def indent(self, direction=1):
        if self.view.mark:
            r1, c1, r2, c2 = self.view.marked_region()
            if c2 > 0:
                r2 += 1
        else:
            r1 = self.view.r
            r2 = r1 + 1
        if direction == 1:
            for r in range(r1, r2):
                self.change(r, 0, r, 0, ['    '])
        else:
            for line in self.lines[r1:r2]:
                if line and not line[:4].isspace():
                    return
            for r in range(r1, r2):
                self.change(r, 0, r, min(4, len(self.lines[r])), [''])
            r, c = self.view.mark
            self.view.mark = r, min(c, len(self.lines[r]))
            self.view.move(*self.view.pos)
            
    def dedent(self):
        self.indent(-1)
                
    def undo(self):
        self.history.undo(self)

    def redo(self):
        self.history.redo(self)

    def replace(self):
        self.handler = Replace(self)

    def paste(self):
        r, c = self.view.pos
        self.change(r, c, r, c, self.session.memory)
        self.view.mark = None
        
    def delete_to_end_of_line(self, append=False):
        r, c = self.view.pos
        if (r, c) == self.view.next():
            return
        line = self.lines[r]
        if c == 0 and line.strip() == '' and r < len(self.lines) - 1:
            lines = self.change(r, 0, r + 1, 0, [''])
        elif c == len(line):
            lines = self.change(r, c, r + 1, 0, [''])
        else:
            lines = self.change(r, c, r, len(line), [''])
        if append:
            if self.session.memory[-1] == '':
                self.session.memory[-1:] = lines
            else:
                self.session.memory.append('')
        else:
            self.session.memory = lines

    def delete_to_end_of_line_again(self):
        self.delete_to_end_of_line(True)

    def enter(self):
        r, c = self.view.pos
        self.change(r, c, r, c, ['', ''])
        self.view.pos = (r + 1, 0)
        self.tab()
        
    def normalize_space(self):
        r, c = self.view.pos
        line = self.lines[r]
        n = len(line)
        c1 = len(line[:c].rstrip())
        c2 = n - len(line[c:].lstrip())
        if c1 == c2:
            return
        if c2 < n:
            if not (line[c2] in ')]}' or
                    c1 > 0 and line[c1 - 1] in '([{'):
                c2 -= 1
        self.change(r, c1, r, c2, [''])
        self.view.move(r, c1)

    def complete(self):
        complete_word(self)
        
    # async
    def jedi(self):
        import jedi
        from jedi import settings
        settings.case_insensitive_completion = False
        from spelltinkle.fromimp import complete
        r, c = self.view.pos
        s = jedi.Script('\n'.join(self.lines), r + 1, c, '')
        compobjs = s.completions()
        completions = [comp.complete for comp in compobjs]
        w = complete('', completions)
        if w:
            self.change(r, c, r, c, [w])
        elif completions:
            if completions == self.completions:
                from spelltinkle.choise import Choise
                lines = [f ^ '{comp.name} ({comp.type})'
                         for comp in compobjs]
                self.handler = Choise(self, lines)
                self.completions = None
                i = yield
                r, c = self.view.pos
                self.change(r, c, r, c, [completions[i]])
                yield
            else:
                self.completions = completions
        
    def format(self):
        r1 = self.view.r
        txt = self.lines[r1]
        r2 = r1 + 1
        while r2 < len(self.lines):
            line = self.lines[r2]
            if len(line) == 0 or line[0] == ' ':
                break
            r2 += 1
            txt += ' ' + line
        width = self.view.text.w - self.view.wn - 1
        lines = textwrap.wrap(txt, width - 3, break_long_words=False)
        self.change(r1, 0, r2 - 1, len(self.lines[r2 - 1]), lines)
            
    def tab(self):
        r, c = self.view.pos
        for key in aliases:
            if self.session.chars.endswith(key):
                self.change(r, c - len(key), r, c, [aliases[key]])
                self.session.chars = ''
                return
                
        if complete_import_statement(self):
            return
                
        r0 = r - 1
        p = []
        pend = False
        indent = None
        while r0 >= 0:
            line = self.lines[r0]
            if line and not line.isspace():
                n = len(line)
                for i in range(n - 1, -1, -1):
                    x = line[i]
                    j = '([{'.find(x)
                    if j != -1:
                        if not p:
                            if i < n - 1:
                                indent = i + 1
                                break
                            pend = True
                        elif p.pop() != ')]}'[j]:
                            indent = 0
                            # message
                            break
                    elif x in ')]}':
                        p.append(x)

                if indent is not None:
                    break
                
                if not p:
                    indent = len(line) - len(line.lstrip())
                    break

            r0 -= 1
        else:
            indent = 0
            line = '?'
                        
        if pend or line.rstrip()[-1] == ':':
            indent += 4

        line = self.lines[r]
        i = len(line) - len(line.lstrip())
        if i < indent:
            self.change(r, 0, r, 0, [' ' * (indent - i)])
        elif i > indent:
            self.change(r, 0, r, i - indent, [''])
        c += indent - i
        if c < indent:
            c = indent
        self.view.move(r, c)

    def task_sort(self):
        r, c = self.view.pos
        line1 = self.lines[r]
        c1 = findword(line1, c)
        tag = line1[c1:].split(',', 1)[0]
        lines = []
        top = []
        for line in self.lines[:-1]:
            if tag in line.rsplit(' ', 1)[1][1:-1].split(','):
                top.append(line)
            else:
                lines.append(line)
        self.change(0, 0, len(self.lines) - 1, 0, top + lines + [''])
        self.view.move(self.lines.index(line1), c)

    def task_renumber(self):
        lines = []
        for i, line in enumerate(self.lines[:-1]):
            text, tags = line.rsplit(' ', 1)
            tags = tags[1:-1].split(',')
            if tags[-1].isdigit():
                tags.pop()
            line = text + ' [' + ','.join(tags) + ',' + str(i + 1) + ']'
            lines.append(line)
        r, c = self.view.pos
        self.change(0, 0, len(self.lines) - 1, 0, lines + [''])
        self.view.move(r, c)

    def task_ordered(self):
        def key(line):
            x = line.rsplit(',', 1)[1][:-1]
            if x.isdigit():
                return int(x)
            return 0
        r, c = self.view.pos
        line = self.lines[r]
        self.change(0, 0, len(self.lines) - 1, 0,
                    sorted(self.lines[:-1], key=key) + [''])
        self.view.move(self.lines.index(line), c)

    def replace2(self):
        pass
