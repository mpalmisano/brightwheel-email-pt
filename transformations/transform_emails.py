import html2text


def convert_email_body_to_plain_text(args):
    """
    Strips the body arg of HTML and returns the args back with the modified body.
    :param args: The dictionary of email field arguments. Includes a body field that may contain html.
    :type args: dict
    :return: str
    """
    plain_text_args = args.copy()
    plain_text_args['body'] = html2text.html2text(args['body'])
    return plain_text_args
