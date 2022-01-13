import os
import pytest


@pytest.fixture(scope="function")
def d(tmpdir) -> str:
    p = tmpdir.chdir()
    yield
    p.chdir()


@pytest.fixture(scope="function")
def case1():
    os.chdir("examples/case1")
    yield
    os.chdir("../..")


@pytest.fixture(scope="function")
def case2():
    os.chdir("examples/case2")
    yield
    os.chdir("../..")
