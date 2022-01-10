import argparse
import configparser
import os
import shutil
from pathlib import Path

CONFIGPATH = "~/.config/confi-path.ini"
DEFAULTS = {"PATHS": {"LocalRepo": "~/.local/config-repo/config", "SecretRepo": "~/.local/config-repo/secret"}}
HOME = Path.home()


def setup():
    config = configparser.ConfigParser()
    conffile = Path(CONFIGPATH)
    if conffile.exists() and conffile.stat().st_size:
        with conffile.open() as fh:
            config.read(fh)
    else:
        config.read_dict(DEFAULTS)
        with conffile.open("w") as fh:
            config.write(fh)
    for path in config["PATHS"].values():
        ppath = Path(path)
        ppath.mkdir(parents=True, exist_ok=True)
    return config


class Linker:
    def __init__(self, home, config):
        self.home = Path(home)
        self.config = config

    def _get_repo(self, is_secret):
        repo = self.config["PATHS"]["LocalRepo"]
        if is_secret:
            repo = self.config["PATHS"]["SecretRepo"]
        return Path(repo)

    def _link_file(self, orig, dest, filepath):
        if orig.is_dir():
            return ("NO DIRECTORY", "E!")
        if not orig.exists():
            return ("NOT FOUND", "E!")
        if dest.exists():
            if os.path.samefile(orig, dest):
                return ("HARDLINKED", "==")
            else:
                return ("DIFFERENT FILES", "E!")
        else:
            if len(filepath.parts) > 1:
                to_path = Path(*dest.parts[:-1])
                to_path.mkdir(parents=True, exist_ok=True)
            os.link(orig, dest)
            if dest.exists():
                return ("LINKED", "->")
            return ("FILE SYSTEM ERROR", "E!")

    def link(self, filename, is_secret=False):
        filepath = Path(filename)
        home_ln = self.home.joinpath(filepath)
        repo = self._get_repo(is_secret)
        repo_ln = repo.joinpath(filepath)
        msg, tag = self._link_file(home_ln, repo_ln, filepath)
        return {"from": home_ln, "to": repo_ln, "file": filepath, "msg": msg, "tag": tag}
