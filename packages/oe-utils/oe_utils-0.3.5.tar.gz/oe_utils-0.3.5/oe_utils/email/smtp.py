# -*- coding: utf-8 -*-
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pyramid.compat import text_


class SMTPClient:
    def __init__(self, smpt, sender):
        '''
            :param smtp: Simple Mail Transfer Protocol (SMTP) to send mails
            :param sender: Sender of the mail
        '''
        self.smtp = smpt
        self.sender = sender

    @property
    def smtp_obj(self):  # pragma no cover
        return smtplib.SMTP(self.smtp)

    def send_mail(self, receivers, subject, message_plain, message_html=None, cc=None, bcc=None):
        '''

        send an email

        :param receivers: Receivers (list)
        :param subject: Email subject
        :param message_plain: Email message (plain text)
        :param message_html: Email message (html version)
        :param cc: carbon copy (list)
        :param bcc: blind carbon copy (list)
        '''
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(subject, "utf-8")
        msg['From'] = Header(text_(self.sender), "utf-8")
        msg['To'] = Header(text_('; '.join(receivers)), "utf-8")
        if cc:
            msg['CC'] = Header(text_('; '.join(cc)), "utf-8")
        if bcc:
            msg['BCC'] = Header(text_('; '.join(bcc)), "utf-8")
        part1 = MIMEText(message_plain, 'plain', _charset="UTF-8")
        part2 = MIMEText(message_html, 'html', _charset="UTF-8")

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        self.smtp_obj.sendmail(self.sender, receivers, msg.as_string())
        self.smtp_obj.quit()
