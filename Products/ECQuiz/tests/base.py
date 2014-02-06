# -*- coding: utf-8 -*-
#
# $Id: base.py 245805 2011-10-23 19:08:23Z amelung $
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

"""Base class for integration tests, based on ZopeTestCase and PloneTestCase.

Note that importing this module has various side-effects: it registers a set of
products with Zope, and it sets up a sandbox Plone site with the appropriate
products installed.
"""

from Testing import ZopeTestCase

# Let Zope know about the products we require above and beyond a basic
# Plone install (PloneTestCase takes care of these).
ZopeTestCase.installProduct('DataGridField')
ZopeTestCase.installProduct('ECQuiz')

# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite

# Set up a Plone site, and apply the membrane and borg extension profiles
# to make sure they are installed.
#setupPloneSite(extension_profiles=('membrane:default', 'borg:default'))
setupPloneSite(products=('ECQuiz',))

from Products.ECQuiz.tools import createObject

def getAccessor(obj, prop_name, getter_p):
    if getter_p:
        prefix = 'get'
    else:
        prefix = 'set'
    name = prefix + prop_name[0].upper() + prop_name[1:]
    return getattr(obj, name)

def setProp(obj, prop_name, value):
    f = getAccessor(obj, prop_name, False)
    f(value)

def getProp(obj, prop_name):
    f = getAccessor(obj, prop_name, True)
    return f()

def setProps(obj, props_values):
    for p, v in props_values:
        setProp(obj, p, v)

class ECQTestCase(PloneTestCase):
    """Base class for integration tests for the 'ECQuiz' product.
    This may provide specific set-up and tear-down operations, or
    provide convenience methods.
    """
    
    def createEmptyQuiz(self):
        """ currently logged-in user must be manager level
        """
        portal = self.portal
        dummy = createObject(self.portal, 'ECQuiz', 'dummy')
        portal.dummy = dummy
        # Set up the test's properties
        setProps(dummy, (('instantFeedback', False),
                         ('allowRepetition', False),
                         ('onePerPage', False),
                         ('onePerPageNav', False),
                         ('scoringFunction', 'cruel'),
                         #('gradingScale', ()),
                         ('directions', 'Please answer these questions!'),
                         ('randomOrder', False),
                         ('numberOfRandomQuestions', 0),))
        return dummy
        
    
    def createDummy(self):
        """ currently logged-in user must be manager level
        """
        portal = self.portal
        # dummy = ECQuiz(oid='dummy')
        # # put dummy in context of portal
        # dummy = dummy.__of__(portal)
        # portal.dummy = dummy
        # dummy.initializeArchetype()
        # return dummy
        dummy = self.createEmptyQuiz()
        # Create an MC question
        mcq = createObject(dummy, 'ECQMCQuestion', 'mcq')
        # Set up the question's properties
        setProps(mcq, (('allowMultipleSelection', False),
                       ('randomOrder', False),
                       ('numberOfRandomAnswers', 0),
                       ('points', 666),
                       ('tutorGraded', False),
                       ))
        # Create MC answers
        for uid, comm, corr, answ in (('mca1', 'Correct comment', True,  'This is correct.'),
                                      ('mca2', 'Wrong comment',   False, 'This is wrong.'  ),
                                      ):
            mca = createObject(mcq, 'ECQMCAnswer', uid)
            # Set up the answer's properties
            setProps(mca, (('comment', comm),
                           ('correct', corr),
                           ('answer',  answ),
                           ))
        # publish the thing
        wtool = portal.portal_workflow
        wtool.doActionFor(dummy, 'publish')
        
        return dummy

class ECQFunctionalTestCase(FunctionalTestCase):
    """Base class for functional integration tests for the 'ECQuiz'
    product.  This may provide specific set-up and tear-down
    operations, or provide convenience methods.
    """
