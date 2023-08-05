from math import log10

from spelltinkle.color import highlight_codes

NHC = len(highlight_codes)

P = {'(': ')', ')': '(', '[': ']', ']': '[', '{': '}', '}': '{'}


class View:
    def __init__(self, doc, show_line_numbers=True):
        self.doc = doc
        self.show_line_numbers = show_line_numbers
        
        self.y1 = 0
        self.x = 0
        self.y = 0
        self.c = 0
        self.r = 0
        self.c0 = None
        
        self.ys1 = 0
        self.ys2 = 0

        self.mark = None

        self.message = None

        self.moved = False
        self.scrolled = True

        self.lines = None
        self.wn = None

    def set_screen(self, scr):
        self.tabs = scr.subwin(1, scr.w, 0, 0)
        self.text = scr.subwin(scr.h - 2, scr.w, 1, 0)
        self.info = scr.subwin(1, scr.w, scr.h - 1, 0)

    @property
    def pos(self):
        return self.r, self.c
        
    @pos.setter
    def pos(self, p):
        self.r, self.c = p
        
    def prev(self):
        if self.c == 0:
            if self.r > 0:
                return (self.r - 1, len(self.doc.lines[self.r - 1]))
            return (0, 0)
        return (self.r, self.c - 1)

    def next(self):
        if self.c == len(self.doc.lines[self.r]):
            if self.r == len(self.doc.lines) - 1:
                return self.pos
            return (self.r + 1, 0)
        return (self.r, self.c + 1)

    def move(self, r=None, c=0, later=True):
        if later:
            self.moved = (r, c)
            return

        if c is None:
            if self.c0 is None:
                self.c0 = self.c
            c = self.c0
        else:
            self.c0 = None
            
        if r is None:
            r = self.r
        L = len(self.doc.lines)
        if r >= L:
            r = L - 1
            c = len(self.doc.lines[r])
        c = min(c, len(self.doc.lines[r]))
        
        self.c = c
        self.r = r
 
        w = self.text.w - self.wn - 1
        self.y = 0
        for row, c1, c2 in self.lines:
            if row == r and c1 <= c <= c2:
                self.x = c - c1
                if self.x == w:
                    self.y += 1
                    self.x = 0
                break
            self.y += 1
        
        h = self.text.h
        if self.y < self.y1:
            self.y1 = self.y
            self.scrolled = True
        elif self.y >= self.y1 + h:
            self.y1 = self.y + 1 - h
            self.scrolled = True

        Y = len(self.lines)
        s1 = self.y1 / Y
        s2 = min(h, Y) / Y
        self.ys1 = int(s1 * min(h, Y))
        self.ys2 = self.ys1 + max(1, int(round(s2 * min(h, Y))))

        self.moved = False

        return self.pos

    def marked_region(self):
        if self.mark is None:
            return 0, 0, -1, 0
        if self.mark < self.pos:
            return self.mark + self.pos
        else:
            return self.pos + self.mark

    def mouse(self, x, y):
        r, c1, c2 = self.lines[min(self.y1 + y - 1, len(self.lines) - 1)]
        c = min(c1 + max(0, x - self.wn - 1), c2)
        self.move(r, c, later=False)
        self.moved = (r, c)
        return r, c
        
    def build(self):
        self.wn = int(log10(len(self.doc.lines))) + 1
        w = self.text.w - self.wn - 1
        self.lines = self.doc.build(w)

    def update(self, session):
        if self.doc.changes or self.lines is None:
            self.build()
        elif not self.moved and self.message is None:
            return

        if self.moved:
            self.move(*self.moved, later=False)
            highlight = self.match_parenthesis()
        else:
            highlight = []
            
        self.update_info_line()
        self.update_tabs(session)

        ra, ca, rb, cb = self.marked_region()

        handler = self.doc.handler
        try:
            choises = handler.choises
        except AttributeError:
            choises = []
            
        text = self.text
        
        y2 = self.y1 + self.text.h
        w = text.w - self.wn - 1
        i = 0
        for r, c1, c2 in self.lines[self.y1:y2]:
            text.move(i, 0)
            cn = 4 * NHC + 5
            if self.ys1 <= i < self.ys2:
                cn += 1
            if c1 == 0:
                text.write('{:{w}} '.format(r + 1, w=self.wn), cn)
            else:
                text.write(' ' * (self.wn + 1), cn)

            line = self.doc.lines[r][c1:c2]
            try:
                colors = self.doc.color.colors[r][c1:c2]
            except IndexError:
                colors = bytearray(len(line))
            m = w - len(line)

            line += ' ' * m
            colors = colors + bytearray(m)
            
            if r == self.r:
                colors = [c + NHC for c in colors]
            
            for rh, ch in highlight:
                if rh == r and c1 <= ch < c2:
                    colors[ch - c1] = colors[ch - c1] % NHC + 2 * NHC
                    
            if ra <= r <= rb:
                if r > ra:
                    ca = c1
                if r == rb:
                    cc = cb
                else:
                    cc = c2
                for c in range(max(ca, c1), min(cc, c2)):
                    colors[c - c1] = colors[c - c1] % NHC + 3 * NHC

            if i < len(choises):
                choise = choises[i]
                n = len(choise)
                line = line[:5] + choise + line[n + 5:]
                if i == handler.r:
                    color = 4 * NHC + 6
                else:
                    color = 4 * NHC + 5
                colors[5:5 + n] = [color] * n

            text.write(line, colors)
            i += 1
        
        if i + self.y1 == len(self.lines):
            text.move(i - 1, self.wn + 1 + c2 - c1)
            text.write(' ' * (w - c2 + c1), 4 * NHC + 7)
            
        while i < self.text.h:
            text.move(i, 0)
            text.write(' ' * self.text.w, 4 * NHC + 7)
            i += 1
        
        text.move(self.y - self.y1, self.x + self.wn + 1)
        text.refresh()
        self.scrolled = False
        self.moved = False

    def match_parenthesis(self):
        r1, c1 = self.pos
        line = self.doc.lines[r1]
        p1 = line[c1:c1 + 1]
        p2 = P.get(p1)
        if not p2:
            if c1 > 0 and line[c1 - 1] in ')]}':
                c1 -= 1
                p1 = line[c1]
                p2 = P[p1]
            else:
                return []
        n = 0
        if p1 in '([{':
            for r2, c2, line in self.doc.enumerate(r1, c1 + 1):
                for c2, p in enumerate(line, c2):
                    if p == p1:
                        n += 1
                    elif p == p2:
                        if n == 0:
                            return [(r1, c1), (r2, c2)]
                        n -= 1
        else:
            for r2, c2, line in self.doc.enumerate(r1, c1, -1):
                c2 = len(line) - 1
                for p in line[::-1]:
                    if p == p1:
                        n += 1
                    elif p == p2:
                        if n == 0:
                            return [(r2, c2), (r1, c1)]
                        n -= 1
                    c2 -= 1
                        
        return []
        
    def update_info_line(self):
        line = self.message

        color = 4 * NHC + 3
        if line is None:
            if self.doc.modified:
                status = '[modified]'
            else:
                status = ''
            r, c = self.doc.view.pos
            name = self.doc.filename
            if name is None:
                name = '[no name]'
            line = 'line:{:{w}} col:{:2} {} {} [{}]'.format(
                r + 1, c + 1, name, status, self.doc.mode, w=self.wn)
            nwarn = len(self.doc.color.report)
            if nwarn:
                line += ' [{}]'.format(nwarn)
            colors = color + 1
        elif not isinstance(line, str):
            line, n = line
            colors = [color] * self.info.w
            colors[n] = color + 1
        else:
            colors = color
            
        line += ' ' * (self.info.w - len(line))
        line = line[:self.info.w - 1]
        self.info.move(0, 0)
        self.info.write(line, colors)
        self.info.refresh()

    def update_tabs(self, session):
        line = ' ' * (self.wn + 1)
        c = NHC * 4
        colors = [c + 2] * (self.wn + 1)
        self.tabcolumns = [self.wn]
        for doc in session.docs[::-1]:
            line += ' ' + doc.name + ' '
            colors.extend([c + doc.modified] * (len(doc.name) + 2))
            c = NHC * 4 + 2
            self.tabcolumns.append(len(line))
            
        line += ' ' * (self.tabs.w - len(line))
        colors += [c] * (self.tabs.w - len(colors))

        self.tabs.move(0, 0)
        self.tabs.write(line, colors)
        self.tabs.refresh()
