import os.path

CONFIG_FILENAME = os.path.expanduser("~/.caenbrewrc")
"""The file in which one's Caenbrew configuration is stored."""

_default_config = {
    "prefix_dir": os.path.expanduser("~/.local"),
    "verbose": False,
}

_types = {
    "prefix_dir": os.path.expanduser,
    "verbose": bool,
}


def get_config():
    """Get the user's configuration."""
    config = _default_config.copy()
    if not os.path.isfile(CONFIG_FILENAME):
        return config

    with open(CONFIG_FILENAME) as f:
        lines = f.read().splitlines()

    for line in lines:
        try:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
        except ValueError:
            raise ValueError(
                "Expected line in form 'foo = bar', "
                "got: {}".format(line)
            )

        if key not in config:
            raise ValueError("Invalid key: {}".format(key))
        config[key] = _types[key](value)
    return config
