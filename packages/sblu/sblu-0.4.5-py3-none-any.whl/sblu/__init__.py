
from .config import get_config
from path import Path

from .version import version

__version__ = version


CONFIG = get_config()
PRMS_DIR = Path(CONFIG['prms_dir'])
