from ryz.check import check
from ryz.condition import (
    ComparisonCondition,
    ComparisonMark,
    UnsupportedComparisonErr,
)
from ryz.err import InpErr


def test_int_equal():
    condition: ComparisonCondition[int] = ComparisonCondition(
        ComparisonMark.Equal,
        value=5,
    )

    assert condition.compare(5)
    assert not condition.compare(10)


def test_int_wrong_type():
    condition: ComparisonCondition[int] = ComparisonCondition(
        ComparisonMark.Equal,
        value=5,
    )

    check.expect(
        condition.compare,
        InpErr,
        "impostor",
    )


def test_int_less_equal():
    condition: ComparisonCondition[int] = ComparisonCondition(
        ComparisonMark.LessEqual,
        value=5,
    )

    assert condition.compare(1)
    assert condition.compare(5)
    assert not condition.compare(10)


def test_unsupported_comparison():
    condition: ComparisonCondition[dict[str, int]] = ComparisonCondition(
        ComparisonMark.LessEqual,
        value={"hello": 1},
    )

    check.expect(
        condition.compare,
        UnsupportedComparisonErr,
        {
            "world": 2,
        },
    )
