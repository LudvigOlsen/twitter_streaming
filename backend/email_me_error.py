"""
Sends an error message via email.

"""

import smtplib

from backend.error_messages import SPECIFIC_MSG

__all__ = ["email_me_error"]


def email_me_error(mail_connection, status_code, custom_msg=None):
    """Sends specific error codes with (optionally) custom messages"""

    if not mail_connection:
        raise ValueError("mail_connection is None. Cannot send email.")

    server = smtplib.SMTP(mail_connection['smtp'])
    server.ehlo()
    server.starttls()
    server.login(mail_connection["from"], mail_connection["password"])

    msg = "\r\n".join([
        "From: {}".format(mail_connection["from"]),
        "To: {}".format(mail_connection["to"]),
        "Subject: Tweepy streaming error occured",
        "",
        "The twitter stream received a {} error and disconnected!{}".format(status_code, SPECIFIC_MSG[status_code])])

    # If we passed along a custom message,
    # e.g. an exception message,
    # Add it to the mail
    if custom_msg is not None:
        msg = "\r\n".join([msg, custom_msg])

    server.sendmail(mail_connection["from"], mail_connection["to"], msg)
    server.quit()
