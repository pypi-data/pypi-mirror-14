# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = "d01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2015-16, Florian JUNG"
__license__ = "All rights reserved"
__version__ = "0.1.0a0"
__date__ = "2016-03-26"
# Created: 2015-03-21 24:00
""" Package facilitating all audience participational needs """

import logging

from .papsException import PapsException
from .changeInterface import ChangeInterface
from .person import Person


__all__ = ["person", "changeInterface", "papsException"]
logger = logging.getLogger(__name__)
