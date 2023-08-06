django-submail
===============

An easy django email backend to send email using `Submail <http://submail.cn>`_'s python `Mail API <http://submail.cn/chs/documents/developer/64xuB4>`_.

Requirements
------------

Django >= 1.8. Django with other versions are not tested.

Installation
------------

Install the backend from PyPI:

.. code:: bash

    pip install django-submail

Add the following lines to your project's ``settings.py`` or your local settings:

.. code:: python

    EMAIL_BACKEND = "smbackend.SubmailBackend"
    SUBMAIL_APP_ID = "Your Submail APPID"
    SUBMAIL_APP_KEY = "Your Submail APPKey"


Usage
-------

If you use ``send_mail`` method, you can simply do it by, for example:

.. code:: python

    from django.core.mail import send_mail

    send_mail(
        "Your Subject",
        "This is a pure text email body.",
        "Dong Zhuang <hello@foo.com>",
        ["dongzhuang@bar.com"]
        )

If you want to use the ``EmailMessage`` class, then:

.. code:: python

    from django.core.mail import EmailMessage

    mail = EmailMultiAlternatives(
        subject="Your Subject",
        body="This is a pure text email body.",
        from_email="Dong Zhuang <hello@example.com>",
        to=["dongzhuang@foo.com"],
        headers={"Reply-To": "dongzhuang@bar.com"}
        )

    mail.send()

If you want to use the ``EmailMultiAlternatives`` class, then:

.. code:: python

    from django.core.mail import EmailMultiAlternatives

    mail = EmailMultiAlternatives(
        subject="Your Subject",
        body="This is a pure text email body.",
        from_email="Dong Zhuang <hello@example.com>",
        to=["dongzhuang@foo.com"],
        headers={"Reply-To": "dongzhuang@bar.com"}
        )

    mail.attach_alternative(
        "<p>This is an HTML email body</p>", "text/html")

    mail.send()

Sometimes you need to send some other emails using APPID other than the default SUBMAIL_APP_ID
set in ``settings.py``, you can add ``SUBMAIL_APP_ID`` and ``SUBMAIL_APP_KEY`` keys in 
headers, for example:

.. code:: python

    from django.core.mail import EmailMultiAlternatives

    mail = EmailMultiAlternatives(
      subject="Your Subject",
      body="This is a simple text email body.",
      from_email="Dong Zhuang <hello@example.com>",
      to=["dongzhuang@foo.com"],
      headers={
        "Reply-To": "dongzhuang@bar.com",
        "SUBMAIL_APP_ID": settings.ANOTHER_APP_ID,
        "SUBMAIL_APP_KEY": settings.ANOTHER_APP_KEY}
    )

    mail.attach_alternative("<p>This is an HTML email body</p>", "text/html")

    mail.send()

DEMO
----
A demo is included in the repository, you can clone the git and run it locally.

You can optionally run the demo using ``virtualenv``.

.. code:: bash

    pip install virtualenv
    virtualenv venv
    venv/scripts/activate

Then

.. code:: bash

    pip install django
    pip install django-submail
    git clone https://github.com/dzhuang/django-submail.git
    cd django-submail/demo
    python manage.py migrate

Make a copy of example local settings:

.. code:: bash

    cd demo
    cp settings_local.py.example settings_local.py
    vi settings_local.py

Edit params in ``settings_local.py`` according to your own
submail app, and edit ``demo/test_smbackend/views.py`` if 
necessary, then run the dev server:

.. code:: bash

    cd ..
    python manage.py runserver

and visit http://127.0.0.1:8000 to see the result.


TODOs
-----
- Support Submail's mail/xsend API
- Support Submail's addressbook


LICENSE
-------

The MIT License.


Contribution
------------           
Django-submail is wholly open source and welcomes contributions of any kind. Feel
free to either extend it, report bugs, or provide suggestions for improvements.
The author of can be contacted at dzhuang.scut@gmail.com.


