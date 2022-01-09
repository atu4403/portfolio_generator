import pytest
import os
import pathlib
import adash as _
from src.portfolio_generator.pfg import (
    Conf,
    Pfg,
    ConfigExistsError,
    ConfigDirectoryNotExistsError,
    ConfigFileNotExistsError,
    InvalidYamlFormatError,
)


class TestConf:
    @pytest.fixture
    def case1(self):
        os.chdir("examples/case1")
        yield
        os.chdir("../..")

    @pytest.fixture
    def case2(self):
        os.chdir("examples/case2")
        yield
        os.chdir("../..")

    @pytest.fixture
    def d(self, tmpdir) -> str:
        p = tmpdir.chdir()
        yield
        p.chdir()

    def test_conf(self, case1):
        # pwd = os.getcwd()
        # assert pwd == "/Users/atu/ghq/github.com/atu4403/portfolio_generator"
        # c = Conf()
        assert Pfg().search_dir == pathlib.PosixPath(".pfg")

    def test_conf_dir_exists_error(self, case1):
        with pytest.raises(ConfigDirectoryNotExistsError) as e:
            c = Conf()
            c.init("atu4403")
        assert "config directory already exists." in str(e.value)

    def test_conf_invalid_yaml_1(self, case1):
        with pytest.raises(InvalidYamlFormatError):
            c = Conf()
            c.load("portfolio2.yml")

    def test_conf_invalid_yaml_2(self, case1):
        with pytest.raises(InvalidYamlFormatError):
            c = Conf()
            c.load("portfolio3.yml")

    def test_conf_file_not_exists(self, case1):
        with pytest.raises(ConfigFileNotExistsError):
            c = Conf()
            c.load("portfolio4.yml")

    def test_no_conf_dir(self, d):
        c = Conf()
        assert c.dot.search_dir is None
        with pytest.raises(ConfigDirectoryNotExistsError):
            c.load("portfolio.yml")

    def test_init(self, d):
        filename = "portfolio.yml"
        c = Conf()
        c.init("atu4403")
        yml = c.load(filename)
        assert yml["user"] == "atu4403"
        tpl = (c.dot.search_dir / "portfolio.j2").read_text()
        assert tpl.startswith("# {{ user }}")
