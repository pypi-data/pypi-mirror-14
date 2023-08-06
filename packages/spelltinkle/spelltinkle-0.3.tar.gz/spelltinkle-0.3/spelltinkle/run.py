import argparse
import logging
import os
import os.path as op
import random
import subprocess
import sys
from importlib.util import find_spec

from spelltinkle.config import configure
from spelltinkle.i18n import set_language
from spelltinkle.session import Session
from spelltinkle.screen import Screen


dir = op.expanduser('~/.spelltinkle')
if not op.isdir(dir):
    os.mkdir(dir)

logging.basicConfig(filename=op.join(dir,
                                     'debug{}.txt'.format(
                                         random.randint(0, 10000))),
                    filemode='w', level=logging.DEBUG)


def run(args=None):
    parser = argparse.ArgumentParser()
    add = parser.add_argument
    add('files', nargs='*')
    add('-w', '--new-window', action='store_true')
    add('-u', '--user')
    add('-m', '--module', action='append', default=[])
    add('-S', '--self-test', action='store_true')
    add('-D', '--debug', action='store_true')
    add('-L', '--language')
    args = parser.parse_args(args)

    set_language(args.language)
    
    if args.new_window:
        for option in ['-w', '--new-window']:
            if option in sys.argv:
                sys.argv.remove(option)
        subprocess.check_call([os.environ['COLORTERM'],
                               '--geometry', '84x35', '-e'] +
                              [' '.join(sys.argv)])
        return
        
    if args.self_test:
        from spelltinkle.test.selftest import test
        return test(args.files)
    
    for module in args.module:
        args.files.append(find_spec(module).origin)

    if args.user:
        config = configure()
        args.files.append(config.user_files[args.user])
        
    scr = Screen()
    session = Session(args.files, scr)
    session.run()
    scr.stop()

    
if __name__ == '__main__':
    run()
