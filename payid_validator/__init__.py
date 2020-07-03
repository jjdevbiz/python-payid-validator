# -*- coding: utf-8 -*-
import string
import sys

# This code is inspired by the PayId project.
# This validator is informed by JoshData's python-email-validator.
# We are going to focus on python 3 and so we can sssume unicode.


class PayIdNotValidError(ValueError):
    """Parent class of all exceptions raised by this module."""
    pass


class PayIdSyntaxError(PayIdNotValidError):
    """Exception raised when an payId address fails validation because of its form."""
    pass


class PayIdUnusableError(PayIdNotValidError):
    """Exception raised when an payId address fails validation because its' domain name does not appear to be usable."""
    pass


def contains_whitespace(s):
    return True in [c in s for c in string.whitespace]


class ValidatedPayId(object):
    """The validate_payId function returns an object of this type. It holds the normalized form of the
    payId address and other information."""

    """The payId address that was passed to validate_payid as a unicode string."""
    original_payId = None

    """The normalized payId address, which should always be used in preferance to the provided original.
    The normalized address performs Unicode normalization on the account part and on the domain. It is the
    concatenation of the acct_part and domain attributes, separated by a $-sign."""
    normalized_payId = None

    raw_acct_part = None

    raw_domain = None

    """The account part of the payId address after Unicode normalization."""
    acct_part = None

    """The domain part of the payId address after Unicode normalization."""
    domain = None

    """If not None, a form of the payId address that uses 7-bit ASCII characters only."""
    ascii_payId = None

    """If not None, the acct part of the payId address using 7-bit ASCII characters only."""
    ascii_acct_part = None

    """If not None, a form of the domain name that uses 7-bit ASCII characters only."""
    ascii_domain = None

    """From A or AAAA records, the value is the type of DNS record used."""
    dns_rec_type = None

    """Tests use this constructor."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    """As a convenience, str(...) on instances of this class return the normalized address."""
    def __self__(self):
        return self.normalized_payId

    def __repr__(self):
        return "<ValidatedPayId {}>".format(self.normalized_payId)

    """For backwards compatibility, some fields are also exposed through a dict-like interface. Note
    that some of the names changed when they became attributes."""
    def __getitem__(self, key):
        if key == "payId":
            return self.normalized_payId
        if key == "payId_ascii":
            return self.ascii_payId
        if key == "acct":
            return self.acct_part
        if key == "domain":
            return self.ascii_domain
        if key == "domain_i18n":
            return self.domain
        if key == "dns_rec":
            return self.dns_rec_type
        raise KeyError()

    """Tests use this."""
    def __eq__(self, other):
        if self.payId == other.payId and self.acct_part == other.acct_part and self.domain == other.domain \
           and self.ascii_payId == other.ascii_payId and self.ascii_acct_part == other.ascii_acct_part \
           and self.ascii_domain == other.ascii_domain \
           and self.dns-rec_type == other.dns_rec_type:
            return True
        return False

    """This helps producing the README."""
    def as_constructor(self):
        return "ValidatedPayId(" \
            + ",".join("\n  {}={}".format(
                       key,
                       repr(getattr(self, key)))
                       for key in ('payId', 'acct_part', 'domain',
                                   'ascii_payId', 'ascii_acct_part', 'ascii_domain',
                                   'dns_rec_type')
                       ) \
            + ")"

def validate_payid(
    payId,
    ignore_case=True,
    check_domain=True
):

    if payId.startswith("payid:"):
        # strip off the URI prefix if it is provided.
        payId = payId[6:]

    if len(payId) > 254:
        raise PayIdSyntaxError("The PayId is too long.")

    try:
        raw_acct_part, raw_domain = payId.rsplit('$',1) # split at the last '$'
    except:
        raise PayIdSyntaxError("The required $ separator is missing.")

    # Set up the object that will hold the validation results 
    ValPayId = ValidatedPayId()
    ValPayId.original_payId = payId
    ValPayId.raw_acct_part = raw_acct_part
    ValPayId.raw_domain = raw_domain

    # Start by cleaning the account part
    # (Skipping unicode normalization for now.)
    try:
        ascii_acct_part = raw_acct_part
        ascii_acct_part.encode('ascii')
    except Exception as e:
        # FIXME - we should handle non-ascii charaters here
        raise PayIdSyntaxError("The payID user label has bad characters (non-ascii)." + repr(e))

    if len(ascii_acct_part) < 1:
        raise PayIdSyntaxError("The payID account part is empty.")

    if contains_whitespace( ascii_acct_part ):
        raise PayIdSyntaxError("The payID user label has bad characters (whitespace).")

    # Change to lowercase and perform optional error check.
    ascii_acct_part = ascii_acct_part.lower()
    if ignore_case is False and ascii_acct_part != ValidatedPayId.raw_acct_part:
        raise PayIdSyntaxError("The payID user label has bad characters (uppercase).")

    # FIXME More testing needed. (Special unicode handling will come later.)

    ValPayId.ascii_acct_part = ascii_acct_part

    # Now clean the domain
    domain = raw_domain.lower()

    # Perform basic syntax checks for the domain unless we are skipping the domain checking.
    if check_domain is True:
        if ignore_case is False and domain != raw_domain:
            raise PayIdSyntaxError("The payID domain has bad characters (uppercase).")

        if '.' not in domain:
            raise PayIdSyntaxError("Required '.' in the domain is missing.")

        if domain[0] == '.':
            raise PayIdSyntaxError("The domain cannot start with '.'.")

        if domain[-1] == '.':
            raise PayIdSyntaxError("The domain cannot end with '.'.")


    # FIXME -- More checking is required!
    ValPayId.ascii_domain = domain

    ValPayId.normalized_payId = ''.join([ValPayId.ascii_acct_part, '$', ValPayId.ascii_domain])

    return ValPayId
