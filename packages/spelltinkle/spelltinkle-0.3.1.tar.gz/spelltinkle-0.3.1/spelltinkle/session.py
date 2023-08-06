import collections
import inspect
import os
import signal
from time import time

from spelltinkle.text import TextDocument
from spelltinkle.exceptions import StopSession
from spelltinkle.keys import keynames, doubles, repeat, again


class Session:
    def __init__(self, filenames, scr, test=False):
        self.scr = scr
        self.test = test
        positions = self.read()
        if filenames:
            self.docs = []
            for filename in filenames:
                doc = TextDocument(self)
                doc.read(filename, positions)
                self.docs.append(doc)
        else:
            self.docs = [TextDocument(self)]

        self.lastkey = None
        self.lasttime = 0.0
        self.memory = ['']
        self.chars = ''
        self.lastsearchstring = ''
        self.failed = False
        
    @property
    def doc(self):
        return self.docs[-1]
        
    def run(self):
        import asyncio
        self.loop = asyncio.new_event_loop()
        self.loop.set_exception_handler(self.error)
        # self.loop.add_signal_handler(signal.SIGWINCH, self.resize)
        self.update()
            
        if self.test:
            self.loop.call_soon(self.inputtest)
        else:
            self.loop.add_reader(0, self.input1)
            
        self.loop.run_forever()
        self.loop.close()
        return self.failed
        
    def error(self, loop, context):
        import traceback
        txt = repr(context) + '\n' + traceback.format_exc()
        if self.test:
            print('\n', txt)
            self.loop.stop()
            self.failed = True
        else:
            for doc in self.docs:
                if doc.filename:
                    old = doc.filename
                    import tempfile
                    fd, name = tempfile.mkstemp()
                    os.close(fd)
                    doc.filename = name
                    doc.write()
                    doc.filename = old
            for doc in self.docs:
                if doc.name == '[error]':
                    self.docs.remove(doc)
                    break
            else:
                doc = TextDocument()
                doc.name = '[error]'
                doc.set_session(self)
            self.docs.append(doc)
            doc.change(0, 0, 0, 0, txt.splitlines())
            self.update()
        
    def resize(self):
        self.scr.resize()
        for doc in self.docs:
            doc.changes = 42
        self.update()
        
    def update(self):
        for doc in self.docs[-1:]:
            doc.view.update(self)
            if doc.changes:
                doc.color.run(self.loop)
            doc.changes = None

    def draw_colors(self):
        doc = self.docs[-1]
        doc.changes = 42
        doc.view.update(self)
        doc.changes = None

    def inputtest(self):
        self.input1()
        if self.loop.is_running():
            self.loop.call_soon(self.inputtest)

    def input1(self, key=None):
        if key is None:
            key = self.scr.input()

        if isinstance(key, list):
            for k in key:
                self.input1(k)
            return
        
        if key is None:
            return  # undefined key
            
        if key == 'resize':
            self.resize()
            return
            
        doc = self.docs[-1]
        handler = doc.handler or doc

        if len(key) == 1:
            self.chars += key
            newdoc = handler.insert_character(key)
        else:
            if key in doubles:
                key2 = self.scr.input()
                key = doubles[key].get(key2)
                if key is None:
                    return
            else:
                key = keynames.get(key, key)
                if key is None:
                    return
                if key[0] == '^':
                    return
            if isinstance(key, list):
                for k in key:
                    self.input1(k)
                return
            if key in again and key == self.lastkey:
                key += '_again'
            elif (key in repeat and key == self.lastkey and
                  time() < self.lasttime + 0.3):
                key += key
            method = getattr(handler, key, None)
            if method is None:
                if hasattr(handler, 'unknown'):
                    newdoc = handler.unknown(key)
                else:
                    newdoc = None
            else:
                if inspect.isgeneratorfunction(method):
                    gen = method()
                    newdoc = next(gen, None)
                    if doc.handler:
                        doc.handler.continuation = gen
                else:
                    newdoc = method()
                
            if key.endswith('_again'):
                key = key[:-6]

        if newdoc:
            newdoc.set_session(self)
            newdoc.changes = 42
            self.docs.append(newdoc)
            
        self.lastkey = key
        self.lasttime = time()
        if len(key) > 1:
            self.chars = ''
        self.update()

    def read(self):
        dct = collections.OrderedDict()
        path = os.path.expanduser('~/.spelltinkle/session.txt')
        if os.path.isfile(path):
            with open(path) as fd:
                for line in fd:
                    name, r, c = line.rsplit(maxsplit=2)
                    dct[name] = int(r), int(c)
        return dct

    def save(self):
        dct = self.read()
        for doc in self.docs:
            if doc.filename is not None:
                dct[os.path.abspath(doc.filename)] = doc.view.pos
        with open(os.path.expanduser('~/.spelltinkle/session.txt'), 'w') as fd:
            for name, (r, c) in dct.items():
                print(name, r, c, file=fd)
