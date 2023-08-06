import re
import sys

regex = re.compile(r'\{.*?\}')


class F:
    def __xor__(self, arg):
        context = sys._getframe(1).f_locals
        parts = []
        for match in regex.finditer(arg):
            a, b = match.span()
            x = arg[a + 1:b - 1]
            if x[0] == '{':
                continue
            if ':' in x:
                x, fmt = x.split(':')
            else:
                fmt = ''
            s = format(eval(x, context), fmt)
            parts.append((a, b, s))
        for a, b, s in reversed(parts):
            arg = arg[:a] + s + arg[b:]
        return arg


f = F()


def untabify(line):
    if '\t' not in line:
        return line
    N = len(line)
    n = 0
    while n < N:
        if line[n] == '\t':
            m = 8 - n % 8
            line = line[:n] + ' ' * m + line[n + 1:]
            n += m
            N += m - 1
        else:
            n += 1
    return line


def isempty(line):
    return line == ' ' * len(line)

# re.match('(.*\S)(?= *)|( +)', line).group()


def tolines(fd):
    lines = []
    line = '\n'
    for n, line in enumerate(fd):
        line = untabify(line)
        for a in line[:-1]:
            assert ord(a) > 31, (line, n)
        if not isempty(line[:-1]):
            line = line[:-1].rstrip() + line[-1]
        lines.append(line[:-1])
    if line[-1] == '\n':
        lines.append('')
    else:
        lines[-1] = line
    return lines

    
def findword(line, c):
    while line[c - 1].isalnum():
        c -= 1
    return c
