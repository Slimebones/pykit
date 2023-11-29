from sbpykit.condition import ComparisonCondition, ComparisonMark
from sbpykit.expectation import ListExpectation

one_item_list_expectation: ListExpectation = ListExpectation(
    count=ComparisonCondition(
        mark=ComparisonMark.Equal,
        value=1,
    ),
)
