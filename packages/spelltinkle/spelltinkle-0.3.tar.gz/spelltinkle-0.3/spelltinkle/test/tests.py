import os
import time


def writeas(session):
    yield '^d^k^k12345<enter><home><home>^k^p^p^a^k^p^p^a^k^p^p^p^p.<enter>'
    yield '# hello<enter>'
    yield 'A' * 25 * 1
    yield '<up>^a^b^b<down>^c<page-up>^p'
    yield 'if 1:<enter>a = 1<enter>b = a'
    yield '<enter>^x^w<bs><bs><bs><bs>writeas.txt<enter>^q'
writeas.args = ['asdf']


def open2(session):
    with open('open2.py', 'w') as fd:
        fd.write('# hello\na = 42\n')
    yield '<home><home>^shello^s <home>^b^b<up>^d'
    yield '^sA<right>^k^x^w'
    yield '<bs>' * len('open2.py')
    yield 'open2b.py<enter>'
    yield '^oopen2.py<enter>^v2^q^q'
open2.args = ['open2.py']


def mouse(session):
    session.scr.position = (3, 1)
    yield 'a.bc<enter><mouse1-clicked>^d'
    assert session.docs[-1].lines[0] == 'abc'
    session.scr.position = (3, 4)
    yield '<mouse1-clicked>'
    assert session.docs[-1].view.pos == (1, 0)
    yield '1<enter>2<enter><up><up><up><end><down>'
    assert session.docs[-1].view.pos == (1, 1)
    yield '^q'


def noend(session):
    with open('noend.py', 'w') as fd:
        fd.write('a = {\n}')
    yield '^onoend.py<enter>'
    assert session.docs[-1].lines[1] == '}'
    yield '^q^q'

    
def complete_import(session):
    yield 'from spelltink<tab>'
    assert session.docs[-1].lines[0].endswith('spelltinkle')
    yield '.ru<tab>'
    assert session.docs[-1].lines[0].endswith('spelltinkle.run')
    yield ' import ru<tab>'
    assert session.docs[-1].lines[0].endswith('run')
    yield '^q'


def replace(session):
    with open('Replace.py', 'w') as fd:
        fd.write('a = {\n}')
    yield '^oRepl<tab><enter><end><end><enter>aa<enter>aaa<enter>aaaa<enter>'
    yield '<home><home>^fa<right>12<enter>ynyyynn!<down>.'
    yield '<home><home>^f12<right>A<enter>!^w'
    txt = '|'.join(session.docs[-1].lines)
    assert txt == 'A = {|}|aA|AAa|aAAA|.', txt
    yield '^q^q'

    
def openline(session):
    assert session.docs[-1].view.pos == (1, 0), session.docs[-1].view.pos
    yield '^q'
openline.args = ['openline.txt:2']
openline.files = [('openline.txt', '1\n2\n')]


def test7(session):
    yield '({[()]})<home>'
    c = session.docs[-1].color.colors[0]
    assert c[0] // 28 == 3, (c, len(c))
    yield '<end>'
    assert c[0] // 28 == 3, c
    yield '^q'
del test7


def test8(session):
    yield '1<enter>2<enter>3<enter>'
    yield '<home><home>^k^k<down>^x^k^k<up>^y<bs>^a<bs>'
    assert session.docs[-1].lines[0] == '132'
    yield '^q'

    
def test9(session):
    yield 'abc<enter>'
    yield '123<enter>'
    session.scr.position = (4, 1)
    yield '<mouse1-clicked>'
    session.scr.position = (5, 2)
    yield '<mouse1-released>'
    time.sleep(0.5)
    session.scr.position = (2, 1)
    yield '<mouse2-clicked>'
    assert ''.join(session.doc.lines) == 'c123abc123'
    yield '^q'

    
def test10(session):
    yield 'AAA^rA^r^r'
    pos = session.docs[0].view.pos
    assert pos == (0, 1), pos
    yield '^q'

    
def test11(session):
    yield '^vt^n'
    print(session.docs[-1].lines[:7])
    print(session.docs[-1].view.lines[:7])
    yield '^q^q'

    
def todo(session):
    from spelltinkle.notes import Tasks
    path = '/tmp/test-tasks.db'
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
    Tasks.taskpath = path
    yield '^t<enter><insert>tag 1h bla<enter>'
    print(session.docs[-1].lines, session.docs[-1].view.y)
    yield '<enter>bla<enter>'
    yield '<insert>10m hmm<enter>'
    print(session.docs[-1].lines, session.docs[-1].view.y)
    yield '+'
    print(session.docs[-1].lines)
    yield '<delete>'
    print(session.docs[-1].lines, session.docs[-1].view.y)
    yield '^q'


def jedi(session):
    yield 'abc = 8<enter>'
    yield 'ab7 = 8<enter>'
    yield 'a<F8><F8><enter>'
    print(session.docs[-1].lines)
    yield '^q'

    
def write(session):
    yield 'abc'
    with open('abc.123', 'w') as fd:
        fd.write('123')
    yield '^wabc.123<enter><enter>abc.1234<enter>...^w'
    yield '^q'
    
    
def fileinput(session):
    yield '^ohmm<tab><tab><tab><enter>'
    assert session.docs[1].lines[0] == 'hmm'
    yield '^q^q'
fileinput.files = [('hmmm/grrr/abc.txt', 'hmm')]


def rectangle_insert(session):
    yield 'aaa<enter>'
    yield 'a<enter>'
    yield 'aa<enter>'
    yield 'aaa<enter>'
    yield '12^a^k<up><right><ctrl_up><up><up><right>^b^y'
    assert '+'.join(session.docs[0].lines) == 'a12a+a+a12+a12a+'
    yield '^q'

    
def mark_and_copy(session):
    yield 'a1234<left>^u^y'
    assert session.docs[0].lines[0] == 'a1234a1234'
    yield '^q'
