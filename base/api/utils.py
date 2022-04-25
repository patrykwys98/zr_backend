from django.core.mail import EmailMessage
import re


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()

    @staticmethod
    def is_match(regex, text):
        return re.compile(regex).search(text) is not None
