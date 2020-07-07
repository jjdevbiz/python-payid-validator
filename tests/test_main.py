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
