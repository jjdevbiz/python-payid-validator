import pytest
from payid_validator import PayIdEncodingError, PayIdSyntaxError, PayIdUnusableError, validate_payid

@pytest.mark.parametrize(
    'payId_input,payId_output',
    [
        (
            'Abc$example.com',
            'abc$example.com'
        ),
        (
            'payid:ABC$example.com',
            'abc$example.com'
        ),
        (
            'rockhoward.reddit$payid.rockhoward.com',
            'rockhoward.reddit$payid.rockhoward.com'
        ),
        (
            'rockhoward-name.reddit$payid.rockhoward.com',
            'rockhoward-name.reddit$payid.rockhoward.com'
        ),
        (
            'rockhoward@reddit$payid.rockhoward.com',
            'rockhoward@reddit$payid.rockhoward.com'
        ),
        (
            'rock$howard@reddit$payid.rockhoward.com',
            'rock$howard@reddit$payid.rockhoward.com'
        ),
        (
            'Yamood.reddit$payid.rockhoward.com',
            'yamood.reddit$payid.rockhoward.com'
        ),
        (
            'payid:Yamood.reddit$payid.rockhoward.com',
            'yamood.reddit$payid.rockhoward.com'
        ),
        (
            'Rock-How_ard.reddit$payid.rockhoward.com',
            'rock-how_ard.reddit$payid.rockhoward.com'
        )
    ]
)

def test_payid_valid(payId_input, payId_output):
    output = validate_payid(payId_input)
    assert payId_output == str(output)


@pytest.mark.parametrize(
    'payId_input, payId_message',
    [
        (
            'rock howard.reddit$payid.rockhoward.com',
            "DISALLOWED/spaces"
        )
    ]
)

def test_payid_encoding(payId_input, payId_message):
    with pytest.raises(PayIdEncodingError) as e:
        assert validate_payid(payId_input)
    assert payId_message in str(e.value)


@pytest.mark.parametrize(
    'payId_input, payId_message',
    [
        (
            'ABC$Example.com',
            'The payID domain has bad characters (uppercase).'
        ),
        (
            'rockhoward.reddit$PayId.rockhoward.com',
            'The payID domain has bad characters (uppercase).'
        ),
        (
            'Rock-How_ard.reddit$PayId.rockhoward.com',
            'The payID domain has bad characters (uppercase).'
        ),
        (
            'rockhoward@gmail.com',
            'The required $ separator is missing.'
        ),
        (
            'rockhoward$.gmail.com',
            "The payId domain cannot start with '.'."
        ),
        (
            'rockhoward$payid.rockhoward.com.',
            "The payId domain cannot end with '.'."
        )
    ]
)

def test_payid_syntax(payId_input, payId_message):
    with pytest.raises(PayIdSyntaxError) as e:
        assert validate_payid(payId_input)
    assert str(e.value) == payId_message
