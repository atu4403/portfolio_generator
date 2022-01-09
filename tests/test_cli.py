import pytest
from click.testing import CliRunner
from portfolio_generator.cli import cli
import portfolio_generator.pfg


class TestCli:
    @pytest.fixture
    def d(self, tmpdir) -> str:
        p = tmpdir.chdir()
        yield
        p.chdir()

    def test_build(self, d):
        res = CliRunner().invoke(cli, args=["build", "-c test"])
        assert ("==> build command") in res.output
        print()


class TestInit:
    def test_init(self, mocker):
        mock = mocker.patch("portfolio_generator.pfg.Conf.init")
        res = CliRunner().invoke(cli, args=["init", "atu4403"])
        assert ("==> init") in res.output
        mock.assert_called_once_with("atu4403", False, False)

    def test_init_02(self, mocker):
        mock = mocker.patch("portfolio_generator.pfg.Conf.init")
        res = CliRunner().invoke(cli, args=["init", "atu4403", "--glo"])
        assert ("==> init") in res.output
        mock.assert_called_once_with("atu4403", True, False)

    def test_init_03(self, mocker):
        mock = mocker.patch("portfolio_generator.pfg.Conf.init")
        res = CliRunner().invoke(cli, args=["init", "atu4403", "--glo", "--force"])
        assert ("==> init") in res.output
        mock.assert_called_once_with("atu4403", True, True)
