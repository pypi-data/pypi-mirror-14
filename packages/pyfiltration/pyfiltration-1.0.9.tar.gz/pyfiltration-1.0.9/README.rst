Pyfiltration
============

Pyfiltration tornado filtration

You can install Pyfiltration from PyPI with

.. sourcecode:: bash

    $ pip install pyfiltration


Version update
--------------

- 1.0.6 Bug Year 2000 (Y2K) issues: Values 100–1899 are always illegal
- 1.0.4 raise Exception
- 1.0.1 initialize project


DEMO
----

.. sourcecode:: python

    #!/usr/bin/env python
    # coding=utf-8

    import tornado.web.RequestHandler
    from pyfiltration import Item, Helper, filtration


    class RegisterHandler(tornado.web.RequestHandler):

        def get_validation_args(self):
            return {
                "post": [
                    Item("password", str, validates=[
                        (
                            lambda k: k and len(k) >= 6 and len(k) <= 16, None, {"password": u"请输入6-16位密码，字母区分大小写，包含字母和数字"}),
                        (
                            Helper.is_valid_string,
                            {"exists": [Helper.STRING_HAS_NUMBER, Helper.STRING_HAS_LETTER]},
                            {"password": u"请输入6-16位密码，字母区分大小写，包含字母和数字"}
                        )
                    ]),
                ]
            }

        @filtration("post")
        def post(self, fparams=None):
            pass


API
---

- Helper.is_valid_email_address(email)
- Helper.is_valid_string(val, exists=None)
- Helper.is_included(val, vals=None)
- Helper.is_valid_random_token(val, length=32)
- Helper.is_valid_telephone(val)
- Helper.is_valid_datetime(val, formats=None)
- Helper.is_excluded_special_char(val)
- Helper.is_valid_password(val, min_length=6, max_length=16)
- Helper.is_valid_url(val, domains=None)
- Helper.is_valid_base64_string(val)
- Helper.get_value(val, vals=None)
- Helper.get_timestamp_from_timestr(val, formats):

Support
-------

If you need help using pyfiltration or have found a bug, please open a `github issue`_.

.. _github issue: https://github.com/nashuiliang/pyfiltration/issues
