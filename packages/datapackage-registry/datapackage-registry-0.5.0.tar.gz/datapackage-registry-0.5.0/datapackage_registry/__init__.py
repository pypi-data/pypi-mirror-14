# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .registry import Registry
import warnings

warnings.warn(
    'The "datapackage-registry" package is deprecated. Please use '
    '"datapackage" instead',
    DeprecationWarning
)
