import os
import stat


class memoize(dict):
    """
    Basic memoizing class, taken from
    http://wiki.python.org/moin/PythonDecoratorLibrary#Alternate_memoize_as_dict_subclass
    """

    def __init__(self, func):
        self.func = func
        self.memoized = {}

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result


def is_pipe(file_obj):
    return stat.S_ISFIFO(os.fstat(file_obj.fileno()).st_mode)


def add_atom_selection_arguments(parser):
    parser.add_argument("--only-CA",
                        action="store_true",
                        default=False,
                        help="Only use C-alpha atoms.")
    parser.add_argument("--only-backbone",
                        action="store_true",
                        default=False,
                        help="Only use backbone atoms.")
    parser.add_argument("--only-selection",
                        default=None,
                        help="Use ProDy selection to select atoms.")

    return parser


def _is_string_like(obj):
    """
    Check whether obj behaves like a string.
    """
    try:
        obj + ''
    except (TypeError, ValueError):
        return False
    return True


# Function to see if executable exists in $PATH
# borrowed from user "Jay" at stackoverflow.com
# https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    """Find an executable.

    Replicates the behavior of the 'which' shell built-in command. If no
    executable is found, returns None.
    """
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def compare_cache():
    pass
