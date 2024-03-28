import pytest
from math_operations import add_two_nums

@pytest.mark.parametrize(
        "num1, num2, result",
        [
            (1, 1, 2),
            (10, 20, 30),
            (2, -3, -1)
        ]
)
def test_add_two_nums(num1, num2, result):
    assert add_two_nums(num1, num2) == result