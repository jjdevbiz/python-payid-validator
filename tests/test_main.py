import pytest
from payid_validator import PayIdSyntaxError, PayIdUnusableError, validate_payid

@pytest.mark.parametrize(
    'payId_input,output',
    [
        (
            'Abc$example.com',
            'payid:abc$example.com'
        ),
        (
            'payid:ABC$Example.com',
            'payid:abc$example.com'
        ),
        (
            'rockhoward.reddit$payid.rockhoward.com',
            'payid:rockhoward.reddit$payid.rockhoward.com'
        ),
        (
            'rockhoward.reddit$PayId.rockhoward.com',
            'payid:rockhoward.reddit$payid.rockhoward.com'
        ),
        (
            'rockhoward@reddit$payid.rockhoward.com',
            'payid:rockhoward@reddit$payid.rockhoward.com'
        ),
        (
            'rock$howard@reddit$payid.rockhoward.com',
            'payid:rock$howard@reddit$payid.rockhoward.com'
        ),
        (
            'payid:Yamood.reddit$payid.rockhoward.com',
            'payid:yamood.reddit$payid.rockhoward.com'
        ),
        (
            'Rock-How_ard.reddit$PayId.rockhoward.com',
            'payid:rock-how_ard.reddit$payid.rockhoward.com'
        )
    ]
)

def test_payid_valid(payId_input, output):
    assert validate_payid(payId_input) == output

@pytest.mark.parametrize(
    'payId_input',
    [
        (
            'Abc$example.com'
        ),
        (
            'ABC$Example.com'
        ),
        (
            'rockhoward.reddit$PayId.rockhoward.com'
        ),
        (
            'Yamood.reddit$payid.rockhoward.com'
        ),
        (
            'Rock-How_ard.reddit$PayId.rockhoward.com'
        ),
        (
            'rockhoward@gmail.com'
        ),
        (
            'rockhoward$.gmail.com'
        ),
        (
            'rockhoward$payid.rockhoward.com.'
        )
    ]
)

def test_payid_syntax(payId_input):
    with pytest.raises(PayIdSyntaxError) as excinfo:
        validate_payid(payId_input, ignore_case=False)
