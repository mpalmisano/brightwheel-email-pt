import re


def is_valid_email_address(email_address):
    """
    Validates an email address string to ensure it is a valid email address.
    :param email_address: A string representing an email address.
    :type email_address: str
    :return: bool
    """
    if re.fullmatch(r'.+@.+\..+', email_address):
        return True
    else:
        return False


def is_valid_email_payload(args):
    """
    Validates the email arguments to ensure they are valid to send via the email service providers.
    :param args: The dictionary of email field arguments.
    :type args: dict
    :return: bool
    """
    # Validate our email address fields to ensure they are valid emails
    email_address_fields = ['to', 'from']
    for field in email_address_fields:
        if not is_valid_email_address(args[field]):
            return False
    return True
