import os

import pytest


@pytest.fixture
def setenv_pykittest_env_to_hello():
    os.environ["PYKITTEST_ENV"] = "hello"
    yield
    del os.environ["PYKITTEST_ENV"]


@pytest.fixture
def setenv_pykittest_env_to_0():
    os.environ["PYKITTEST_ENV"] = "0"
    yield
    del os.environ["PYKITTEST_ENV"]


@pytest.fixture
def setenv_pykittest_env_to_1():
    os.environ["PYKITTEST_ENV"] = "1"
    yield
    del os.environ["PYKITTEST_ENV"]
