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
    check_domain=True,
    include_prefix = False
):

    if len(payId) > 254:
        raise PayIdSyntaxError("The PayId is too long.")

    try:
        raw_label, raw_domain_host = payId.rsplit('$',1) # split at the last '$'
    except:
        raise PayIdSyntaxError("The required $ separator is missing.")

    # Start by cleaning the user_label
    user_label = raw_label.lower()
    if user_label.startswith("payid:"):
        user_label = user_label[6:]

    # Perform the basic syntax testing of the user_label
    if ignore_case is False and user_label != raw_label:
        raise PayIdSyntaxError("The payID user label has bad characters (uppercase).")

    if len(user_label) < 1:
        raise PayIdSyntaxError("The payID username is empty.")

    # FIXME More testing needed. (Special unicode handling will come later.)

    # Now clean the domain host
    domain_host = raw_domain_host.lower()

    # Perform basic syntax checks for the domain host unless we are skipping the domain checking.
    if check_domain is True:
        if ignore_case is False and domain_host != raw_domain_host:
            raise PayIdSyntaxError("The payID domain host has bad characters (uppercase).")

        if '.' not in domain_host:
            raise PayIdSyntaxError("Required '.' in the domain is missing.")

        if domain_host[0] == '.':
            raise PayIdSyntaxError("The domain host cannot start with '.'.")

        if domain_host[-1] == '.':
            raise PayIdSyntaxError("The domain host cannot end with '.'.")

    # FIXME -- More checking is required!
    if include_prefix is True:
        results = ["payid:"]
    else:
        results = ['']
    results.append(user_label)
    results.append('$')
    results.append(domain_host)
    return ''.join(results)
