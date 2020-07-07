# -*- coding: utf-8 -*-
import string
import sys
import idna
from precis_i18n import get_profile


acct_part_profile = get_profile('UsernameCaseMapped')  # Used for precis 8264 checking.

# This code is inspired by the PayId project.
# This validator is informed by JoshData's python-email-validator.
# We are going to focus on python 3 and so we can assume unicode.

# Here are the guiding concepts from payid-org/rfcs/payid-uri.txt on github:
#
#    o  The 'acctpart' consists only of Unicode code points that conform
#       to the PRECIS IdentifierClass specified in [RFC8264]. (DONE - needs more testing)
#
#    o  The 'host' consists only of Unicode code points that conform to [RFC5892]. (FIXME)
#
#    o  Internationalized domain name (IDN) labels are encoded as A-labels [RFC5890]. (FIXME)
#

class PayIdNotValidError(ValueError):
    """Parent class of all exceptions raised by this module."""
    pass


class PayIdEncodingError(PayIdNotValidError):
    """Exception raised due to a unicode error or whitespace or such."""
    pass


class PayIdSyntaxError(PayIdNotValidError):
    """Exception raised when an payId address fails validation because of its form."""
    pass


class PayIdDomainEncodingError(PayIdNotValidError):
    """Exception raised when an payId address fails validation because of its form."""
    pass

class PayIdUnusableError(PayIdNotValidError):
    """Exception raised when an payId address fails validation because its' domain name does not appear to be usable."""
    pass


def contains_whitespace(s):
    return True in [c in s for c in string.whitespace]


class ValidatedPayId(object):
    """The validate_payId function returns an object of this type.
       It holds the normalized form of the payId address and other information."""
    # The Unicode normalization is coming soon. For now we only handle pure ascii payIds.

    """The payId address that was passed to validate_payid as a unicode string."""
    original_payId = None

    """This finalized payId should always be used in preference to the provided original.
    It is the concatenation of the acct_part and domain attributes connected by a $-sign."""
    payId = None

    """ The unchanged account part of the payId directly from the original_payId."""
    raw_acct_part = None

    """ The unchanged domain part of the payId directly from the original_payId."""
    raw_domain = None

    """The finslized account part of the payId address after Unicode normalization."""
    # For now this is just a copy of the ascii version. Unicode normalization is pending.
    acct_part = None

    """The finalized domain part of the payId address after Unicode normalization."""
    # For now this is just a copy of the ascii version. Unicode normalization is pending.
    domain = None

    """If not None, a form of the payId address that uses 7-bit ASCII characters only."""
    ascii_payId = None

    """If not None, the acct part of the payId address using 7-bit ASCII characters only."""
    ascii_acct_part = None

    """If not None, a form of the domain name that uses 7-bit ASCII characters only."""
    ascii_domain = None

    """From A or AAAA records, the value is the type of DNS record used."""
    # Ignore this as DNS is not being checked yet.
    dns_rec_type = None

    """Tests use this constructor."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    """As a convenience, str(...) on instances of this class return the normalized payId."""
    def __str__(self):
        return self.payId

    def __repr__(self):
        return "<ValidatedPayId {}>".format(self.payId)

    def as_uri(self):
        return "payid:{}".format(self.payId)

    """For backwards compatibility, some fields are also exposed through a dict-like interface. Note
    that some of the names changed when they became attributes."""
    def __getitem__(self, key):
        if key == "payId":
            return self.payId
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
           and self.ascii_payId == other.ascii_payId \
           and self.ascii_acct_part == other.ascii_acct_part and self.ascii_domain == other.ascii_domain \
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
    # We use the precis_i18n package to do this.
    # 
    try:
        acct_part = acct_part_profile.enforce(raw_acct_part)
    except UnicodeEncodeError as e:
        raise PayIdEncodingError("Unicode Error: " + repr(e))
    ValPayId.acct_part = acct_part

    # Not sure we need to mess with the ascii version, but the email package that I copied
    # is doing this and so we include this as well for now.
    #
    try:
        ascii_acct_part = acct_part
        ascii_acct_part.encode('ascii')
    except Exception as e:
        # ascii encoding failed
        ascii_acct_part = None
    ValPayId.ascii_acct_part = ascii_acct_part


    # Now clean the domain host
    # FIXME -- It is time to rework this for proper domain host checking.
    #
    try:
        idna_encoded_domain = idna.encode(raw_domain)
        domain = idna_encoded_domain.decode('idna')
        domain_utf8 = domain.encode('utf-8')
    except idna.IDNAError as e:
        raise PayIdDomainEncodingError("Domain Error: " + repr(e))

    """
    # domain = raw_domain.lower()

    # Perform basic syntax checks for the domain unless we are skipping the domain checking.
    if check_domain is True:
        if domain != raw_domain:
            raise PayIdSyntaxError("The payID domain has bad characters (uppercase).")

        if '.' not in domain:
            raise PayIdSyntaxError("Required '.' in the domain is missing.")

        if domain[0] == '.':
            raise PayIdSyntaxError("The payId domain cannot start with '.'.")

        if contains_whitespace( domain ):
            raise PayIdSyntaxError("The payID domain has bad characters (whitespace).")
    """

    # FIXME -- Add domain DNS checking for A or AAAA records.

    ValPayId.domain = domain

    # For cleanliness we are enforcing lowercase domain if the domain is ascii.
    #
    try:
        ascii_domain = domain
        ascii_domain.encode('ascii')
        ascii_domain = ascii_domain.lower()
    except Exception as e:
        # ascii encoding failed
        ascii_domain = None
    ValPayId.ascii_domain = ascii_domain

    # Finally assemble the final cleaned PayId.
    #
    if ValPayId.ascii_domain is not None:
        ValPayId.payId = ''.join([ValPayId.acct_part, '$', ValPayId.ascii_domain])
    else:
        ValPayId.payId = ''.join([ValPayId.acct_part, '$', ValPayId.domain])

    return ValPayId
