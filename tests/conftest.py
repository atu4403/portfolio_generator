import os
from pathlib import Path
import pytest


@pytest.fixture(scope="function")
def d(tmpdir) -> str:
    p = tmpdir.chdir()
    yield
    p.chdir()


@pytest.fixture(scope="function")
def case1():
    cwd = os.getcwd()
    _dir = Path("examples") / "case1"
    os.chdir(_dir)
    yield
    os.chdir(cwd)


@pytest.fixture(scope="function")
def case2():
    cwd = os.getcwd()
    _dir = Path("examples") / "case2"
    os.chdir(_dir)
    yield
    os.chdir(cwd)
