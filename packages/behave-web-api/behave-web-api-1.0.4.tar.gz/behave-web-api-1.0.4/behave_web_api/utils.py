from __future__ import unicode_literals
import os
import re
import requests
from functools import wraps


def make_url(context, endingpoint):
    BASE_URL = dereference_variables(context, '$BASE_URL')
    if 'http' not in BASE_URL:
        BASE_URL = 'http://{}'.format(BASE_URL)

    return '{}{}'.format(BASE_URL, endingpoint)


def dereference_variables(context, value):
    variables = context.variables\
        if hasattr(context, 'variables') else {}

    for key in re.findall('\$+\w+', value):
        var_name = key[1:]
        value = value.replace(
            key,
            variables.get(
                var_name,
                os.environ.get(var_name, key)
            )
        )

    return value


def dereference_arguments(f):
    @wraps(f)
    def wrapper(context, *args, **kwargs):
        new_kwargs = {}
        new_args = []
        for key, value in kwargs.items():
            new_kwargs[key] = dereference_variables(context.text, value)
        for value in args:
            new_args.append(dereference_variables(context.text, value))
        context.text = dereference_variables(context, context.text)\
            if context.text else ''
        return f(context, *new_args, **new_kwargs)
    return wrapper


def compare_lists(expected_list, actual_list, path=None):
    assert type(expected_list) is list,\
        "Expected {} is not a list".format(repr(expected_list))
    assert type(actual_list) is list,\
        "Actual {} is not a list".format(repr(actual_list))

    for i, item in enumerate(expected_list):
        path = '{}.{}'.format(path, i) if path else str(i)
        try:
            actual_value = actual_list[i]
        except ValueError:
            actual_value = None
        compare_values(item, actual_value, path=path)


def compare_dicts(expected_dict, actual_dict, path=None):
    assert type(expected_dict) is dict,\
        "Expected {} is not a dict".format(repr(expected_dict))
    assert type(actual_dict) is dict,\
        "Actual {} is not a dict".format(repr(actual_dict))

    for key in expected_dict:
        expected_value = expected_dict[key]
        actual_value = actual_dict.get(key, None)
        path = '{}.{}'.format(path, key) if path else key

        compare_values(expected_value, actual_value, path=path)


def compare_values(expected_value, actual_value, path=None):
    if type(expected_value) is dict:
        compare_dicts(expected_value, actual_value, path=path)
    elif type(expected_value) is list:
        compare_lists(expected_value, actual_value, path=path)
    elif isinstance(expected_value, basestring)\
            and expected_value[0] == '%'\
            and expected_value[-1] == '%':
        if not re.match(expected_value.strip('%'), actual_value or ''):
            message = 'Expected {} to match regex {}'
            params = [repr(actual_value), repr(expected_value)]

            if path:
                message = message + ' at path {}'
                params.append(path)

            raise AssertionError(message.format(*params))
    else:
        try:
            assert expected_value == actual_value
        except AssertionError:
            message = 'Expected {} to equal {}'
            params = [repr(actual_value), repr(expected_value)]

            if path:
                message = message + ' at path {}'
                params.append(path)

            raise AssertionError(message.format(*params))


def do_request(context, method, endingpoint, body=None):
    fn = getattr(requests, method.lower())
    kwargs = {}

    if hasattr(context, 'request_headers'):
        kwargs['headers'] = context.request_headers

    if body:
        kwargs['data'] = body

    if hasattr(context, 'request_files'):
        kwargs['files'] = context.request_files

    context.response = fn(make_url(context, endingpoint), **kwargs)
