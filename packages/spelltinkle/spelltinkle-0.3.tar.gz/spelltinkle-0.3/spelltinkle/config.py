import os.path as op


class Configuration:
    initialized = False
    pass
    
conf = Configuration()


def configure():
    if conf.initialized:
        return conf
    filename = op.expanduser('~/.spelltinkle/config.py')
    if op.isfile(filename):
        dct = {}
        with open(filename) as fd:
            exec(fd.read(), dct)
        if 'user_files' in dct:
            conf.user_files = {shortcut: op.expanduser(name)
                               for shortcut, name in dct['user_files'].items()}
        if 'calender_file' in dct:
            conf.calender_file = op.expanduser(dct['calender_file'])
            
    conf.initialized = True
    return conf
