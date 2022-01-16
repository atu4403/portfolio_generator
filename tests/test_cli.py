import pytest
from click.testing import CliRunner
from portfolio_generator.cli import cli
import portfolio_generator.pfg
from portfolio_generator.build import Build


class TestCli:
    @pytest.mark.parametrize(
        "test_args",
        [
            (["build", "-c", "test", "-o", "A.txt"]),
            (["build", "-ctest", "-o", "A.txt"]),
            (["build", "--config", "test", "--out", "A.txt"]),
        ],
    )
    def test_build(self, mocker, test_args):
        mock = mocker.patch.object(Build, "__init__", return_value=None)
        res = CliRunner().invoke(cli, args=test_args)
        mock.assert_called_once_with(**{"offline": False, "output": "A.txt", "path": "test"})

    def test_build_2(self, mocker):
        mock = mocker.patch.object(Build, "__init__", return_value=None)
        res = CliRunner().invoke(cli, args=["build", "--offline"])
        print(mock.call_args_list)
        mock.assert_called_once_with(**{"offline": True, "output": "", "path": "portfolio.yml"})

    def test_help(self):
        res = CliRunner().invoke(cli, args=["--help"])
        assert "--help  Show this message and exit." in res.output


class TestInit:
    def test_init(self, mocker):
        mock = mocker.patch("portfolio_generator.pfg.Conf.init")
        res = CliRunner().invoke(cli, args=["init", "-n", "atu4403"])
        assert ("==> init") in res.output
        mock.assert_called_once_with("atu4403", False, False)

    def test_init_02(self, mocker):
        mock = mocker.patch("portfolio_generator.pfg.Conf.init")
        res = CliRunner().invoke(cli, args=["init", "-n", "atu4403", "--glo"])
        assert ("==> init") in res.output
        mock.assert_called_once_with("atu4403", True, False)

    def test_init_03(self, mocker):
        mock = mocker.patch("portfolio_generator.pfg.Conf.init")
        res = CliRunner().invoke(cli, args=["init", "-n", "atu4403", "--glo", "--force"])
        assert ("==> init") in res.output
        mock.assert_called_once_with("atu4403", True, True)

    def test_init_04(self, mocker):
        mock = mocker.patch("portfolio_generator.pfg.Conf.init")
        res = CliRunner().invoke(cli, args=["init"], input="atu4403")
        assert ("==> init") in res.output
        mock.assert_called_once_with("atu4403", False, False)


class Testvalidate:
    @pytest.mark.parametrize(
        "test_args,expected",
        [
            (["validate", "-c", "test"], ["test"]),
            (["validate"], ["portfolio.yml"]),
        ],
    )
    def test_validate(self, mocker, test_args, expected):
        mock = mocker.patch("portfolio_generator.pfg.Conf.load")
        res = CliRunner().invoke(cli, args=test_args)
        assert ("==> validate") in res.output
        mock.assert_called_once_with(*expected)

    def test_validate_cli_ok(self, case1):
        res = CliRunner(mix_stderr=False).invoke(cli, args=["validate", "-c", "portfolio.yml"])
        assert res.exit_code == 0
        assert "==> validate" in res.stdout
        assert "portfolio.yml is clean" in res.stdout

    def test_validate_cli_error(self, case1):
        res = CliRunner(mix_stderr=False).invoke(cli, args=["validate", "-c", "portfolio2.yml"])
        assert res.exit_code == 1
        assert "==> validate" in res.stdout
        assert "error: portfolio2.yml invalid: must be of dict type" in res.stderr
