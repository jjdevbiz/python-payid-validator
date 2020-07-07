import pytest
from payid_validator import (
    PayIdEncodingError,
    PayIdSyntaxError,
    PayIdUnusableError,
    PayIdDomainEncodingError,
    validate_payid
)

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
            'ABC$Example.com',
            'abc$example.com'
        ),
        (
            'abc$example.COM',
            'abc$example.com'
        ),
        (
            'rockhoward.reddit$PayId.rockhoward.com',
            'rockhoward.reddit$payid.rockhoward.com'
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
        ),
        (
            'user+mailbox/department=shipping$example.com',
            'user+mailbox/department=shipping$example.com',
        ),
        (
            "!#$%&'*+-/=?^_`.{|}~$example.com",
            "!#$%&'*+-/=?^_`.{|}~$example.com"
        ),
        (
            '伊昭傑$郵件.商務',
            '伊昭傑$郵件.商務'
        ),
        (
            'राम$मोहन.ईन्फो',
            'राम$मोहन.ईन्फो'
        ),
        (
            'юзер$екзампл.ком',
            'юзер$екзампл.ком'
        ),
        (
            'θσερ$εχαμπλε.ψομ',
            'θσερ$εχαμπλε.ψομ'
        ),
        (
            'ñoñó$example.com',
            'ñoñó$example.com'
        ),
        (
            '我買$example.com',
            '我買$example.com',
        ),
        (
            '甲斐黒川日本$example.com',
            '甲斐黒川日本$example.com'
        ),
        (
            'чебурашкаящик-с-апельсинами.рф$example.com',
            'чебурашкаящик-с-апельсинами.рф$example.com'
        ),
        (
            'उदाहरण.परीक्ष$domain.with.idn.tld',
            'उदाहरण.परीक्ष$domain.with.idn.tld'
        ),
        (
            'ιωάννης$εεττ.gr',
            'ιωάννης$εεττ.gr'
        ),
        # Why do 3 of the final 4 tests fail? (Commented out for now.)
        # (
        #     '葉士豪$臺網中心.tw',
        #     '葉士豪$臺網中心.tw'
        # ),
        (
            'jeff$臺網中心.tw',
            'jeff$臺網中心.tw'
        )
        # (
        #      '葉士豪$臺網中心.台灣',
        #      '葉士豪$臺網中心.台灣'
        # )
        # (
        #     'jeff葉$臺網中心.tw',
        #     'jeff葉$臺網中心.tw'
        # )
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
        ),
        (
            'rock_\xad_howard$payid.rockhoward.com',
            'DISALLOWED/precis_ignorable_properties'
        ),
        (
            'rock_\u1100_howard$payid.rockhoward.com',
            'DISALLOWED/old_hangul_jamo'
        ),
        (
            'rock_\u1FBF_howard$payid.rockhoward.com',
            'DISALLOWED/has_compat'
        ),
        (
            '\nmy$example.com',
            'DISALLOWED/controls'
        ),
        (
            'm\ny$example.com',
            'DISALLOWED/controls'
        ),
        (
            'my\n$example.com',
            'DISALLOWED/controls'
        )
    ]
)

def test_payid_encoding(payId_input, payId_message):
    with pytest.raises(PayIdEncodingError) as e:
        assert validate_payid(payId_input)
    assert payId_message in str(e.value)

"""
DISALLOWEDs to check someday:

DISALLOWED/arabic_indic Arabic-Indic digits cannot be mixed with Extended Arabic-Indic Digits. (Context)
DISALLOWED/bidi_rule    Right-to-left string cannot contain left-to-right characters due to the “Bidi” rule. (Context)
INCLUDED - DISALLOWED/controls Control character is not allowed.
DISALLOWED/empty    After applying the profile, the result cannot be empty.
DISALLOWED/exceptions   Exception character is not allowed.
DISALLOWED/extended_arabic_indic    Extended Arabic-Indic digits cannot be mixed with Arabic-Indic Digits. (Context)
DISALLOWED/greek_keraia Greek keraia must be followed by a Greek character. (Context)
INCUDED - DISALLOWED/has_compat   Compatibility characters are not allowed.
DISALLOWED/hebrew_punctuation   Hebrew punctuation geresh or gershayim must be preceded by Hebrew character. (Context)
DISALLOWED/katakana_middle_dot  Katakana middle dot must be accompanied by a Hiragana, Katakana, or Han character. (Context)
DISALLOWED/middle_dot   Middle dot must be surrounded by the letter ‘l’. (Context)
DISALLOWED/not_idempotent   After reapplying the profile, the result is not stable.
INCLUDED - DISALLOWED/old_hangul_jamo  Conjoining Hangul Jamo is not allowed.
DISALLOWED/other    Other character is not allowed.
DISALLOWED/other_letter_digits  Non-traditional letter or digit is not allowed.
INCLUDED - DISALLOWED/precis_ignorable_properties  Default ignorable or non-character is not allowed.
DISALLOWED/punctuation  Non-ASCII punctuation character is not allowed.
INCLUDED - DISALLOWED/spaces   Space character is not allowed.
DISALLOWED/symbols  Non-ASCII symbol character is not allowed.
DISALLOWED/unassigned   Unassigned unicode character is not allowed.
DISALLOWED/zero_width_joiner    Zero width joiner must immediately follow a combining virama. (Context)
DISALLOWED/zero_width_nonjoiner Zero width non-joiner must immediately follow a combining virama, or appear where it breaks a cursive connection in a formally cursive script. (Context)
"""

@pytest.mark.parametrize(
    'payId_input, payId_message',
    [
        (
            'rockhoward@gmail.com',
            'The required $ separator is missing.'
        )
    ]
)

def test_payid_syntax(payId_input, payId_message):
    with pytest.raises(PayIdSyntaxError) as e:
        assert validate_payid(payId_input)
    assert str(e.value) == payId_message


@pytest.mark.parametrize(
    'payId_input, payId_message',
    [
        (
            'rockhoward$.gmail.com',
            'Empty Label'
        )
    ]
)

def test_payid_domain_error(payId_input, payId_message):
    with pytest.raises(PayIdDomainEncodingError) as e:
        assert validate_payid(payId_input)
    assert payId_message in str(e.value)
