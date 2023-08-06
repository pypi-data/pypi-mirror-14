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

from django.conf import settings

from email.header import Header
from email.utils import parseaddr

from django.utils.encoding import force_text

def split_addr_name(addr, encoding):
    if not isinstance(addr, tuple):
        addr = parseaddr(force_text(addr))
    nm, addr = addr
    nm = Header(nm, encoding).encode()
    try:
        addr.encode('ascii')
    except UnicodeEncodeError:  # IDN
        if '@' in addr:
            localpart, domain = addr.split('@', 1)
            localpart = str(Header(localpart, encoding))
            domain = domain.encode('idna').decode('ascii')
            addr = '@'.join([localpart, domain])
        else:
            addr = Header(addr, encoding).encode()
    return addr, nm

def make_config(email):
    """
    Make config from headers or settings.py
    """
    appid = None
    appkey = None
    if email.extra_headers:
        if "SUBMAIL_APP_KEY" in email.extra_headers:
            appkey = email.extra_headers["SUBMAIL_APP_KEY"]
        if "SUBMAIL_APP_ID" in email.extra_headers:
            appid = email.extra_headers["SUBMAIL_APP_ID"]
    if appkey is None:
        appkey = getattr(settings, "SUBMAIL_APP_KEY", None)
    if appid is None:
        appid = getattr(settings, "SUBMAIL_APP_ID", None)
    sign_type = getattr(settings, "SUBMAIL_SIGN_TYPE", "normal")

    config = {}
    if appid and appkey:
        config['appid'] = appid
        config['appkey'] = appkey
        config['sign_type'] = sign_type
    else:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "Both SUBMAIL_APP_ID and SUBMAIL_APP_KEY must be "
            "declared in settings.py or in your EmailMessage headers.")
    return config
