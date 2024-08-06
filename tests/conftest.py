import os

import pytest


@pytest.fixture
def setenv_ryztest_env_to_hello():
    os.environ["RYZTEST_ENV"] = "hello"
    yield
    del os.environ["RYZTEST_ENV"]


@pytest.fixture
def setenv_ryztest_env_to_0():
    os.environ["RYZTEST_ENV"] = "0"
    yield
    del os.environ["RYZTEST_ENV"]


@pytest.fixture
def setenv_ryztest_env_to_1():
    os.environ["RYZTEST_ENV"] = "1"
    yield
    del os.environ["RYZTEST_ENV"]
