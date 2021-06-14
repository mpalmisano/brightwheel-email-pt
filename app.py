import time
from flask import Flask
from flask_restful import Resource, Api, reqparse

from config import REROUTE_TRAFFIC_TO_SNAILGUN, SPENDGRID_API_KEY, SNAILGUN_API_KEY
from email_service_providers.snailgun import SnailgunClient
from email_service_providers.spendgrid import SpendgridClient
from transformations.transform_emails import convert_email_body_to_plain_text
from validations.validate_emails import is_valid_email_payload


# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)


def send_email(args):
    """
    Calls the appropriate email service provider function to send an email.  Defaults to using Spendgrid.
    :param args: The dictionary of email field arguments.
    :type args: dict
    :return: None
    """
    if REROUTE_TRAFFIC_TO_SNAILGUN is True:
        return send_email_via_snailgun(args)
    else:
        # Send to Spendgrid by default
        return send_email_via_spendgrid(args)


def send_email_via_spendgrid(args):
    """
    Sends an email via the Spendgrid service provider API and returns a response.
    :param args: The dictionary of email field arguments.
    :type args: dict
    :return: Response
    """
    # Connect to our spendgrid client
    client = SpendgridClient(api_key=SPENDGRID_API_KEY)

    # Transform the payload
    payload = dict()
    payload['sender'] = f"{args['to_name']} <{args['to']}>"
    payload['recipient'] = f"{args['from_name']} <{args['from']}>"
    payload['subject'] = args['subject']
    payload['body'] = args['body']

    return client.send_email(payload=payload)


def send_email_via_snailgun(args, timeout=1800, interval=10):
    """
    Sends an email via the Snailgun service provider API and returns a response.
    :param args: The dictionary of email field arguments.
    :type args: dict
    :param timeout: The amount of time in seconds to check for a successful email status before timeout.
    :type timeout: int
    :param interval: The amount of time in seconds between email status checks.
    :type interval: int
    :return: Response
    """
    # Connect to our snailgun client
    client = SnailgunClient(api_key=SNAILGUN_API_KEY)

    # Transform the payload
    payload = dict()
    payload['from_email'] = args['from']
    payload['from_name'] = args['from_name']
    payload['to_email'] = args['to']
    payload['to_name'] = args['to_name']
    payload['subject'] = args['subject']
    payload['body'] = args['body']

    response = client.send_email(payload=payload)
    response_body = response.json()
    email_id = response_body['id']

    start = time.time()
    check = start
    while check - start < timeout:
        # Check the email's status
        check_response = client.check_email_status(email_id)
        check_response_body = check_response.json()
        check = time.time()  # Reset the check time

        # If it is still queued then wait and retry
        if check_response_body['status'] == 'queued':
            time.sleep(interval)
            continue

        # We got either a success or a failure status
        return check_response

    # We timed out, return the original response body so this can be checked later
    return Flask.response_class(status=408, response_body=response_body)


class Email(Resource):
    """
    A class defining the Email resource.
    """

    def post(self):
        """
        Accepts POST requests with standard email field arguments to send emails via an external email service
        provider.
        """

        # Parse the arguments
        parser = reqparse.RequestParser()
        parser.add_argument('to', type=str, required=True, help='The email address to send to')
        parser.add_argument('to_name', type=str, required=True, help='The name to accompany the email')
        parser.add_argument('from', type=str, required=True, help='The email address in the from and reply fields')
        parser.add_argument('from_name', type=str, required=True, help='the name to accompany the from/reply emails')
        parser.add_argument('subject', type=str, required=True, help='The subject line of the email')
        parser.add_argument('body', type=str, required=True, help='The HTML body of the email')
        args = parser.parse_args()

        # Run validations on the email data
        if not is_valid_email_payload(args=args):
            return {'message': 'Invalid email payload. Email not sent.', 'data': args}, 400

        # Convert email body
        plain_text_args = convert_email_body_to_plain_text(args=args)

        # Send email
        response = send_email(args=plain_text_args)
        if 200 <= response.status_code <= 299:
            return {'message': 'Email successfully sent.', 'data': response.json()}, response.status_code
        else:
            return {'message': 'Email failed to send.', 'data': response.json()}, response.status_code


api.add_resource(Email, '/email')
