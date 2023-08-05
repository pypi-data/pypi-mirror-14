#!/usr/bin/env python
# coding=utf-8

__version__ = "1.0.9"

import logging
import datetime
import functools
import re
import types
import urlparse

#: logging handler
_logger = logging.getLogger("pyfiltration")

__all__ = ["FiltrationException", "Item", "filtration", "Helper"]


class _ObjectDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


class FiltrationException(Exception):
    def __init__(self, message, error=None):
        super(FiltrationException, self).__init__(message)
        self.error = error


def filtration(arg_key):
    """ filter request params

    :param string arg_key: self.get_validation_args() arg_key
    """

    def _filtration(method):
        @functools.wraps(method)
        def _wrapper(self, *args, **kwargs):
            assert getattr(self, "get_validation_args", None)

            all_params = self.get_validation_args()
            fparams = _Filtration(all_params[arg_key], self).parse()
            kwargs["fparams"] = fparams
            return method(self, *args, **kwargs)
        return _wrapper
    return _filtration


class _Filtration(object):
    def __init__(self, items, request):

        self.items = items
        self.request = request
        assert getattr(self.request, "request", None)

        self.request_arguments = self.request.request.arguments

    def get_request_detail(self):
        f_module = self.request.request.__class__.__module__
        f_class = self.request.request.__class__.__name__
        method = self.request.request.method
        return u"<{f_module}.{f_class}>({method})".format(
            f_module=f_module, f_class=f_class, method=method)

    def parse(self):
        args = _ObjectDict()
        for item in self.items:
            assert isinstance(item, Item)

            #: required check
            if item.required and not self.is_exist_item_name(item.name):
                raise FiltrationException(u"{} {}: required".format(self.get_request_detail(), item.name), item.err_message)

            if not item.required and not self.is_exist_item_name(item.name):
                args[item.dest] = item.default
            else:
                args[item.dest] = self._parse_item(item, self.get_argument(item.name))
        return args

    def get_argument(self, name):
        return self.request.get_argument(name)

    def is_exist_item_name(self, name):
        return name in self.request_arguments

    def convert_data_type(self, item, value):
        try:
            if item.type_ == int:
                return int(value)
            elif item.type_ == str:
                return value
            raise FiltrationException(u"{} {}: type({}) not support".format(
                self.get_request_detail(), item.name, item.type_), item.err_message)
        except:
            raise FiltrationException(u"{} {}: type error({} required)".format(
                self.get_request_detail(), item.name, item.type_), item.err_message)

    def _parse_item(self, item, value):
        value = self.convert_data_type(item, value)

        for funcs in item.validates:
            try:
                if funcs.args:
                    result = funcs.func(value, **funcs.args)
                else:
                    result = funcs.func(value)
            except Exception as e:
                raise FiltrationException(u"{} {}: validate failed: {}({}) {}".format(
                    self.get_request_detail(), item.name, funcs.f_, value, e), funcs.err_message)

            if not result:
                raise FiltrationException(u"{} {}: validate failed: {}({})".format(
                    self.get_request_detail(), item.name, funcs.f_, value), funcs.err_message)

        for funcs in item.uses:
            try:
                if funcs.args:
                    value = funcs.func(value, **funcs.args)
                else:
                    value = funcs.func(value)

            except Exception as e:
                raise FiltrationException(u"{} {}: uses failed: {}({}) {}".format(
                    self.get_request_detail(), item.name, funcs.f_, value, e), funcs.err_message)
        return value


class Item(object):
    def __init__(self, name, type_, validates=None, default=None, required=True, dest=None, uses=None, err_message=None):
        self.name = name
        self.type_ = type_

        self.validates = []
        if validates:
            if not isinstance(validates, types.ListType):
                validates = [validates]
            for funcs in validates:
                self.validates.append(self.get_func_details(funcs))

        self.uses = []
        if uses:
            if not isinstance(uses, types.ListType):
                uses = [uses]
            for funcs in uses:
                self.uses.append(self.get_func_details(funcs))

        self.default = default
        self.required = required
        self.dest = dest
        if self.dest is None:
            self.dest = self.name
        self.err_message = err_message

    def get_func_details(self, funcs):
        assert isinstance(funcs, types.TupleType)
        assert (isinstance(funcs[0], types.FunctionType)
                or isinstance(funcs[0], types.LambdaType)
                or isinstance(funcs[0], types.MethodType))
        f_name = funcs[0].__name__
        f_module = funcs[0].__class__.__module__
        f_class = funcs[0].__class__.__name__
        args = None
        err_message = None
        if len(funcs) > 1 and isinstance(funcs[1], types.DictType):
            args = funcs[1]
        if len(funcs) == 3:
            err_message = funcs[2]
        return _ObjectDict(
            func=funcs[0],
            args=args,
            err_message=err_message,
            f_=u"<{f_module}.{f_class}.{f_name}>({args})".format(
                f_module=f_module, f_class=f_class, f_name=f_name, args=args))


class Helper(object):
    EMAIL_ADDRESS_REG = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*")'
        r'@(?:[A-Z0-9](?:[A-Z0-9-]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))$',
        re.IGNORECASE
    )
    EMAIL_ADDRESS_SUFFIX_REG = re.compile(
        r'^@(?:[A-Z0-9](?:[A-Z0-9-]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))$',
        re.IGNORECASE
    )
    URL_ADDRESS_REG = re.compile(
        r"^(https?|ftp):\/\/"  # http:// or https:// or ftp://
        r"(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?"  # domain
        r"(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|"  # ip
        r"((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|"
        r"(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])"
        r"([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*"
        r"([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+"
        r"(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|"
        r"(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])"
        r"([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*"
        r"([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)"
        r"(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+"
        r"(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?"
        r"(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|"
        r"[!\$&'\(\)\*\+,;=]|:|@)|"
        r"[\uE000-\uF8FF]|\/|\?)*)?"
        r"(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|"
        r"(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$"
    )
    STRING_HAS_NUMBER = 1
    STRING_HAS_LETTER = 2

    @classmethod
    def is_valid_email_address(cls, email):
        return cls.EMAIL_ADDRESS_REG.search(email) is not None

    @classmethod
    def is_valid_email_address_suffix(cls, suffix):
        return cls.EMAIL_ADDRESS_SUFFIX_REG.search(suffix) is not None

    @classmethod
    def is_valid_string(cls, val, exists=None):
        if not exists:
            return bool(val)
        for cond in set(exists):
            if cond == cls.STRING_HAS_NUMBER and re.search(r"\d", val) is None:
                return False
            elif cond == cls.STRING_HAS_LETTER and re.search(r"[a-zA-Z]", val) is None:
                return False
        return True

    @classmethod
    def is_included(cls, val, vals=None):
        assert vals
        return val in vals

    @classmethod
    def get_value(cls, val, vals=None):
        assert vals
        return vals[val]

    @classmethod
    def is_valid_random_token(cls, val, length=32):
        return re.match(r"^([0-9a-z]){" + "{}".format(length) + "}$", val) is not None

    @classmethod
    def is_valid_telephone(cls, val):
        return re.match(r"^1[3,4,5,7,8]{1}[0-9]{9}$", val) is not None

    @classmethod
    def is_valid_datetime(cls, val, formats=None):
        try:
            datetime.datetime.strptime(val, formats)
            return True
        except ValueError:
            return False

    @classmethod
    def is_excluded_special_char(cls, val):
        return re.match(r"([`~!@$^&*()=|{}'·:;',\\\[\]<>/?~！@￥……&*（）——|{}【】‘；：”“'。，、？]){1,}", val) is None

    @classmethod
    def is_valid_password(cls, val, min_length=6, max_length=16):
        password_length = len(val)
        return val and password_length >= 6 and password_length <= 16

    @classmethod
    def is_valid_url(cls, val, domains=None):
        if not domains:
            domains = ["http", "https"]

        assert isinstance(domains, types.TupleType) or isinstance(domains, types.ListType)

        pieces = urlparse.urlparse(val)
        return (all([pieces.scheme, pieces.netloc]) and pieces.scheme in domains)

    @classmethod
    def is_valid_base64_string(cls, val):
        return ((len(val) % 4 == 0) and re.match('^[A-Za-z0-9+/]+[=]{0,2}$', val) is not None)

    @classmethod
    def get_timestamp_from_timestr(cls, val, formats):
        import datetime
        import time
        return time.mktime(datetime.datetime.strptime(val, formats).timetuple())
