import os
import sys
import shutil
import cProfile
from logging import debug

import spelltinkle.test.tests as tests
from spelltinkle.exceptions import StopSession
from spelltinkle.run import run
from spelltinkle.session import Session
from spelltinkle.utils import f


class Input:
    session = None

    def __init__(self, test):
        self.stream = self.characters(test)
        self.queue = []
        
    def get(self):
        if self.queue:
            return self.queue.pop(0)
        c = next(self.stream)
        print(f^'<{c}>', end='')
        return c
    
    def put(self, c):
        self.queue.append(c)
        
    def characters(self, test):
        for s in test(self.session):
            while s:
                s0 = s
                if s[:2] == '^^':
                    yield '^'
                    s = s[2:]
                if s[0] == '^':
                    yield s[:2]
                    s = s[2:]
                elif s[:2] == '<<':
                    yield '<'
                    s = s[2:]
                elif s[0] == '<':
                    key, s = s[1:].split('>', 1)
                    yield key.replace('-', '_')
                elif s[0] == '\n':
                    s = s[1:]
                else:
                    yield s[0]
                    s = s[1:]
                debug(s0[:len(s0) - len(s)])
                

def test(names):
    if os.path.isdir('spelltinkle-self-test'):
        shutil.rmtree('spelltinkle-self-test')
    os.mkdir('spelltinkle-self-test')
    os.chdir('spelltinkle-self-test')
    prof = cProfile.Profile()
    prof.enable()
    if not names:
        names = sorted(name for name, f in tests.__dict__.items()
                       if callable(f))
    for name in names:
        print(name)
        t = getattr(tests, name)
        scr = Screen(10, 60, Input(t))
        filenames = getattr(t, 'args', [])
        files = getattr(t, 'files', [])
        for name, txt in files:
            if '/' in name:
                dir = name.rsplit('/', 1)[0]
                os.makedirs(dir)
            with open(name, 'w') as fd:
                fd.write(txt)
        s = Session(filenames, scr, test=True)
        scr.stream.session = s
        error = s.run()
        print()
        if error:
            break
    prof.disable()
    prof.dump_stats('test.profile')

    
class Screen:
    def __init__(self, h, w, stream=None):
        self.h = h
        self.w = w
        self.stream = stream
        
    def subwin(self, a, b, c, d):
        return Screen(a, b)
        
    def erase(self):
        pass
        
    def refresh(self):
        pass
        
    def move(self, a, b):
        pass
        
    def write(self, line, colors):
        pass
    
    def input(self):
        return self.stream.get()
