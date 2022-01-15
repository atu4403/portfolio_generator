import os
import pytest
from src.portfolio_generator.build import Build
from src.portfolio_generator.pfg import (
    Conf,
    ConfigDirectoryNotExistsError,
    ConfigFileNotExistsError,
    InvalidYamlFormatError,
    TemplateFileNotExistsError,
)


class TestBuild:
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

    def test_build_case1(self, case1):
        # Conf().init("atu4403")
        Build("portfolio.yml", output="README.md", offline=True).execute()

    @pytest.mark.heavy
    def test_build_tmp(self, d):
        Conf().init("atu4403")
        Build("portfolio.yml", output="README.md").execute()

    def test_build_ConfigDirectoryNotExistsError(self, d):
        with pytest.raises(ConfigDirectoryNotExistsError) as e:
            Build().execute()
        assert str(e.value) == "configディレクトリが存在しません。'pfg init'を実行してください"

    def test_build_ConfigFileNotExistsError(self, case1):
        with pytest.raises(ConfigFileNotExistsError) as e:
            Build("portfolio1.yml").execute()
        assert str(e.value) == "portfolio1.ymlは存在しません"

    def test_build_InvalidYamlFormatError(self, case1):
        with pytest.raises(InvalidYamlFormatError) as e:
            Build("portfolio2.yml").execute()
        assert str(e.value) == "portfolio2.yml invalid: must be of dict type"

    def test_build_TemplateFileNotExistsError(self, case2):
        with pytest.raises(TemplateFileNotExistsError) as e:
            Build("portfolio.yml").execute()
        assert str(e.value) == "portfolio.ymlは存在しません"
