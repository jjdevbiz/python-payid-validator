# python-payid-validator

A python-based validator for the emerging PayId URI standard.

This version targets version 1.0 of the PayId standard.

Add links to the spec here.

### Caveats

The first version of this validator is handling just the basics. This means:

- No characters beyond ascii are allowed.
- No DNS checking is done.
- Some other advanced features are missing.

These limitations will be addressed over time.

### Options

The first version supports these options:

- ignore_case (default: False)
- check_domain (default: True)

If validation is successful, the function returns the valid PayId. It will always be lower case only.

If 'ignore_case' is True, then the returned PayId string may not match the submitted one if any characters were changed to lower case as part of the validation process.

If 'check_domain' is False then the domain portion of the PayId is not checked. This can save time in situations where your code is always using the same domain every time that you invoke the validator.

All validation failures should result in thrown exceptions.

```
class PayIdSyntaxError(PayIdNotValidError):
    """Exception raised when a payId fails validation because of its' form."""
```

```
class PayIdUnusableError(PayIdNotValidError):
    """Exception raised when a payId fails validation because its' domain name does not appear usable."""
```

