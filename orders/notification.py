import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_confirmation():
    message = Mail(
        from_email='praveena4e@gmail.com',
        to_emails='pvsrinivasan1201@gmail.com',
        subject='Order Confirmed',
        html_content='<strong>Your Order confirmed</strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)