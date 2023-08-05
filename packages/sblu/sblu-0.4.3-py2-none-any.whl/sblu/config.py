import os
import getpass
from configobj import ConfigObj

from path import path

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
    "scc": {
        "hostname": "scc1.bu.edu",
        "username": getpass.getuser()
    },
    "prms_dir": os.path.join(os.environ['HOME'], "prms")
}


def get_config():
    config = ConfigObj(DEFAULTS)

    config_file = path("~/.sblurc").expand()
    if config_file.exists():
        config.merge(ConfigObj(config_file))
    else:
        config.filename = config_file
        config.write()
        config.filename = None

    return config
