from pykit import validation
from pykit.env import EnvSpec, EnvUtils
from pykit.errors.expect import StrExpectError
from pykit.errors.main import PleaseDefineError


def test_get(
    setenv_pykittest_env_to_hello,
):
    assert EnvUtils.get(EnvSpec(
        key="PYKITTEST_ENV",
    )) == "hello"


def test_get_default():
    assert EnvUtils.get(EnvSpec(
        key="PYKITTEST_ENV",
        default="wow",
    )) == "wow"


def test_get_bool_0(
    setenv_pykittest_env_to_0,
):
    assert EnvUtils.get_bool(EnvSpec(
        key="PYKITTEST_ENV",
    )) is False


def test_get_bool_1(
    setenv_pykittest_env_to_1,
):
    assert EnvUtils.get_bool(EnvSpec(
        key="PYKITTEST_ENV",
    )) is True


def test_get_bool_default_0():
    assert EnvUtils.get_bool(EnvSpec(
        key="PYKITTEST_ENV",
        default="0",
    )) is False


def test_get_bool_default_1():
    assert EnvUtils.get_bool(EnvSpec(
        key="PYKITTEST_ENV",
        default="1",
    )) is True


def test_get_please_define_error():
    validation.expect(
        EnvUtils.get,
        PleaseDefineError,
        EnvSpec(
            key="PYKITTEST_ENV",
        ),
    )


def test_get_bool_str_expect_error(
    setenv_pykittest_env_to_hello,
):
    validation.expect(
        EnvUtils.get_bool,
        StrExpectError,
        EnvSpec(
            key="PYKITTEST_ENV",
        ),
    )


def test_get_bool_str_expect_error_from_default():
    validation.expect(
        EnvUtils.get_bool,
        StrExpectError,
        EnvSpec(
            key="PYKITTEST_ENV",
            default="malformed",
        ),
    )
