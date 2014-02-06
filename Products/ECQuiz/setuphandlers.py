# -*- coding: utf-8 -*-
# $Id: setuphandlers.py 245805 2011-10-23 19:08:23Z amelung $
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
#
__author__ = """Mario Amelung <mario.amelung@gmx.de>"""
__docformat__ = 'plaintext'

import transaction

from Products.CMFCore.utils import getToolByName

from Products.ECQuiz import config
from Products.ECQuiz.tools import log

def isNotECQuizProfile(context):
    """
    """
    return context.readDataFile("ECQuiz_marker.txt") is None


def installGSDependencies(context):
    """Install dependend profiles.
    """
    
    if isNotECQuizProfile(context): return 
    
    # Has to be refactored as soon as generic setup allows a more 
    # flexible way to handle dependencies.
    return


def installQIDependencies(context):
    """Install dependencies
    """
    
    if isNotECQuizProfile(context): return 

    site = context.getSite()

    portal = getToolByName(site, 'portal_url').getPortalObject()
    quickinstaller = portal.portal_quickinstaller
    
    for dependency in config.DEPENDENCIES:
        if quickinstaller.isProductInstalled(dependency):
            log('Reinstalling dependency %s:' % dependency)
            quickinstaller.reinstallProducts([dependency])
            transaction.savepoint()
        else:
            log('Installing dependency %s:' % dependency)
            quickinstaller.installProduct(dependency)
            transaction.savepoint()
