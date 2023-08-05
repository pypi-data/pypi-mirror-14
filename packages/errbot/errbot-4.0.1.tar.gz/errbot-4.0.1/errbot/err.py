#!/usr/bin/env python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import inspect
import os
import sys
import logging
import argparse
from os import path, sep, getcwd, access, W_OK
from platform import system
from .plugin_wizard import new_plugin_wizard
from .version import VERSION

PY3 = sys.version_info[0] == 3
PY2 = not PY3

# Fail early if the user tries to run err under the incorrect interpreter


def foo(param='canary'):
    pass

foo_src = inspect.getsourcelines(foo)[0][0]

if PY3 and "param=u'canary'" in foo_src:
    print('Err has been converted to Python2 but you try to run it under Python3')
    sys.exit(-1)

if PY2 and "param='canary'" in foo_src:
    print('You are trying to run err under python2 without converting the source code to py2 first.')
    print('Either use python3 or install err using ./setup.py develop.')
    sys.exit(-1)

if sys.getdefaultencoding().lower() != 'utf-8':
    logging.warning('Starting errbot with a default system encoding other than \'utf-8\''
                    ' might cause you a heap of troubles.'
                    ' Your current encoding is set at \'%s\'' % sys.getdefaultencoding())

log = logging.getLogger(__name__)


# noinspection PyUnusedLocal
def debug(sig, frame):
    """Interrupt running process, and provide a python prompt for
    interactive debugging."""
    d = {'_frame': frame}  # Allow access to frame object.
    d.update(frame.f_globals)  # Unless shadowed by global
    d.update(frame.f_locals)

    i = code.InteractiveConsole(d)
    message = "Signal received : entering python shell.\nTraceback:\n"
    message += ''.join(traceback.format_stack(frame))
    i.interact(message)


def ispydevd():
    for frame in inspect.stack():
        if frame[1].endswith("pydevd.py"):
            return True
    return False

ON_WINDOWS = system() == 'Windows'

if not ON_WINDOWS:
    from daemonize import Daemonize
    import code
    import traceback
    import signal

    signal.signal(signal.SIGUSR1, debug)  # Register handler for debugging

logger = logging.getLogger('')
logging.getLogger('yapsy').setLevel(logging.INFO)  # this one is way too verbose in debug
logging.getLogger('Rocket.Errors.ThreadPool').setLevel(logging.INFO)  # this one is way too verbose in debug
logger.setLevel(logging.INFO)

pydev = ispydevd()
stream = sys.stdout if pydev else sys.stderr
isatty = pydev or stream.isatty()  # force isatty if we are under pydev because it supports coloring anyway.
console_hdlr = logging.StreamHandler(stream)

if isatty:
    from colorlog import ColoredFormatter  # noqa
    formatter = ColoredFormatter(
        "%(asctime)s %(log_color)s%(levelname)-8s%(reset)s "
        "%(blue)s%(name)-25.25s%(reset)s %(white)s%(message)s%(reset)s",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }
    )
    console_hdlr.setFormatter(formatter)
else:
    console_hdlr.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(name)-25s %(message)s"))
logger.addHandler(console_hdlr)


def get_config(config_path):
    __import__('errbot.config-template')  # - is on purpose, it should not be imported normally ;)
    template = sys.modules['errbot.config-template']
    config_fullpath = config_path
    if not path.exists(config_fullpath):
        log.error(
            'I cannot find the file %s \n'
            '(You can change this path with the -c parameter see --help)' % config_path
        )
        log.info(
            'You can use the template %s as a base and copy it to %s. \nYou can then customize it.' % (
                path.dirname(template.__file__) + sep + 'config-template.py', config_path)
        )
        exit(-1)

    # noinspection PyBroadException
    try:
        config = __import__(path.splitext(path.basename(config_fullpath))[0])

        diffs = [item for item in set(dir(template)) - set(dir(config)) if not item.startswith('_')]
        if diffs:
            log.error('You are missing configs defined from the template :')
            for diff in diffs:
                log.error('Missing config : %s' % diff)
            exit(-1)
    except Exception as _:
        log.exception('I could not import your config from %s, please check the error below...' % config_fullpath)
        exit(-1)
    log.info('Config check passed...')
    return config


def main():

    execution_dir = getcwd()

    # By default insert the execution path (useful to be able to execute err from
    # the source tree directly without installing it.
    sys.path.insert(0, execution_dir)

    parser = argparse.ArgumentParser(description='The main entry point of the errbot.')
    parser.add_argument('-c', '--config', default=None,
                        help='Full path to your config.py (default: config.py in current working directory).')

    mode_selection = parser.add_mutually_exclusive_group()
    mode_selection.add_argument('-v', '--version', action='version', version='Errbot version {}'.format(VERSION))
    mode_selection.add_argument('-r', '--restore', nargs='?', default=None, const='default',
                                help='restore a bot from backup.py (default: backup.py from the bot data directory)')
    mode_selection.add_argument('-l', '--list', action='store_true', help='list all available backends')
    mode_selection.add_argument('--new-plugin', nargs='?', default=None, const='current_dir',
                                help='create a new plugin in the specified directory')
    mode_selection.add_argument('-T', '--text', dest="backend", action='store_const', const="Text",
                                help='force local text backend')
    mode_selection.add_argument('-G', '--graphic', dest="backend", action='store_const', const="Graphic",
                                help='force local graphical backend')

    if not ON_WINDOWS:
        option_group = parser.add_argument_group('optional daemonization arguments')
        option_group.add_argument('-d', '--daemon', action='store_true', help='Detach the process from the console')
        option_group.add_argument('-p', '--pidfile', default=None,
                                  help='Specify the pid file for the daemon (default: current bot data directory)')

    args = vars(parser.parse_args())  # create a dictionary of args

    # This must come BEFORE the config is loaded below, to avoid printing
    # logs as a side effect of config loading.
    if args['new_plugin']:
        directory = os.getcwd() if args['new_plugin'] == "current_dir" else args['new_plugin']
        for handler in logging.getLogger().handlers:
            logger.removeHandler(handler)
        try:
            new_plugin_wizard(directory)
        except KeyboardInterrupt:
            sys.exit(1)
        except Exception as e:
            sys.stderr.write(str(e) + "\n")
            sys.exit(1)
        finally:
            sys.exit(0)

    config_path = args['config']
    # setup the environment to be able to import the config.py
    if config_path:
        # appends the current config in order to find config.py
        sys.path.insert(0, path.dirname(path.abspath(config_path)))
    else:
        config_path = execution_dir + sep + 'config.py'

    config = get_config(config_path)  # will exit if load fails
    if args['list']:
        from errbot.main import enumerate_backends
        print('Available backends:')
        for backend_name in enumerate_backends(config):
            print('\t\t%s' % backend_name)
        sys.exit(0)

    if args['restore']:
        backend = 'Null'  # we don't want any backend when we restore
    elif args['backend'] is None:
        if not hasattr(config, 'BACKEND'):
            log.fatal("The BACKEND configuration option is missing in config.py")
            sys.exit(1)
        backend = config.BACKEND
    else:
        backend = args['backend']

    log.info("Selected backend '%s'." % backend)

    # Check if at least we can start to log something before trying to start
    # the bot (esp. daemonize it).

    log.info("Checking for '%s'..." % config.BOT_DATA_DIR)
    if not path.exists(config.BOT_DATA_DIR):
        raise Exception("The data directory '%s' for the bot does not exist" % config.BOT_DATA_DIR)
    if not access(config.BOT_DATA_DIR, W_OK):
        raise Exception("The data directory '%s' should be writable for the bot" % config.BOT_DATA_DIR)

    if (not ON_WINDOWS) and args['daemon']:
        if args['text']:
            raise Exception('You cannot run in text and daemon mode at the same time')
        if args['restore']:
            raise Exception('You cannot restore a backup in daemon mode.')
        if args['pidfile']:
            pid = args['pidfile']
        else:
            pid = config.BOT_DATA_DIR + sep + 'err.pid'

        # noinspection PyBroadException
        try:
            def action():
                from errbot.main import main
                main(backend, logger, config)

            daemon = Daemonize(app="err", pid=pid, action=action, chdir=os.getcwd())
            daemon.start()
        except Exception:
            log.exception('Failed to daemonize the process')
        exit(0)
    from errbot.main import main
    restore = args['restore']
    if restore == 'default':  # restore with no argument, get the default location
        restore = path.join(config.BOT_DATA_DIR, 'backup.py')

    main(backend, logger, config, restore)
    log.info('Process exiting')

if __name__ == "__main__":
    main()
