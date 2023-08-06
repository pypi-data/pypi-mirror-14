import re
import threading

from spelltinkle.input import Input
from spelltinkle.search import TRANSLATION, make_regular_expression, NHC
from spelltinkle.utils import f

        
class Replace(Input):
    def __init__(self, doc):
        self.doc = doc
        self.view = doc.view
        self.replace = None
        Input.__init__(self)
        self.regex = None
        self.paint_thread = None

        if doc.view.mark:
            r1, c1, r2, c2 = doc.view.marked_region()
            if r1 == r2 and c2 > c1:
                doc.view.mark = None
                find = doc.lines[r1][c1:c2]
                self.update(f ^ '/{find}//')
                self.c = len(find) + 2
                self.view.pos = r1, c1
        else:
            self.update('///')
            self.c = 1 
        
    def update(self, string=None):
        Input.update(self, string)
        if self.replace is None:
            text = '/find/replace/: ' + self.string
        else:
            text = 'Replace?  yes, no or all!'
        self.view.message = text
        self.view.update_info_line()
        
    def enter(self):
        if self.replace is None:
            self.find, self.replace = self.string[1:-1].split(self.string[0])
            self.regex = re.compile(re.escape(self.find))
            self.next()
            self.update()
            
    def insert_character(self, chr):
        if self.replace is None:
            Input.insert_character(self, chr)
            return
            
        r, c = self.view.pos
        
        if chr == 'n':
            self.view.move(r, c + len(self.find))
            self.next()
        elif chr == 'y':
            self.doc.change(r, c, r, c + len(self.find), [self.replace])
            self.next()
        elif chr == '!':
            while True:
                self.doc.change(r, c, r, c + len(self.find), [self.replace])
                if not self.next():
                    break
                r, c = self.view.moved
                
    def next(self):
        if self.view.moved:
            r, c = self.view.moved
        else:
            r, c = self.view.pos
        for r, c, line in self.doc.enumerate(r, c):
            match = self.regex.search(line)
            if match:
                c += match.start()
                self.view.move(r, c)
                return True

        self.esc()
        return False
                
    def esc(self):
        self.view.message = None
        self.doc.handler = None
        
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
        self.session.queue.put('draw colors')
                    
    def clean(self):
        for line in self.doc.color.colors:
            line[:] = line.translate(TRANSLATION)
