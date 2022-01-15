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
    def test_conf(self, case1):
        assert str(Pfg().search_dir) == ".pfg"

    def test_conf_dir_exists_error(self, case1):
        with pytest.raises(ConfigExistsError) as e:
            c = Conf()
            c.init("atu4403")
        assert "config ディレクトリはすでに存在します" in str(e.value)

    def test_conf_invalid_yaml_1(self, case1):
        with pytest.raises(InvalidYamlFormatError) as e:
            c = Conf()
            c.load("portfolio2.yml")
        assert "portfolio2.yml invalid: must be of dict type" in str(e.value)

    def test_conf_invalid_yaml_2(self, case1):
        with pytest.raises(InvalidYamlFormatError) as e:
            c = Conf()
            c.load("portfolio3.yml")
        assert "portfolio3.yml invalid: {'no_names': ['unknown field']" in str(e.value)
        assert "template': ['required field'], 'test': ['unknown field']}" in str(e.value)

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
        res = c.init("atu4403")
        assert res.endswith(".pfg")
        yml = c.load(filename)
        assert yml["user"] == "atu4403"
        tpl = (c.dot.search_dir / "portfolio.j2").read_text()
        assert tpl.startswith("# {{ user }}")
