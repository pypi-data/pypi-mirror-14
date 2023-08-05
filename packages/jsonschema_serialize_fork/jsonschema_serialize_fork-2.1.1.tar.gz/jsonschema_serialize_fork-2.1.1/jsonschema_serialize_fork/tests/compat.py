import sys


if sys.version_info[:2] < (2, 7):  # pragma: no cover
    import unittest2 as unittest
    from ordereddict import OrderedDict
else:
    import unittest
    from collections import OrderedDict

try:
    from unittest import mock
except ImportError:
    import mock


# flake8: noqa
