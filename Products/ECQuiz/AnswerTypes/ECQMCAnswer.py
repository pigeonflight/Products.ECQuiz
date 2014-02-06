# -*- coding: utf-8 -*-
#
# $Id: ECQMCAnswer.py 245805 2011-10-23 19:08:23Z amelung $
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

from AccessControl import ClassSecurityInfo

#from Products.ECQuiz import config
from Products.ECQuiz import permissions
#from Products.ECQuiz.tools import log
from Products.ECQuiz.tools import registerTypeLogged
from Products.ECQuiz.AnswerTypes.ECQCorrectAnswer import ECQCorrectAnswer

class ECQMCAnswer(ECQCorrectAnswer):
    """An answer to a multiple-choice question."""
    
    schema = ECQCorrectAnswer.schema.copy()
    
    schema['id'].read_permission = permissions.PERMISSION_STUDENT
    schema['answer'].read_permission = permissions.PERMISSION_STUDENT


    meta_type = 'ECQMCAnswer'    # zope type name
    portal_type = meta_type      # plone type name
    archetype_name = 'MC Answer' # friendly type name

    # Use the portal_factory for this type.  The portal_factory tool
    # allows users to initiate the creation objects in such a way
    # that if they do not complete an edit form, no object is created
    # in the ZODB.
    #
    # This attribute is evaluated by the Extensions/Install.py script.
    use_portal_factory = True

    security = ClassSecurityInfo()
    
    #security.declareProtected(permissions.PERMISSION_STUDENT, 'getId')
    #security.declareProtected(PERMISSION_STUDENT, 'getAnswer')
    

# Register this type in Zope
registerTypeLogged(ECQMCAnswer)
