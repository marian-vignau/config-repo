import tempfile
import unittest
from pathlib import Path

from src import linker


class TestOne(unittest.TestCase):
    def setUp(self):
        self.test_conf_file = tempfile.NamedTemporaryFile()
        linker.CONFIGPATH = self.test_conf_file.name
        linker.HOME = Path(__file__).parent / "test_data"
        self.test_local_dir = tempfile.TemporaryDirectory(dir=Path(__file__).parent)

        for k, v in linker.DEFAULTS["PATHS"].items():
            linker.DEFAULTS["PATHS"][k] = v.replace("~/.local/config-repo", self.test_local_dir.name)

    def tearDown(self):
        self.test_local_dir.cleanup()

    def test_1setup(self):
        config = linker.setup()
        assert Path(self.test_conf_file.name).stat().st_size > 0
        assert self.test_local_dir.name in config["PATHS"]["LocalRepo"]
        assert Path(config["PATHS"]["LocalRepo"]).exists()
        assert Path(config["PATHS"]["SecretRepo"]).exists()

    def test_2linker(self):
        config = linker.setup()
        link_obj = linker.Linker(linker.HOME, config)
        temp_files = [f for f in Path(config["PATHS"]["LocalRepo"]).glob("*")]
        assert not temp_files
        resp = link_obj.link(".tmux.conf")
        assert resp["to"].exists()
        resp = link_obj.link("non_existent")
        assert resp["tag"] == "E!"
        assert not resp["to"].exists()
        resp = link_obj.link(".config/nvim/init.vim")
        assert resp["to"].exists()
        temp_files_after = [f for f in Path(config["PATHS"]["LocalRepo"]).glob("*")]
        assert temp_files != temp_files_after

    def test_3secret(self):
        config = linker.setup()
        link_obj = linker.Linker(linker.HOME, config)
        temp_files = [f for f in Path(config["PATHS"]["SecretRepo"]).glob("*")]
        assert not temp_files
        resp = link_obj.link(".tmux.conf", is_secret=True)
        assert resp["to"].exists()
        resp = link_obj.link("non_existent", is_secret=True)
        assert resp["tag"] == "E!"
        assert not resp["to"].exists()
        resp = link_obj.link(".config/nvim/init.vim", is_secret=True)
        assert resp["to"].exists()
        temp_files_after = [f for f in Path(config["PATHS"]["SecretRepo"]).glob("*")]
        assert len(temp_files_after) == 2


if __name__ == "__main__":
    unittest.main()
