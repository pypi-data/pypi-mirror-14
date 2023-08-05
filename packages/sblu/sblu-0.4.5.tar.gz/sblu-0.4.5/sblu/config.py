import os
import getpass
from configobj import ConfigObj

from path import Path

DEFAULTS = {
    "cluspro": {
        "local_path": None,
        "username": None,
        "api_secret": None,
        "server": "cluspro.bu.edu"
    },
    "ftmap": {
        "local_path": None
    },
    "prms_dir": os.path.join(os.environ['HOME'], "prms")
}


def get_config(config_path="~/.sblurc"):
    config = ConfigObj(DEFAULTS)

    config_file = Path(config_path).expand()
    if config_file.exists():
        config.merge(ConfigObj(config_file))
    else:
        config.filename = config_file
        config.write()
        config.filename = None

    return config
