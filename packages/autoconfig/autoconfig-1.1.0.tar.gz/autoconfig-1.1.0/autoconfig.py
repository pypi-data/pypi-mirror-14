
__all__ = ['init']

import os, sys, configparser, re
from os.path import exists, isdir, abspath, join, dirname, isabs


class Parser(configparser.ConfigParser):
    # I want to use Python's ConfigParser to read the file, but it lowercases keys by default.
    # This is not acceptable for the [env] section.  I would like other sections to lowercase,
    # however, and there doesn't seem to be a good way to do that.  I tried providing a Boolean
    # and toggling it but that doesn't work.  For now I'm going to keep the case and lowercase
    # the keys myself.
    def __init__(self):
        configparser.ConfigParser.__init__(self, allow_no_value=True, comment_prefixes='#',
                                           interpolation=configparser.ExtendedInterpolation())
    def optionxform(self, option):
        return option


def init(filename='.config', searchfrom=None, env=None):
    """
    filename
      The name of the configuration file.

      This can be a simple filename, in which case the file will be searched for.  It can also
      be a fully qualified filename such as '/etc/project.conf'.

      If not provided, a file named ".config" will be searched for.

    searchfrom
      Optional directory to start searching from.  If not provided, the default is the current
      working directory.  To search from the directory where the calling code is located, use::

        autoconfig.init(searchfrom=__file__)

      This parameter is ignored if `filename` is a path since no search is performed.

    env
      Additional section names to treat as environment variables.  This can be a string for a
      single section or a list of names.

    Raises FileNotFoundError if the configuration file is not found.
    """
    fqn = _locate_config(filename, searchfrom)

    p = Parser()
    p.read(fqn)

    _copy_env(fqn, p, env)
    _setup_logging(p)


_STDOUT = sys.stdout
_GREEN = '\033[1m\033[32m'
_RESET = '\033[1m\033[0m'

class _StdoutWrapper(object):
    """
    We replace sys.stdout with an instance of this to add color to print
    statements.  You should only use print statements when developing /
    debugging.  Do not leave them in!
    """
    def __init__(self):
        sys.stdout = self

    def write(self, *args):
        # Note: Print statements in Python 3 seem to print the text and then a
        # new line.  Don't bother to color the newline.
        _STDOUT.write(_GREEN)
        _STDOUT.write(' '.join(args))
        _STDOUT.write(_RESET)

    def flush(self):
        _STDOUT.flush()

    def __getattr__(self, name):
        return getattr(_STDOUT, name)


def _setup_logging(p):
    if 'logging' not in p.sections():
        return

    d = { key.lower(): p.get('logging', key) for key in p.options('logging') }
    # (See the note in Parser about case.)

    import logging, logging.handlers

    # Setup file and console handlers if requested.  If colorlog exists, the console output
    # will be in color.

    handlers = []
    filename = d.get('filename')
    if filename:
        format = d.get('format', "%(asctime)s %(levelname).1s %(name)s %(message)s")
        h = logging.handlers.TimedRotatingFileHandler(filename, when='midnight', backupCount=6)
        h.setLevel(logging.DEBUG)
        h.setFormatter(logging.Formatter(format))
        handlers.append(h)

    console = d.get('console', 'false')
    if console.lower() in ('true', 'short', 'long'):
        format = '%(levelname).1s %(name)s %(message)s'
        if console == 'long':
            format = '%(asctime)s ' + format

        try:
            from colorlog import ColoredFormatter
            formatter = ColoredFormatter(
                '%(log_color)s' + format,
                reset=True,
                log_colors={
                    'DEBUG':    'cyan',
                    'INFO':     'white',
                    'WARNING':  'yellow',
                    'ERROR':    'bg_red,white',
                    'CRITICAL': 'bg_red,white',
                },
                secondary_log_colors={},
                style='%')
        except:
            formatter = logging.Formatter(format)

        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        h.setFormatter(formatter)
        handlers.append(h)

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    if handlers:
        root.handlers = handlers

    re_sep = re.compile(r'[\s,]+')
    names = set()
    names.update(name for name in re_sep.split(os.environ.get('DEBUG', '')) if name)
    names.update(name for name in re_sep.split(d.get('debug', '')) if name)

    for name in names:
        l = logging.getLogger(name)
        l.setLevel(logging.DEBUG)

    # Redirect stdout so we can color print statements too.
    sys.stdout = _StdoutWrapper()



def _copy_env(fqn, p, env):
    """
    Copies the items from the [env] section, and any additional sections listed in 'env'
    to os.environ.

    If PYTHONPATH is provided, it is parsed and prefixed to the system path.

    fqn
      The fully qualified path of the configuration file.

    p
      The ConfigParser

    env
      Optional list of environment sections to add to the environment.
    """
    envs = ['env']
    if env:
        assert isinstance(env, (str, list))
        if isinstance(env, str):
            envs.append(env)
        else:
            envs.extend(env)

    paths = []

    for name in envs:
        if name in p.sections():
            for key, value in p[name].items():
                if value is None or value == '':
                    # A key with no value is used to "unset".
                    if key in os.environ:
                        del os.environ[key]
                else:
                    # Do we need to check the encoding?
                    os.environ[key] = value

                    if key == 'PYTHONPATH':
                        paths.extend(value.split(os.pathsep))

    # If we found any PYTHONPATH entries, add them to the system path.  Make sure you keep the
    # original order.  If they are not fully qualified, they are relative to the configuration
    # file

    if paths:
        rootdir = dirname(fqn)
        paths = [ (path if isabs(path) else join(rootdir, path)) for path in paths if path ]
        sys.path[:0] = paths



def _locate_config(filename, searchfrom):
    """
    Locates the configuration file.

    We're going to allow filename to be a path to a different file so we can accept __file__.
    """
    if os.sep in filename and searchfrom:
        raise ValueError('Cannot provide a path in `filename` and a `searchfrom` value.')

    if isabs(filename):
        if not exists(filename):
            raise FileNotFoundError('Did not find configuration file.  filename=%r' % filename)
        return filename

    searchfrom = abspath(searchfrom or os.getcwd())
    path = searchfrom

    while 1:
        if isdir(path):
            fqn = join(path, filename)
            if exists(fqn) and not isdir(fqn):
                return fqn

        parent = dirname(path)
        if parent == path:
            raise FileNotFoundError('Did not find configuration file.  filename=%r searchfrom=%s' % (filename, searchfrom))
        path = parent
