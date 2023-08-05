import os
import json
import mimetypes
from behave import *

from behave_web_api.utils import dereference_arguments, do_request,\
    compare_values, compare_contents


@given(u'I set header "{}" with value "{}"')
@dereference_arguments
def i_set_header_with_value(context, key, value):
    if not hasattr(context, 'request_headers'):
        context.request_headers = {}
    context.request_headers[key] = value


@given(u'I set variable "{}" with value "{}"')
@dereference_arguments
def i_set_variable_with_value(context, key, value):
    if not hasattr(context, 'variables'):
        context.variables = {}
    context.variables[key] = value


@given(u'I attach the file "{}" as "{}"')
@dereference_arguments
def i_attach_the_file_as(context, path, key):
    if not hasattr(context, 'request_files'):
        context.request_files = []
    name = os.path.basename(path)
    mimetype = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    context.request_files.append(
        (key, (name, open(path, 'rb'), mimetype))
    )


@when(u'I send a {} request to "{}" with body')
@dereference_arguments
def i_send_a_request_with_body(context, method, endingpoint):
    do_request(context, method, endingpoint, context.text)


@when(u'I send a {} request to "{}" with values')
@dereference_arguments
def i_send_a_request_with_values(context, method, endingpoint):
    values = {}

    for line in context.text.split(u'\n'):
        pieces = line.split(u'=')
        values[pieces[0]] = ''.join(pieces[1:]) if len(pieces) > 1 else ''

    do_request(context, method, endingpoint, values)


@when(u'I send a {} request to "{}"')
@dereference_arguments
def i_send_a_request(context, method, endingpoint):
    do_request(context, method, endingpoint)


@then(u'the response code should be {}')
@dereference_arguments
def the_response_should_be(context, status_code):
    compare_values(int(status_code), context.response.status_code)


@then(u'the response should contain json')
@dereference_arguments
def the_response_should_contain_json(context):
    expected_data = json.loads(context.text)
    actual_data = json.loads(context.response.text)
    compare_values(expected_data, actual_data)


@then(u'the response should contain text')
@dereference_arguments
def the_response_should_contain_text(context):
    compare_contents(context.text, context.response.text)


@then(u'print response')
def print_response(context):
    print(context.response.text)
