import re
import threading

from spelltinkle.input import Input
from spelltinkle.search import TRANSLATION, make_regular_expression, NHC

        
class Replace(Input):
    def __init__(self, doc):
        self.find = None
        self.doc = doc
        self.view = doc.view
        Input.__init__(self)
        self.regex = None
        self.replace = None
        self.paint_thread = None
        self.update('')
        
    def update(self, string=None):
        Input.update(self, string)
        if self.find is None:
            text = 'Find:' + self.string
        elif self.replace is None:
            text = 'Replace:' + self.string
        else:
            text = 'Replace?  yes, no or all!'
        self.view.message = text
        self.view.update_info_line()
        
    def enter(self):
        if self.find is None:
            self.find = self.string
            self.regex = re.compile(re.escape(self.find))
            self.c = 0
            self.update('')
            return
        
        if self.replace is None:
            self.replace = self.string
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
