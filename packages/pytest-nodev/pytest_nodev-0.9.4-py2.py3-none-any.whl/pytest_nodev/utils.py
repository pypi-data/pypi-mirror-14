# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

# python 2 support via python-future
from __future__ import absolute_import, unicode_literals
from builtins import super

import logging


# regex impossible to match (even in re.MULTILINE mode)
NOMATCH_PATTERN = r'.\A'


def exclude_include_pattern(include_pattern='', exclude_pattern=NOMATCH_PATTERN):
    """Return a pattern that matches ``include_pattern`` except matches of ``exclude_pattern``.

    :param str include_pattern: Include everything by default (r'').
    :param str exclude_pattern: Exclude nothing by default (r'.\A').
    :rtype: str
    """
    return '(?!%s)%s' % (exclude_pattern, include_pattern)


class EmitHandler(logging.Handler):
    """Send logging output via a custom callable."""
    def __init__(self, emit_callable, **kwargs):
        super(EmitHandler, self).__init__(**kwargs)
        self.emit_callable = emit_callable

    def emit(self, record):
        self.emit_callable(self.format(record))
