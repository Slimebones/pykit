from ryz import env
from ryz.core import Err, ecode


def test_get(
    setenv_ryztest_env_to_hello,
):
    assert env.get(
        key="RYZTEST_ENV",
    ).unwrap() == "hello"

def test_get_default():
    assert env.get(
        key="RYZTEST_ENV",
        default="wow",
    ).unwrap() == "wow"

def test_get_bool_0(
    setenv_ryztest_env_to_0,
):
    assert env.get_bool(
        key="RYZTEST_ENV",
    ).unwrap() is False


def test_get_bool_1(
    setenv_ryztest_env_to_1,
):
    assert env.get_bool(
        key="RYZTEST_ENV",
    ).unwrap() is True


def test_get_bool_default_0():
    assert env.get_bool(
        key="RYZTEST_ENV",
        default="0",
    ).unwrap() is False


def test_get_bool_default_1():
    assert env.get_bool(
        key="RYZTEST_ENV",
        default="1",
    ).unwrap() is True


def test_get_not_found_err():
    r = env.get("RYZTEST_ENV")
    assert isinstance(r, Err)
    assert r.is_(ecode.NotFound)

def test_get_bool_inp_err(
    setenv_ryztest_env_to_hello,
):
    r = env.get_bool("RYZTEST_ENV")
    assert isinstance(r, Err)

def test_get_bool_inp_err_from_default():
    r = env.get_bool("RYZTEST_ENV", "malformed")
    assert isinstance(r, Err)
