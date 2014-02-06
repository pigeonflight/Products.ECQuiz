# -*- coding: utf-8 -*-
#
# $Id: test_perms.py 245805 2011-10-23 19:08:23Z amelung $
#
# Copyright © 2004-2011 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECQuiz.
#
# ECQuiz is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# ECQuiz is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ECQuiz; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

from AccessControl import Unauthorized

from base import ECQTestCase
from base import setProp, setProps, getProp, getAccessor
from Products.ECQuiz.config import *
from Products.ECQuiz.tools import createObject


class TestPermissions(ECQTestCase):
    
    def afterSetUp(self):
        ECQTestCase.afterSetUp(self)
        self.membership = self.portal.portal_membership
        self.membership.addMember('member', 'secret', ['Member'], [])
        self.membership.addMember('manager', 'secret', ['Manager'], [])
        self.login('manager')
        self._dummy = self.createDummy()
    
    
    def testQuizPerms(self):
        t = self._dummy
        self.login('member')
        
        self.assertRaises(Unauthorized, t.maybeMakeNewTest)
        

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPermissions))
    return suite
