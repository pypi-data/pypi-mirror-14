import datetime
import os
import signal
import time

from spelltinkle.document import Document
from spelltinkle.input import Input

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
          'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

oneday = datetime.timedelta(days=1)


class CalenderDocument(Document):
    def __init__(self):
        Document.__init__(self)
    
    def set_session(self, session):
        Document.set_session(self, session)
        self.list()
        self.changes = 42
        
    def enter(self, new=False):
        i, event = self.days[self.view.r][:2]
        self.handler = NewEvent(self, self.begin + i * oneday, event, new)

    def insert(self):
        self.enter(new=True)
        
    def list(self):
        self.begin = datetime.datetime.combine(datetime.date.today(),
                                               datetime.time())
        end = self.begin + 500 * oneday
        c = Calender()
        c.read(self.begin, end)
        self.days = c.html()
        self.change(0, 0, len(self.lines) - 1, 0,
                    [line for i, e, line in self.days])
        self.view.move(0, 0)

    def add(self):
        s = args.time + ' ' + ' '.join(args.text)
        event = str2event(s, datetime.datetime.now())
        if args.repeat:
            event.repeat = args.repeat
        if args.alarm:
            2 / 0
        c = Calender()
        c.read(repeat=False)
        c.events.append(event)
        c.write()
        
        
class NewEvent(Input):
    def __init__(self, doc, day, event, new):
        self.doc = doc
        txt = '...'
        Input.__init__(self, txt)
        
    def update(self, string=None):
        Input.update(self, string)
        self.doc.view.message = self.string, self.c
        self.doc.view.update_info_line()

    def enter(self):
        self.esc()
        
    def esc(self):
        self.doc.view.message = None
        self.doc.handler = None
        self.doc.list()
        self.doc.view.move(self.doc.ids.index(id))
        

class Event:
    def __init__(self, start, stop, alarm, repeat, text):
        self.start = start
        self.stop = stop
        self.alarm = alarm
        self.repeat = repeat
        self.text = text

    def write(self, day, html=False):
        t1 = max(self.start, day)
        t2 = min(self.stop, day + oneday)
        n = int(round(t1.hour + t1.minute / 60))
        dn = max(int(round((t2 - t1).total_seconds() / 3600)), 1)
        if not html:
            fmt = '\x1b[48;5;236m{}\x1b[48;5;238m{}\x1b[48;5;236m{}\x1b[49m'
            bar = fmt.format(' ' * n, '.' * dn, ' ' * (24 - n - dn))
            print('{} {:02d}:{:02d} {}'.format(
                  bar, t1.hour, t1.minute, self.text))
            return
        fmt = '{}{}{}'
        bar = fmt.format('.' * n, '#' * dn, '.' * (24 - n - dn))
        return '{} {:02d}:{:02d} {}'.format(
            bar, t1.hour, t1.minute, self.text)
            
    def __str__(self):
        t1 = self.start
        duration = dt2str(self.stop - t1)
        fmt = '{}-{}-{:02d}-{:02d}:{:02d}+{}'
        s = fmt.format(t1.year,
                       months[t1.month - 1],
                       t1.day, t1.hour, t1.minute,
                       duration)
        if self.alarm:
            s += 'A' + dt2str(t1 - self.alarm)
        if self.repeat:
            s += 'R' + self.repeat
        return '{:27} {}'.format(s, self.text)
        
    def get_repeats(self):
        if self.repeat is None:
            return
        event = self
        while True:
            if self.repeat == 'w':
                dt = 7 * oneday
            elif self.repeat == 'y':
                start = event.start
                dt = start.replace(year=start.year + 1) - start
            event = Event(event.start + dt, event.stop + dt,
                          event.alarm and event.alarm + dt,
                          None, event.text)
            yield event
            
        
def str2min(s):
    return int(s[:-1]) * {'h': 60, 'm': 1, 'd': 24 * 60}[s[-1]]

    
def dt2str(dt):
    if dt.days:
        return str(dt.days) + 'd'
    m = dt.seconds // 60
    if m % 60 == 0:
        return str(m // 60) + 'h'
    return str(m) + 'm'
    
                
class Calender:
    def __init__(self):
        self.events = []
        
    def read(self, begin=datetime.datetime.min, end=datetime.datetime.max,
             repeat=True):
        self.begin = begin
        self.end = end
        last = begin
        for line in open('/home/jensj/ownCloud/calender.txt'):
            event = str2event(line.rstrip(), last)
            last = event.start
            ok = event.stop > begin and event.start < end
            if ok or repeat and event.repeat:
                if ok:
                    self.events.append(event)
                if repeat:
                    for e in event.get_repeats():
                        if e.stop <= begin:
                            continue
                        if e.start >= end:
                            break
                        self.events.append(e)
        self.sort()
        
    def sort(self):
        self.events.sort(key=lambda e: e.start)

    def alarm(self, begin=datetime.datetime.min, end=datetime.datetime.max):
        self.begin = begin
        self.end = end
        last = begin
        for line in open('/home/jensj/ownCloud/calender.txt'):
            event = str2event(line.rstrip(), last)
            last = event.start
            ok = event.alarm and begin < event.alarm <= end
            if ok or event.repeat and event.alarm:
                if ok:
                    self.events.append(event)
                else:
                    for e in event.get_repeats():
                        if begin >= e.alarm:
                            continue
                        if e.alarm > end:
                            break
                        self.events.append(e)
        self.sort()
        
    def write(self):
        self.sort()
        with open('/home/jensj/ownCloud/calender.txt', 'w') as fd:
            for event in self.events:
                print(event, file=fd)
                
    def summary(self, html):
        if html:
            return self.html()
        day = self.begin
        events = list(self.events)
        n = 0
        while day < self.end:
            print('{}{:02d} '.format(days[day.weekday()].title(), day.day),
                  end='')
            day1 = day + oneday
            done = []
            first = True
            for n, e in enumerate(events):
                if e.stop > day and e.start < day1:
                    if not first:
                        print('      ', end='')
                    else:
                        first = False
                    e.write(day)
                if e.stop < day1:
                    done.append(n)
            if first:
                print('\x1b[48;5;236m{}\x1b[49m'.format(' ' * 24), end='')
                print()
            if day.weekday() == 6:
                print('------------------------------')
            for n in reversed(done):
                del events[n]
            day = day1

    def html(self):
        lines = []
        
        day = self.begin
        events = list(self.events)
        i = 0
        while day < self.end:
            line = '{}{:02d} '.format(days[day.weekday()].title(), day.day)
            day1 = day + oneday
            done = []
            first = True
            for n, e in enumerate(events):
                if e.stop > day and e.start < day1:
                    if not first:
                        line = '      '
                    else:
                        first = False
                    line += e.write(day, True)
                lines.append((i, e, line))
                if e.stop < day1:
                    done.append(n)
            if first:
                lines.append((i, None, '........................'))
            for n in reversed(done):
                del events[n]
            day = day1
        return lines

        
def alarm():
    path = '/home/jensj/.spelltinkle/calender-alarm.pid'
    if os.path.isfile(path):
        with open(path) as fd:
            pid = int(fd.read())
        try:
            os.kill(pid, signal.SIGUSR1)
        except OSError:
            pass
        else:
            return
            
    pid = os.getpid()
    print('PID:', pid)
    signal.signal(signal.SIGUSR1, signal.SIG_IGN)
    with open(path, 'w') as fd:
        print(pid, file=fd)

    p = '/home/jensj/ownCloud/calender.txt'
    last = None
    while True:
        path = '/home/jensj/.spelltinkle/calender-last-alarm.txt'
        if last is None:
            with open(path) as fd:
                last = datetime.datetime(*(int(x)
                                           for x in fd.read().split()))
        
        mtime = os.stat(p).st_mtime
        c = Calender()
        end = last + oneday
        c.alarm(last, end)
        for event in c.events:
            t = event.alarm
            while t > datetime.datetime.now():
                time.sleep(300)
                if os.stat(p).st_mtime > mtime:
                    last = None
                    break
            else:
                mail(event)
                
                with open(path, 'w') as fd:
                    print(t.year, t.month, t.day, t.hour, t.minute,
                          file=fd, flush=True)
                continue
            break
        else:
            last = end
            while last > datetime.datetime.now():
                time.sleep(300)
                if os.stat(p).st_mtime > mtime:
                    last = None
                    break
        
                
def mail(event):
    import smtplib
    from email.mime.text import MIMEText
    subject = '{}: {}'.format(event.start, event.text)
    msg = MIMEText('bla')
    msg['Subject'] = subject
    to = 'jensj@fysik.dtu.dk'
    msg['From'] = to
    msg['To'] = to
    s = smtplib.SMTP('mail.fysik.dtu.dk')
    s.sendmail(msg['From'], [to], msg.as_string())
    s.quit()
    

def check_mail():
    import imaplib
    from email.header import decode_header
    path = '/home/jensj/.spelltinkle/calender-email-config.txt'
    with open(path) as fd:
        passwd = fd.read().strip()
    with open('/home/jensj/.spelltinkle/calender-email-seen.txt') as fd:
        done = set(line.strip() for line in fd.readlines())
    M = imaplib.IMAP4_SSL('mail.dtu.dk')
    M.login('jjmo', passwd)
    N = int(M.select()[1][0])
    a, b = M.fetch('1:{}'.format(N), '(BODY[HEADER.FIELDS (SUBJECT)])')
    newdone = set()
    for c in b:
        if isinstance(c, tuple):
            txt = ''.join(s if isinstance(s, str) else s.decode(e or 'ascii')
                          for s, e in decode_header(c[1].decode()))
            txt = txt.strip().split('Subject:', 1)[1].strip()
            if txt.startswith('Cal: '):
                txt = txt[5:]
                if txt not in done:
                    event = str2event(txt, datetime.datetime.now())
                    c = Calender()
                    c.read(repeat=False)
                    c.events.append(event)
                    c.write()
                newdone.add(txt)
    if newdone != done:
        with open('/home/jensj/.spelltinkle/calender-email-seen.txt',
                  'w') as fd:
            for line in newdone:
                print(line, file=fd)
            
    M.close()
    M.logout()


def str2event(s, last):
    s, text = s.split(' ', 1)
    text = text.strip()
    duration = None
    repeat = None
    alarm = None
    if 'R' in s:
        s, repeat = s.split('R')
    if 'A' in s:
        s, alarm = s.split('A')
    if '+' in s:
        s, duration = s.split('+')
    w = s.split('-')
    if ':' in w[-1]:
        hour, minute = (int(x) for x in w.pop().split(':'))
        duration = duration or '1h'
    else:
        hour = 0
        minute = 0
        duration = duration or '1d'
    day = w.pop()
    if day[:3] in days:
        assert len(w) == 0
        weekday = days.index(day)
        t = last + oneday
        while t.weekday() != weekday:
            t += oneday
        day = t.day
        month = t.month
        year = t.year
    else:
        day = int(day)
        if w:
            month = w.pop()
            if month.isdigit():
                month = int(month)
            else:
                month = months.index(month) + 1
            if w:
                assert len(w) == 1
                year = int(w[0])
            else:
                year = last.year
        else:
            month = last.month
            year = last.year
    
    start = datetime.datetime(year, month, day, hour, minute)
    stop = start + datetime.timedelta(minutes=str2min(duration))
    if alarm:
        alarm = start - datetime.timedelta(minutes=str2min(alarm))
    return Event(start, stop, alarm, repeat, text)
