
from .config import get_config
from path import Path

__version__ = "0.4.3"

CONFIG = get_config()
PRMS_DIR = Path(CONFIG['prms_dir'])
