# -*- coding: utf-8 -*-
#
# $Id: ListValidator.py 245805 2011-10-23 19:08:23Z amelung $
#
# Copyright © 2004-2011 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECQuiz.
#
# ECQuiz is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# ECQuiz is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ECQuiz; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

""" A simple validator for lists. Currently not used. """

import re

from zope.interface import implements
from Products.validation.interfaces.IValidator import IValidator

from tools import registerValidatorLogged

listValidatorRe = re.compile(ur"\s*(?P<nonEmpty>\[\s*'[^']+'(\s*,\s*'[^']+'\s*)*\s*\])|(?P<empty>\[\s*\])\s*")

class ListValidator:
    """ A simple validator for lists. """

    implements(IValidator)

    def __init__(self, name):
        self.name = name
    def __call__(self, value, *args, **kwargs):
        if (not listValidatorRe.match(value)):
            return """Validation failed"""
        return 1

# Register this validator in Zope
registerValidatorLogged(ListValidator, 'isList')
