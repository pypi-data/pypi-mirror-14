from spelltinkle.keys import keynames, doubles
from spelltinkle.document import Document


x = """
analysis
calender
tasks
p3 setup.py sdist (register) upload --show-response  # fix .pypirc first!
go to point before jump
go to next problem marker
spell check: ispell -a
swap two chars
check state of file every two seconds when active?

Fast and simple editor based on Python and Pygments.

XKCD: automation 1319

   ------
  | SPEL |
  | LTIN |
  | KLE  |
   ------

    ##### ##### ##### #
    #     #   # #     #
    ##### ##### ####  #
        # #     #     #
    ##### #     ##### #####
    
    #     ##### ##### #   #
    #       #     #   ##  #
    #       #     #   # # #
    #       #     #   #  ##
    #####   #   ##### #   #
    
    #   # #     #####
    #  #  #     #
    ###   #     ####
    # #   #     #
    #  #  ##### #####

    
     ___________
    |           |
    |  Hello    |
    |           |
    |___________|
    /S/P/E/L/L/ /
   /T/I/N/K/L/E/
  /___________/
  
        S
        P
        E
T I N K L E
        L

C-v t todo
C-v c calender
C-v e email (pymailgui)
C-v a analysis
C-v i irc

([[](()))
        ^: ]?

pep8 not installed?

Color names: GOOD, BAD, OK, IMPORTANT, IRRELEVANT, ...

email: filter: check spamfilter emails

C-p/C-n: up/down 1 line instead of one screen-line

http://stackoverflow.com/questions/2230037/how-to-fetch-an-email-body-using-imaplib-in-python
http://stackoverflow.com/questions/122267/imap-how-to-move-a-message-from-one-folder-to-another
http://stackoverflow.com/questions/12490648/imap-fetch-subject


ReST: section folding and jumping


spelltris?

autosave to /tmp after some time
$spelltinkle dir/ -> open fileinput

pkgutil, sys.modules

open-current-session-in-new-window-and-stop-the-old-one()

only one file-list at the time

replace+color
no indent after return
run tests
replace marked area by abc and add line before with abc = <marked-area>


Put help for opening files on the filelist page

When selcting area with mouse use scrollbar to scroll up or down

session.py: result=actions.method(doc);isgenerator(result)?
(for questions and other input)

remove tabs when reading (or replace with 4 tabs that display as spaces?)
smooth scrolling when jumping?
b block: b:begin, r:rectangle, l:lines
f replace,x:regex
g goto 123,()[]{},x:inner
h help,x:search in help
i-(tab) x:insert file or !shell
j- x:join
k kill,x:backwards
l delete line
m- x:makro
n
o open file or !shell or >>> python
q quit,x:ask
r reverse find,x:word under cursor
s find
t
y mark: wl()[]{},x:inner
z delete wl()[]{},x:inner

How about ^Z?

^#12 or ^1^2?

Jump to marked point? Put position on stack

reST mode

crash: report to launchpad

<c-1><c-2>: repeat 12 times
scroll:up, down,center,top, bottom
big movements

look at to vim plugins: svn,snippets,easymove
complete

scripting: abc<enter><up><end>


Use number columns to show stuff: last changed line(s)


write docs on errors and write debug info

python3 -m spelltinkle

spt --beginner --verbose --read-only --black-and-white

"""


class HelpDocument(Document):
    def __init__(self):
        Document.__init__(self)
        self.name = '[help]'
        lines = []
        for c in sorted(keynames):
            k = keynames[c]
            if not isinstance(k, str):
                k = '+'.join(k)
            lines.append('  {}: {}'.format(c, k))
        for c1 in doubles:
            for c2, k in doubles[c1].items():
                if not isinstance(k, str):
                    k = '+'.join(k)
                lines.append('{}{:2}: {}'.format(c1, c2, k))
        lines += x.split('\n')
        self.change(0, 0, 0, 0, lines)