import re
import threading

from spelltinkle.color import highlight_codes

NHC = len(highlight_codes)

TRANSLATION = bytes.maketrans(bytes(range(2 * NHC)),
                              bytes(list(range(NHC)) * 2))


def make_regular_expression(s):
    if s.islower():
        flags = re.IGNORECASE
    else:
        flags = 0
    return re.compile(re.escape(s), flags)
        
        
class Search:
    def __init__(self, doc, direction=1):
        self.session = doc.session
        self.doc = doc
        self.direction = direction
        
        self.string = None
        self.match = None
        self.positions = None
        self.paint_thread = None
        
        self.reset()
        
        if doc.view.mark:
            r1, c1, r2, c2 = doc.view.marked_region()
            if r1 == r2 and c2 > c1:
                doc.view.mark = None
                self.session.lastsearchstring = doc.lines[r1][c1:c2]
                self.search_forward(direction)

    def reset(self):
        self.string = ''
        self.match = ''
        self.update_info_line()
        self.positions = [self.doc.view.pos + ('',)]

    def search_forward(self, direction=1):
        if self.direction != direction:
            self.direction *= -1
            self.session.lastsearchstring = self.string
            self.reset()
        if self.string == '':
            for c in self.session.lastsearchstring:
                self.string += c
                self.find()
            self.paint()
            return
        self.find(True)

    def search_backward(self):
        self.search_forward(direction=-1)

    def insert_character(self, c):
        self.string += c
        self.find()
        self.paint()
        
    def bs(self):
        if len(self.string) > len(self.match):
            self.string = self.string[:-1]
            r, c = self.doc.view.pos
        elif len(self.positions) == 1:
            return
        else:
            self.positions.pop()
            r, c, self.string = self.positions[-1]
            self.match = self.string
        self.update_info_line()
        self.doc.view.move(r, c)
        self.paint()

    def unknown(self, name):
        self.clean()
        self.doc.view.message = None
        self.doc.view.update_info_line()
        self.session.lastsearchstring = self.string
        self.doc.handler = None
        return getattr(self.doc, name)()
            
    def find(self, next=False):
        d = self.direction
        reo = make_regular_expression(self.string[::d])
        r, c = self.doc.view.pos

        if d == 1:
            if next:
                c += len(self.match)

            for dr, line in enumerate(self.doc.lines[r:]):
                if dr == 0:
                    m = reo.search(line, c)
                else:
                    m = reo.search(line)
                if m:
                    c = m.start()
                    r += dr
                    self.match = self.string
                    self.update_info_line()
                    self.positions.append((r, c, self.string))
                    self.doc.view.move(r, c)
                    return
        else:
            if next:
                c -= len(self.match)

            for dr, line in enumerate(self.doc.lines[r::-1]):
                N = len(line)
                if dr == 0:
                    m = reo.search(line[::-1], N - c)
                else:
                    m = reo.search(line[::-1])
                if m:
                    c = N - m.start()
                    r -= dr
                    self.match = self.string
                    self.update_info_line()
                    self.positions.append((r, c, self.string))
                    self.doc.view.move(r, c)
                    return
                    
        self.update_info_line()
        self.doc.view.update(self.session)
                
    def update_info_line(self):
        view = self.doc.view
        view.message = 'Search: {}({})'.format(self.match,
                                               self.string[len(self.match):])
        view.update_info_line()

    def paint(self):
        if self.paint_thread:
            self.paint_thread.join()
        self.paint_thread = threading.Thread(target=self.painter)
        self.paint_thread.start()
        
    def painter(self):
        self.clean()
        reo = make_regular_expression(self.string)
        for r, line in enumerate(self.doc.lines):
            for match in reo.finditer(line):
                for c in range(match.start(), match.end()):
                    self.doc.color.colors[r][c] += NHC
        self.session.loop.call_soon(self.session.draw_colors)
                    
    def clean(self):
        for line in self.doc.color.colors:
            line[:] = line.translate(TRANSLATION)
