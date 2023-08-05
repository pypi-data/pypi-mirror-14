import os.path as op


class Configuration:
    pass
    

def configure():
    conf = Configuration()
    filename = op.expanduser('~/.spelltinkle/config.py')
    if op.isfile(filename):
        dct = {}
        with open(filename) as fd:
            exec(fd.read(), dct)
        if 'user_files' in dct:
            conf.user_files = {shortcut: op.expanduser(name)
                               for shortcut, name in dct['user_files'].items()}
    return conf
