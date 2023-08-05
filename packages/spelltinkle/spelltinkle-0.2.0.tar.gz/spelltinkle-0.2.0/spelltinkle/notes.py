import argparse
import os
import sqlite3
import textwrap

from spelltinkle.document import Document
from spelltinkle.input import Input


def str2min(s):
    return int(s[:-1]) * {'m': 1,
                          'h': 60,
                          'd': 8 * 60,
                          'w': 5 * 8 * 60,
                          'M': 22 * 8 * 60,
                          'y': 46 * 5 * 8 * 60}[s[-1]]

    
def min2str(m):
    for c, t in [('d', 8 * 60),
                 ('h', 60),
                 ('m', 1)]:
        n = m // t
        if n > 0:
            return str(n) + c
            
    
init_statements = """\
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    importance REAL,
    duration INTEGER,
    ctime REAL,
    deadline INTEGER,
    status TEXT,
    tags TEXT,
    description TEXT);
CREATE TABLE tags (
    tag TEXT,
    id INTEGER,
    FOREIGN KEY (id) REFERENCES tasks(id));
CREATE INDEX importance_index ON tasks(importance);
CREATE INDEX duration_index ON tasks(duration);
CREATE INDEX tag_index ON tags(tag)"""


def task(cur, row):
    if len(row) >= 8:
        return Task(row)
    return row
    
        
class Task:
    def __init__(self, row):
        (self.id, self.importance, self.duration, self.ctime,
         self.deadline, self.status, tags, self.description) = row[:8]
        self.tags = tags.split(',')
        
        
class Tasks(Document):
    taskpath = '/home/jensj/ownCloud/tasksnew.db'
    
    def __init__(self):
        Document.__init__(self)
        self.tags = []
        self.tag = ''
        new = not os.path.isfile(self.taskpath)
        self.con = sqlite3.connect(self.taskpath)
        if 0:
            self.renumber()
        if new:
            for statement in init_statements.split(';'):
                self.con.execute(statement)
            self.con.commit()
            
        if 1:
            self.con.row_factory = task
        if 0:
            path = '/home/jensj/ownCloud/tasksnew.db'
            con = sqlite3.connect(path)
            for statement in init_statements.split(';'):
                con.execute(statement)
                print(statement)
            con.commit()
            sql = 'SELECT * FROM tasks'
            cur = self.con.execute(sql)
            id = 1
            for row in cur.fetchall():
                print(row)
                con.execute(
                    'INSERT INTO tasks VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)',
                    (-row[1], row[2], 15.3, 0, 'pending', row[6], row[7]))
                con.commit()
                # cur2 = con.execute(
                #     'SELECT seq FROM sqlite_sequence WHERE name="tasks"')
                # id = 1#cur2.fetchone()[0]
                # con.commit()
                # print(id)
                for tag in row[6].split(','):
                    con.execute('INSERT INTO tags VALUES (?, ?)', (tag, id))
                con.commit()
                id += 1
                
    def set_session(self, session):
        Document.set_session(self, session)
        self.list()
        
    def insert_character(self, c):
        if c.isalnum():
            self.tag += c
        elif c == '+':
            n = int(self.tag or 1)
            self.move(n)
        elif c == '-':
            n = int(self.tag or 1)
            self.move(-n)
        
    def enter(self):
        if self.tag:
            self.toggle()
        else:
            if len(self.ids) == 0:
                return
            # Edit:
            task = self.get(self.id)
            txt = '{} {} {}'.format(','.join(task.tags),
                                    min2str(task.duration),
                                    task.description)
            self.handler = NewTask(self, txt, task.importance, edit=True)
            
    def move(self, d):
        self.tag = ''
        j = self.ids0.index(self.id)
        if d > 0:
            if j == 0:
                return
            if j <= d:
                importance = self.get(self.ids0[0]).importance
                importance = self.next_importance(importance)
            else:
                imp1 = self.get(self.ids0[j - d - 1]).importance
                imp2 = self.get(self.ids0[j - d]).importance
                importance = (imp1 + imp2) / 2
                assert imp1 > importance > imp2
        else:
            N = len(self.ids0)
            if j == N - 1:
                return
            if j >= N + d:
                importance = self.get(self.ids0[-1]).importance
                importance = self.prev_importance(importance)
            else:
                imp1 = self.get(self.ids0[j - d - 1]).importance
                imp2 = self.get(self.ids0[j - d]).importance
                importance = (imp1 + imp2) / 2
                assert imp1 > importance > imp2
            
        self.con.execute('UPDATE tasks SET importance = ? WHERE id = ?',
                         (importance, self.id))
        self.con.commit()
        self.list()
        
    def select(self, query, *args):
        return self.con.execute('SELECT ' + query, args).fetchall()
        
    def next_importance(self, importance):
        results = self.select('importance FROM tasks '
                              'WHERE importance > ? '
                              'AND status = "pending" '
                              'ORDER BY importance LIMIT 1',
                              importance)
        if results:
            i = results[0][0]
            newimportance = (importance + i) / 2
            assert importance < newimportance < i
        else:
            newimportance = importance + 1
        return newimportance
        
    def prev_importance(self, importance):
        results = self.select('importance FROM tasks '
                              'WHERE importance < ? '
                              'AND status = "pending" '
                              'ORDER BY importance DESC LIMIT 1',
                              importance)
        if results:
            i = results[0][0]
            newimportance = (importance + i) / 2
            assert importance > newimportance > i
        else:
            newimportance = importance - 1
        return newimportance
        
    def insert(self):
        if self.ids:
            task = self.get(self.id)
            importance = self.next_importance(task.importance)
            txt = ','.join(task.tags) + ' '
        else:
            txt = ''
            importance = 0.0
        self.handler = NewTask(self, txt, importance)
        
    def toggle(self):
        if self.tag in self.tags:
            self.tags.remove(self.tag)
        else:
            self.tags.append(self.tag)
        self.tag = ''
        self.list()
        
    def list(self, limit=1000):
        tables = ['tasks']
        where = ['tasks.status = "pending"']
        args = []
        for n, tag in enumerate(self.tags):
            tables.append('tags as t{}'.format(n))
            where.append('tasks.id = t{0}.id AND t{0}.tag = ?'.format(n))
            args.append(tag)
            
        if where:
            where = 'WHERE {} '.format(' AND '.join(where))
        else:
            where = ''
        sql = ('SELECT * FROM {} {}'
               'ORDER BY importance DESC '
               'LIMIT ?').format(', '.join(tables), where)
        args.append(limit)
        cur = self.con.execute(sql, args)
        
        common = None
        n = 0
        tasks = []
        for task in cur.fetchall():
            if common is None:
                common = set(task.tags)
            else:
                common &= set(task.tags)
            n = max(n, len(','.join(task.tags)))
            tasks.append(task)
        
        if common is None:
            common = set()
        s = ','.join(sorted(common))
        n = max(n - len(s) - 1, 4)
        indent = '{}|    |'.format(' ' * n)
        ncolumns = self.view.text.w - 4
        width = ncolumns - len(indent) - 1
        wrapper = textwrap.TextWrapper(width=width)
        if s:
            self.view.message = 'Common tags: ' + s
        fmt = '{:{}}|{:>4}|{}'
        lines = []
        self.ids = []
        self.ids0 = []
        for task in tasks:
            tags = ','.join(sorted(set(task.tags) - common))
            dlines = wrapper.wrap(task.description or '???')
            lines.append(fmt.format(tags, n,
                                    min2str(task.duration),
                                    dlines[0]))
            for line in dlines[1:]:
                lines.append(indent + line)
            self.ids += [task.id] * len(dlines)
            self.ids0.append(task.id)
        
        r = self.view.r
        lines.append('')
        self.change(0, 0, len(self.lines) - 1, 0, lines)
        self.view.move(r)
        self.changes = 42

    def get(self, id):
        return self.select('* FROM tasks WHERE id = ?', id)[0]
        
    def add(self, importance, duration, tags, description):
        ctime = 15.35
        self.con.execute(
            'INSERT INTO tasks VALUES (NULL, ?, ?, ?, 0, ?, ?, ?)',
            (importance, duration, ctime, 'pending', ','.join(tags),
             description))
        cur = self.con.execute(
            'SELECT seq FROM sqlite_sequence WHERE name="tasks"')
        id = cur.fetchone()[0]
        for tag in tags:
            self.con.execute('INSERT INTO tags VALUES (?, ?)', (tag, id))
        self.con.commit()
        return id

    def delete(self, status='done'):
        self.con.execute('UPDATE tasks SET status = ? WHERE id = ?',
                         (status, self.id))
        self.con.commit()
        self.list()
        
    def renumber(self):
        sql = 'SELECT id FROM tasks ORDER BY importance DESC'
        ids = [row[0] for row in self.con.execute(sql)]
        importance = len(ids)
        for id in ids:
            self.con.execute('UPDATE tasks SET importance = ? WHERE id = ?',
                             (importance, id))
            self.con.commit()
            importance -= 1
        
    @property
    def id(self):
        return self.ids[self.view.y]
        
        
class NewTask(Input):
    def __init__(self, doc, txt, importance, edit=False):
        self.doc = doc
        Input.__init__(self, txt)
        self.importance = importance
        self.edit = edit
        
    def update(self, string=None):
        Input.update(self, string)
        self.doc.view.message = self.string, self.c
        self.doc.view.update_info_line()

    def enter(self):
        try:
            tags, duration, description = self.string.split(' ', 2)
            duration = str2min(duration)
        except ValueError:
            return
        if self.edit:
            self.doc.delete('edited')
        id = self.doc.add(self.importance, duration, tags.split(','),
                          description)
        self.esc(id)
        
    def esc(self, id=None):
        self.doc.view.message = None
        self.doc.handler = None
        self.doc.list()
        # if id:
        #    try:
        #        r = self.doc.ids.index(id)
        #    except ValueError:
        #        return
        
            
def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='additional help',
                                       dest='cmd')
    add = subparsers.add_parser('add')
    add.add_argument('importance')
    add.add_argument('duration')
    add.add_argument('tags')
    add.add_argument('description', nargs='+')
    
    lst = subparsers.add_parser('list')
    lst.add_argument('tags')
    lst.add_argument('--limit', '-l', type=int, default=10)
    
    done = subparsers.add_parser('done')
    done.add_argument('id', type=int)
    
    args = parser.parse_args()
    tasks = Tasks()
    if args.cmd == 'add':
        importance = str2min(args.importance)
        duration = str2min(args.duration)
        tasks.add(importance, duration, args.tags.split(','),
                  ' '.join(args.description))
    elif args.cmd == 'list':
        tasks.list(args.tags.split(','), limit=args.limit)
    elif args.cmd == 'done':
        tasks.done(args.id)

    return
    import sys
    for line in sys.stdin:
        if line[0] != '*':
            t0 = 'work,' + line[:-1]
            continue
        else:
            x, d = line[1:].split(' ', 1)
            x = x.split(',')
            i, du = x[:2]
            if len(x) == 3:
                t = t0 + ',' + x[2]
            else:
                t = t0
            tags = set()
            for x in t.split(','):
                x = x.lower()
                if x[0] == '-':
                    tags.discard(x[1:])
                else:
                    tags.add(x)
        importance = str2min(i)
        duration = str2min(du)
        # print(importance, duration, list(tags), d.strip())
        tasks.add(importance, duration, list(tags), d.strip())
            
            
if __name__ == '__main__':
    main()
