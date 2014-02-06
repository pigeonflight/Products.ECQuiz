# -*- coding: utf-8 -*-
#
# $Id:ECQFolder.py 1255 2009-09-24 08:47:42Z amelung $
#
# Copyright � 2004-2011 Otto-von-Guericke-Universit�t Magdeburg
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

from Products.Archetypes.public import OrderedBaseFolder
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from AccessControl import ClassSecurityInfo
#from Products.CMFCore import permissions as CMFCorePermissions

from Products.ECQuiz import config 
from Products.ECQuiz import permissions
from Products.ECQuiz.tools import registerATCTLogged
from Products.ECQuiz import log

class ECQFolder(ATFolder):
    """An ATFolder that calls the ECQuiz method [syncResults] when
    something happens that might invalidate existing result objects."""
    schema = ATFolderSchema.copy()
    __implements__ = (ATFolder.__implements__)
    
    #global_allow = False
    #meta_type = 'ECQFolder'          # zope type name
    #portal_type = meta_type          # plone type name
    #archetype_name = 'ECQuiz Folder' # friendly type name
    
    security = ClassSecurityInfo()

    """Only users with privileges of PERMISSION_INTERROGATOR (see
    config) or higher may call this
    function directly or indirectly (e.g. by calling the
    folder_contents page template).
    """
    #security.declareProtected(PERMISSION_INTERROGATOR, 'listFolderContents')
    
    """Declaring 'folderlistingFolderContents' as protected prevents
    the answers from being listed if someone without
    PERMISSION_INTERROGATOR tries to call the 'base_view' template for
    a derived type (like quiz or question group).
    """
    #security.declareProtected(PERMISSION_INTERROGATOR,
    #                          'folderlistingFolderContents')
    security.declareProtected(permissions.PERMISSION_STUDENT, 'Type')
    security.declareProtected(permissions.PERMISSION_STUDENT, 'title_or_id')

    #security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'moveObjectsByDelta')
    def moveObjectsByDelta(self, *args, **kwargs):
        """
        """
        #log("moveObjectsByDelta: %s" % self)

        retVal = ATFolder.moveObjectsByDelta(self, *args, **kwargs)
        self.syncResults('move')
        return retVal
    
    security.declarePrivate('manage_afterAdd')
    def manage_afterAdd(self, *args, **kwargs):
        """
        """
        #log("manage_afterAdd: %s" % self)

        #retVal = OrderedBaseFolder.manage_afterAdd(self, *args, **kwargs)
        retVal = ATFolder.manage_afterAdd(self, *args, **kwargs)
        self.syncResults('add')
        return retVal
    
    security.declarePrivate('manage_beforeDelete')
    def manage_beforeDelete(self, *args, **kwargs):
        """
        """
        #log("manage_beforeDelete: %s" % self)

        retVal = ATFolder.manage_beforeDelete(self, *args, **kwargs)
        self.syncResults('delete')
        return retVal


# Register this type in Zope
registerATCTLogged(ECQFolder)

