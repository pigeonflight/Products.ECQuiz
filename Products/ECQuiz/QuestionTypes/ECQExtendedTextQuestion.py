# -*- coding: utf-8 -*-
#
# $Id: ECQExtendedTextQuestion.py 245805 2011-10-23 19:08:23Z amelung $
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

from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import Schema, TextAreaWidget, TextField, \
     IntegerField, IntegerWidget

from Products.ECQuiz.config import *
from Products.ECQuiz.permissions import *
from Products.ECQuiz.tools import *
from Products.ECQuiz.QuestionTypes.ECQPointsQuestion \
     import ECQPointsQuestion

class ECQExtendedTextQuestion(ECQPointsQuestion):
    """A question that allows the candidate to write a text answer."""

    schema = ECQPointsQuestion.schema.copy() + Schema((
        TextField(
            'answerTemplate', # See 'description' property
                              # of the widget.
            searchable=True,
            required=False,
            allowable_content_types=('text/plain',
                                     #'text/structured',
                                     #'text/restructured',
                                     #'text/html',
                                     ),
            default_output_type='text/plain',
            widget=TextAreaWidget(
                label='Answer Template',
                label_msgid='answer_template_label',
                description="You can provide a template for the "
                "candidate's answer.",
                description_msgid='answer_template_tool_tip',
                i18n_domain=I18N_DOMAIN,
                rows=10,
                ),
            validators=('isXML',),
            read_permission=PERMISSION_STUDENT,
            ),
        
        IntegerField('expectedLength',
                required=False,
                default=50,
                validators=('isPositiveInt',),
                widget=IntegerWidget(
                    label='Expected Length',
                    label_msgid='expected_length_label',
                    description="You can set the number of words you "
                    "expect the candidate's answer to have.",
                    description_msgid='expected_length_tool_tip',
                    i18n_domain=I18N_DOMAIN),
                read_permission=PERMISSION_STUDENT,
            ),
        ),)
    # This type of question is always tutor-graded
    schema.delField('tutorGraded')
    # Make "points" appear *after* the "answerTemplate"
    schema.moveField('points', 1)
    schema.moveField('points', 1)
        
    allowed_content_types = ()
    filter_content_types = True # Otherwise allowed_content_types == ()
                                # means 'allow everything'
    
    meta_type = 'ECQExtendedTextQuestion'     # zope type name
    portal_type = meta_type                   # plone type name
    archetype_name = 'Extended Text Question' # friendly type name

    # Use the portal_factory for this type.  The portal_factory tool
    # allows users to initiate the creation objects in a such a way
    # that if they do not complete an edit form, no object is created
    # in the ZODB.
    #
    # This attribute is evaluated by the Extensions/Install.py script.
    use_portal_factory = True

    typeDescription = "A question that allows the candidate to write " \
                      "a text answer."
    typeDescMsgId = 'description_edit_extextquestion'

    security = ClassSecurityInfo()

    security.declarePublic('isTutorGraded')
    def isTutorGraded(self, *args, **kwargs):
        return True


# Register this type in Zope
registerATCTLogged(ECQExtendedTextQuestion)
