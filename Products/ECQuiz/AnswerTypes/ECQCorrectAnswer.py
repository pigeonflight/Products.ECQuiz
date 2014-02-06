# -*- coding: utf-8 -*-
#
# $Id: ECQCorrectAnswer.py 251338 2012-10-31 16:31:52Z amelung $
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

from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import Schema, BooleanField, TextAreaWidget, BooleanWidget

from Products.ECQuiz import config
from Products.ECQuiz import permissions
from Products.ECQuiz.tools import registerTypeLogged
from Products.ECQuiz.AnswerTypes.ECQSelectionAnswer import ECQSelectionAnswer
from Products.ECQuiz.InlineTextField import InlineTextField

class ECQCorrectAnswer(ECQSelectionAnswer):
    """ An answer that can be either a right or wrong (in the context of
        a question that contains this answer).
    """

    schema = ECQSelectionAnswer.schema.copy() + Schema((
            InlineTextField('comment',
                accessor='getCommentPrivate',
                searchable=True,
                required=False,
                read_permission=permissions.PERMISSION_INTERROGATOR,
                allowable_content_types=('text/plain',
                    'text/structured',
                    'text/restructured',
                    'text/html',),
                default_output_type='text/html',
                widget=TextAreaWidget(
                    label='Comment',
                    label_msgid='answer_comment_label',
                    description='A comment on the answer. If the quiz '
                    'is set to "instant feedback", '
                    'the candidate will see this text in case his/her '
                    'answer was wrong.',
                    description_msgid='answer_comment_tool_tip',
                    i18n_domain=config.I18N_DOMAIN),
                validators=('isXML',),
            ),
            BooleanField('correct',
                accessor='isCorrectPrivate',
                default=0,
                searchable=False,
                read_permission=permissions.PERMISSION_INTERROGATOR,
                widget=BooleanWidget(
                    label='Correct',
                    label_msgid='correct_label',
                    description='The checkbox should be marked if this '
                    'is a correct answer.',
                    description_msgid='correct_tool_tip',
                    i18n_domain=config.I18N_DOMAIN),
                languageIndependent=True,
            ),
        ),
    )
    
    # Use a custom page template for viewing.
    actions = (
        {
            'id': 'view',
            'action': 'string:${object_url}/ecq_correctanswer_view',
        },
    )
    
    meta_type = 'ECQCorrectAnswer'    # zope type name
    portal_type = meta_type           # plone type name
    archetype_name = 'Correct Answer' # friendly type name
    
    security = ClassSecurityInfo()
    security.declareProtected(permissions.PERMISSION_STUDENT, 'isCorrect')
    def isCorrect(self, *args, **kwargs):
        # no docstring prevents publishing
        #FIXME: check permssions: only return something if we're in resultView
        return self.isCorrectPrivate(*args, **kwargs)
        
    security.declareProtected(permissions.PERMISSION_STUDENT, 'getComment')
    def getComment(self, *args, **kwargs):
        # no docstring prevents publishing
        #FIXME: check permssions: only return something if we're in resultView
        return self.getCommentPrivate(*args, **kwargs)
    

# Register this type in Zope
registerTypeLogged(ECQCorrectAnswer)
