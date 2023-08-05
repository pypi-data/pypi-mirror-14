# encoding: utf-8
# This module is courtesy of Adrian Macneil and licensed under the same terms as the Django codebase to
# which it was contributed:
# https://gist.github.com/amacneil/5af7cd0e934f5465b695
# https://code.djangoproject.com/ticket/17419

from __future__ import absolute_import, division, print_function, unicode_literals

from json import dumps as json_dumps

from django.core.serializers.json import DjangoJSONEncoder
from django.template import Library

register = Library()


@register.filter
def json(data):
    """
    Safely JSON-encode an object

    To protect against XSS attacks, HTML special characters (``<``, ``>``, ``&``) and unicode newlines are
    replaced by escaped unicode characters. Django does not escape these characters by default.

    Output of this method is not marked as HTML safe. If you use it inside an HTML attribute, it must be
    escaped like regular data::

        <div data-user="{{ data|json }}">

    If you use it inside a ``<script>`` tag, then the output does not need to be escaped, so you can mark it
    as safe::

        <script>
            var user = {{ data|json|safe }};
        </script>

    Escaped characters taken from Rails ``json_escape()`` helper:
    https://github.com/rails/rails/blob/v4.2.5/activesupport/lib/active_support/core_ext/string/output_safety.rb#L60-L113
    """

    unsafe_chars = {'&': '\\u0026',
                    '<': '\\u003c',
                    '>': '\\u003e',
                    '\u2028': '\\u2028',
                    '\u2029': '\\u2029'}

    json_str = json_dumps(data, cls=DjangoJSONEncoder)

    for (c, d) in unsafe_chars.items():
        json_str = json_str.replace(c, d)

    return json_str
