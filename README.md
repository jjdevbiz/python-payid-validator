# python-payid-validator

A python-based validator for the emerging PayId URI standard.

This version targets version 1.0 of the PayId standard. This includes:

- URI spec: [RFCS draftfuelling-payid-uri-01](https://github.com/payid-org/rfcs/blob/master/dist/spec/payid-uri.txt)
- Whitepaper [PayID Protocol](https://payid.org/whitepaper.pdf)

### Caveats

The first version of this validator is handling just the basics. This means:

- No characters other than ascii are allowed.
- No DNS checking is done.
- Some required syntax checks may be missing.

### Options

The current version (0.2) of the validate_payid function supports these options:

- ignore_case (default: True)
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

If 'ignore_case' is True, then the returned PayId string may not match the submitted one if any characters
were changed to lower case as part of the validation process.

If 'check_domain' is False then the domain portion of the PayId is not checked.

All validation failures should result in thrown exceptions.

```
class PayIdSyntaxError(PayIdNotValidError):
    """Exception raised when a payId fails validation because of its' form."""

class PayIdUnusableError(PayIdNotValidError):
    """Exception raised when a payId fails validation because its' domain name does not appear usable."""
```

This version performs a variety of syntax checks but will only work for ascii characters at this time.
Support for the full set of allowed unicode characters will be included in the next release.
