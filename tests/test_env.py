from ryz.check import check
from ryz.env import EnvUtils
from ryz.core import InpErr, NotFoundErr


def test_get(
    setenv_ryztest_env_to_hello,
):
    assert EnvUtils.get(
        key="RYZTEST_ENV",
    ) == "hello"

def test_get_default():
    assert EnvUtils.get(
        key="RYZTEST_ENV",
        default="wow",
    ) == "wow"

def test_get_bool_0(
    setenv_ryztest_env_to_0,
):
    assert EnvUtils.get_bool(
        key="RYZTEST_ENV",
    ) is False


def test_get_bool_1(
    setenv_ryztest_env_to_1,
):
    assert EnvUtils.get_bool(
        key="RYZTEST_ENV",
    ) is True


def test_get_bool_default_0():
    assert EnvUtils.get_bool(
        key="RYZTEST_ENV",
        default="0",
    ) is False


def test_get_bool_default_1():
    assert EnvUtils.get_bool(
        key="RYZTEST_ENV",
        default="1",
    ) is True


def test_get_not_found_err():
    check.expect(
        EnvUtils.get,
        NotFoundErr,
        key="RYZTEST_ENV",
    )


def test_get_bool_inp_err(
    setenv_ryztest_env_to_hello,
):
    check.expect(
        EnvUtils.get_bool,
        InpErr,
        key="RYZTEST_ENV",
    )


def test_get_bool_inp_err_from_default():
    check.expect(
        EnvUtils.get_bool,
        InpErr,
        key="RYZTEST_ENV",
        default="malformed",
    )
