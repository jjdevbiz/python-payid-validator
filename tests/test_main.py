import pytest
from payid_validator import PayIdSyntaxError, PayIdUnusableError, validate_payid

@pytest.mark.parametrize(
    'payId_input,output',
    [
        (
            'Abc$example.com',
            'abc$example.com',
        )
    ]
)

def test_payid_valid(payId_input, output):
    assert validate_payid(payId_input) == output

