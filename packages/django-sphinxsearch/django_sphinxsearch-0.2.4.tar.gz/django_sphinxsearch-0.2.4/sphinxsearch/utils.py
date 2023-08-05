# coding: utf-8

# $Id: $
import re

from django.utils import six


def sphinx_escape(value):
    """ Escapes SphinxQL search expressions. """

    if not isinstance(value, six.string_types):
        return value

    value = re.sub(r"([=<>()|!@~&/^$\-\'\"\\])", r'\\\1', value)
    value = re.sub(r'(SENTENCE|PARAGRAPH)', r'\\\1', value, flags=re.I)
    return value
