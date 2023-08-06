import datetime as dt
import os
import signal
import time

from spelltinkle.color import NoColor
from spelltinkle.config import configure
from spelltinkle.document import Document
from spelltinkle.i18n import _
from spelltinkle.input import Input
from spelltinkle.text import TextDocument
from spelltinkle.utils import f


months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
          'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

DAY = dt.timedelta(days=1)
HOUR = dt.timedelta(hours=1)


def hm(s):
    return (int(x) for x in s.split(':'))
    
    
def weeknumber(t):
    t1 = dt.datetime(t.year + 1, 1, 1)
    n = t1.weekday()
    if 0 < n < 4 and t.month == 12 and t.day > 31 - n:
        return 1
    t1 = dt.datetime(t.year, 1, 1)
    n = t1.weekday()
    if n <= 3:
        return ((t - t1).days + n) // 7 + 1
    wn = ((t - t1).days + n) // 7
    if wn == 0:
        return weeknumber(t1 - DAY)
    return wn
    
    
def parse1(lines):
    for line in lines:
        words = line.strip().split()
        if not words:
            continue
        w = words.pop(0)
        if len(words) == 0:
            if w.isnumeric():
                year = int(w)
            else:
                month = months.index(w) + 1
            continue

        if '-' in w:
            day1, day2 = (int(day) for day in w.split('-'))
            t1 = dt.datetime(year, month, day1)
            if day2 < day1:
                month += 1
                if month == 13:
                    month = 1
                    year += 1
            t2 = dt.datetime(year, month, day2)

            t2 += DAY
        else:
            day = int(w)
            
            w = words[0]
            if w[0].isnumeric() and ':' in w:
                if '-' in w:
                    t1, t2 = (dt.datetime(year, month, day, *hm(t))
                              for t in w.split('-'))
                else:
                    t1 = dt.datetime(year, month, day, *hm(w))
                    t2 = t1 + HOUR
                words.pop(0)
            else:
                t1 = dt.datetime(year, month, day)
                t2 = t1 + DAY
            
        birthday = False
        w = words[0]
        if w[0] == '!':
            if w == '!':
                birthday = True
                repeat = 'y'
            else:
                repeat = w[1:]
            words.pop(0)
            w = words[0]
        else:
            repeat = False
        
        if w == '*':
            alarm = True
            words.pop(0)
        else:
            alarm = False
            
        yield t1, t2, birthday, repeat, ' '.join(words)
        

def parse2(lines):
    for t1, t2, birthday, repeat, description in parse1(lines):
        t = dt.datetime(t1.year, t1.month, t1.day) + DAY
        while t2 > t:
            yield t1, t, birthday, repeat, description
            t1 = t
            t += DAY
        yield t1, t2, birthday, repeat, description
            
    
def parse3(lines, start, stop):
    for t1, t2, birthday, repeat, description in parse2(lines):
        if repeat == 'y':
            t = dt.datetime(start.year - 1,
                            t1.month, t1.day, t1.hour, t1.minute)
            while t - t1 + t2 < start:
                t = dt.datetime(t.year + 1, t.month, t.day, t.hour, t.minute)
            y = ''
            while t < stop:
                if birthday:
                    y = t.year - t1.year
                    if y == 1:
                        y = ' ({} {})'.format(y, _('year'))
                    elif y > 1:
                        y = ' ({} {})'.format(y, _('years'))
                yield t, t - t1 + t2, birthday, repeat, description + y
                t = dt.datetime(t.year + 1, t.month, t.day, t.hour, t.minute)
        elif repeat == 'md':
            wd = t1.weekday()
            n = (t1.day - 1) // 7
            t = dt.datetime(start.year, start.month, 1, t1.hour, t1.minute)
            while True:
                day = (wd - t.weekday() + 7) % 7 + 1 + n * 7
                t = dt.datetime(t.year, t.month, day, t.hour, t.minute)
                if t - t1 + t2 >= start:  # XXX >= or > ????
                    if t >= stop:
                        break
                    yield t, t - t1 + t2, False, repeat, description
                year = t.year
                month = t.month + 1
                if month == 13:
                    month = 1
                    year += 1
                t = dt.datetime(year, month, 1, t.hour, t.minute)
        else:
            if t2 > start and t1 < stop:
                yield t1, t2, birthday, repeat, description
            
                
class CalenderDocument(Document):
    def __init__(self):
        Document.__init__(self)
        self.conf = configure()
        self.color = NoColor()
        
    def set_session(self, session):
        Document.set_session(self, session)
        self.list()
        self.changes = 42
        
    def list(self):
        begin = dt.date.today()
        begin = dt.datetime(begin.year, begin.month, begin.day)
        end = begin + 500 * DAY
        with open(self.conf.calender_file) as fd:
            events = sorted(parse3(fd, begin, end))
        lines = []
        day = begin
        for t1, t2, birthday, repeat, description in events:
            day1 = dt.datetime(t1.year, t1.month, t1.day)
            while day < day1:
                lines.append((day, day, ''))
                day += DAY
            lines.append((t1, t2, description))
            day += DAY
        
        lines2 = []
        self.color.colors = colors = []
        nweekdayprev = -1
        for t1, t2, description in lines:
            nweekday = t1.weekday()
            if nweekday == nweekdayprev:
                weekday = '   '
            else:
                nweekdayprev = nweekday
                if t1.day == 1:
                    lines2.append('================ {} {}:'
                                  .format(_(months[t1.month - 1]).title(),
                                          t1.year))
                    colors.append(bytearray([2] * len(lines2[-1])))
                if nweekday == 0:
                    lines2.append('----- {} {}:'.format(_('week'),
                                                        weeknumber(t1)))
                    colors.append(bytearray([3] * len(lines2[-1])))
                weekday = _(days[nweekday]).title()
                    
            if description:
                p1 = t1.hour + t1.minute / 60
                p2 = p1 + (t2 - t1).total_seconds() / 3600
                i1 = int(p1 + 0.49)
                i2 = int(p2 + 0.49)
                if i1 == i2:
                    bar = '-' * i1 + '|' + (24 - i1) * '-'
                else:
                    bar = ('-' * i1 + '|' + (i2 - i1 - 1) * '=' + '|' +
                           (24 - i2) * '-')
                line = '{}{:02d} {} {:2}:{:02} {}'.format(
                    weekday, t1.day, bar, t1.hour, t1.minute, description)
                colors.append(bytearray([0, 0, 0, 0, 0, 0] + [4] * 26 +
                                        [0] * (7 + len(description))))
            else:
                line = '{}{:02d}'.format(weekday, t1.day)
                colors.append(bytearray(len(line)))
            lines2.append(line)
            
        self.change(0, 0, len(self.lines) - 1, 0, lines2)
        self.view.move(0, 0)

    def enter(self):
        for i, doc in enumerate(self.session.docs):
            if doc.filename == self.conf.calender_file:
                self.session.docs.append(self.session.docs.pop(i))
                return
        doc = TextDocument()
        doc.read(self.conf.calender_file, self.session.read())
        return doc
        
        
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
