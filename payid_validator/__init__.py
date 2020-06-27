# -*- coding: utf-8 -*-

import sys

# This code is inspired by the PayId project.
# This validator is informed by JoshData's python-email-validator.


# ease compatibility in type checking
if sys.version_info >= (3,):
    unicode_class = str
else:
    unicode_class = unicode  # noqa: F821


class PayIdNotValidError(ValueError):
    """Parent class of all exceptions raised by this module."""
    pass


class PayIdSyntaxError(PayIdNotValidError):
    """Exception raised when an payId address fails validation because of its form."""
    pass


class PayIdUnusableError(PayIdNotValidError):
    """Exception raised when an payId address fails validation because its' domain name does not appear to be usable."""
    pass


def validate_payid(
    payId,
    ignore_case=True,
    check_domain=True
):

    if len(payId) > 254:
        raise PayIdSyntaxError("The PayId is too long.")

    if '$' not in payId:
        raise PayIdSyntaxError("The required $ separator is missing.")

    raw_label, raw_domain_host = payId.rsplit('$',1)
    if len(raw_label) < 1:
        raise PayIdSyntaxError("The user label is empty.")

    if '.' not in raw_domain_host:
        raise PayIdSyntaxError("Required '.' in the domain is missing.")

    user_label = raw_label.lower()
    if ignore_case is False and user_label != raw_label:
        raise PayIdSyntaxError("The payID user label has bad characters (uppercase).")

    domain_host = raw_domain_host.lower()
    if ignore_case is False and domain_host != raw_domain_host:
        raise PayIdSyntaxError("The payID domain host has bad characters (uppercase).")

    # FIXME -- More checking is required!
 
    return user_label + '$' + domain_host

