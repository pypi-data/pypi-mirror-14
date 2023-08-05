from __future__ import absolute_import
from .config import get_config
from path import Path

__version__ = "0.4.4"

CONFIG = get_config()
PRMS_DIR = Path(CONFIG['prms_dir'])
