# python-payid-validator

A python-based validator for the emerging PayId URI standard.

This version targets version 1.0 of the PayId standard. This includes:

- URI spec: [RFCS draftfuelling-payid-uri-01](https://github.com/payid-org/rfcs/blob/master/dist/spec/payid-uri.txt)
- Whitepaper [PayID Protocol](https://payid.org/whitepaper.pdf)

### Caveats

This second alpha version of this validator is still pretty basic. This means:

- No DNS checking is done.
- Some required syntax checks may be missing.
- While support for i18n is now onboard, there are no unit tests for it yet.

### Options

The current version (0.2) of the validate_payid function supports one option:

- check_domain (default: True)

If validation is successful, the function returns a ValidatedPayId object.

You can access in one of two ways shown by the following example code:
```
    valid_payid_obj = validate_payid(raw_payid)
    validated_payid = str(valid_payid_obj)
    validated_payid = valid_payid_obj.payId
```

The result does not include the 'payid:' prefix whether or not the input raw_payid included it.
(In other words it is OK to not include 'payid:' as the prefix of your raw payid, but if you do, no problem.)

If you want to get the full uri (i.e., include the leading 'payid:' prefix), use:

```
    validated_payid_uri = validate_payid(raw_payid).as_uri())
```

If 'check_domain' is False then the domain portion of the PayId is not checked.
This can save time if you are only using a well-known domain.

All validation failures should result in thrown exceptions.

```
class PayIdEncodingError(PayIdNotValidError):
    """Exception raised due to a unicode error or whitespace or such."""

class PayIdSyntaxError(PayIdNotValidError):
    """Exception raised when a payId fails validation because of its' form."""

class PayIdUnusableError(PayIdNotValidError):
    """Exception raised when a payId fails validation because its' domain name does not appear usable."""
```
