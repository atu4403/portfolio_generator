import pytest
from src.portfolio_generator.build import Build
from src.portfolio_generator.pfg import Conf


class TestBuild:
    @pytest.fixture
    def d(self, tmpdir) -> str:
        p = tmpdir.chdir()
        yield
        p.chdir()

    # def test_config_not_exists(self):
    #     with pytest.raises(ConfigNotExistsError) as e:
    #         b = Build()
    #     assert "portfolio.yml not exists" in str(e.value)

    # def test_invalid_yaml_format(self):
    #     with pytest.raises(InvalidYamlFormatError) as e:
    #         b = Build("tests/invalid.yml")
    #     assert "tests/invalid.yml can not be read" in str(e.value)

    def test_build(self, d):
        Conf().init("atu4403")
        b = Build("portfolio.yml")
        b.execute()
