# -*- coding: utf-8 -*-

from __future__ import division

__copyright__ = """
Copyright (c) 2015-2016 Dong Zhuang (dzhuang.scut@gmail.com)
"""

__license__ = """
The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the 
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the 
following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMultiAlternatives
from email.utils import parseaddr

from .submail.mail_send import MAILSend

from .utils import split_addr_name, make_config


class SubmailBackend(BaseEmailBackend):
    '''
    Django submail mail/send Backend
    '''

    def open(self):
        pass

    def close(self):
        pass

    def send_messages(self, emails):
        if not emails:
            return

        result = []
        for email in emails:
            mail = build_sm_mail(email)
            result.append(mail.send())
        return result


def build_sm_mail(email):
    """
    Convert django email class to submail.MAILSend class
    """
    mail = MAILSend(make_config(email))

    from_addr, from_name = split_addr_name(
        email.from_email, email.encoding)
    mail.set_sender(from_addr, from_name)

    for send_to in email.to:
        to_addr, to_name = split_addr_name(send_to, email.encoding)
        mail.add_to(to_addr, to_name)

    for send_cc in email.cc:
        cc_addr, cc_name = split_addr_name(send_cc, email.encoding)
        mail.add_cc(cc_addr, cc_name)

    for bcc in email.bcc:
        bcc_addr, bcc_name = split_addr_name(bcc, email.encoding)
        mail.add_bcc(bcc_addr, bcc_name)

    if email.reply_to:
        mail.set_reply(parseaddr(email.reply_to)[1])
    elif email.extra_headers:
        if "Reply-To" in email.extra_headers:
            mail.set_reply(parseaddr(email.extra_headers["Reply-To"])[1])

    mail.set_text(email.body)
    mail.set_subject(email.subject)

    if isinstance(email, EmailMultiAlternatives):
        for alt in email.alternatives:
            if alt[1] == "text/html":
                mail.set_html(alt[0])

    for attachment in email.attachments:
        mail.add_attachment(attachment)

    return mail
