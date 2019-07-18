import pytest

import mediares.constants


@pytest.mark.parametrize(
    'gender', mediares.constants.Gender,
)
def test_gender_repr(gender):
    assert gender.name in repr(gender)
