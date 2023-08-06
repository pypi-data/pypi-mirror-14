import os
import os.path as op

from spelltinkle.document import Document
from spelltinkle.text import TextDocument


class FileInputDocument(Document):
    def __init__(self, path, action='open'):
        Document.__init__(self)
        self.action = action
        self.name = '[{}]'.format(action)
        self.c = None
        self.dir = None
        self.filename = None
        self.allfiles = None
        self.path = None
        self.update(path)
                  
    def insert_character(self, chr):
        c = self.c
        p = self.path[:c] + chr + self.path[c:]
        self.c += 1
        self.update(p)
        
    def enter(self):
        self.session.docs.pop()
        if self.action == 'open':
            doc = TextDocument()
            doc.read(self.path, self.session.read())
            return doc
        else:
            self.session.docs[-1].set_filename(self.path)
            self.session.docs[-1].write()

    def esc(self):
        self.session.docs.pop()
    
    def bs(self):
        c = self.c
        if c:
            p = self.path[:c - 1] + self.path[c:]
            self.c -= 1
            self.update(p)
        
    def delete(self):
        c = self.c
        p = self.path[:c] + self.path[c + 1:]
        self.update(p)
        
    def tab(self):
        names = self.lines[:-1]
        if not names:
            return
            
        i0 = i = len(self.filename)
        while True:
            name0 = names[0][:i + 1]
            if len(name0) == i:
                break
            for f in names[1:]:
                if not f.startswith(name0):
                    break
            else:
                i += 1
                continue
            break
             
        self.c += i - i0
        self.filename = name0[:i]
        self.path += name0[i0:i]
        self.view.message = self.path + ' ', self.c
        self.update(self.path)
        
    def update(self, path):
        self.path = path
            
        if self.c is None:
            self.c = len(path)
            
        self.view.message = path + ' ', self.c

        if path == '..':
            dir = '..'
            self.filename = ''
        else:
            dir, self.filename = op.split(path)
        
        if dir != self.dir:
            self.allfiles = os.listdir(op.expanduser(dir) or '.')[:1000]
            self.dir = dir
            
        names = []
        for f in self.allfiles:
            if f.startswith(self.filename):
                if op.isdir(op.join(dir, f)):
                    f += '/'
                names.append(f)

        self.change(0, 0, len(self.lines) - 1, 0, names + [''])
        self.view.move(0, 0)
