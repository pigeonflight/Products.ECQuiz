# -*- coding: utf-8 -*-
#
# $Id: ECQBaseQuestion.py 245805 2011-10-23 19:08:23Z amelung $
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

import random

from AccessControl import ClassSecurityInfo

from Acquisition import *

from Products.Archetypes.public import Schema, BooleanField, BooleanWidget, \
     IntegerField, IntegerWidget, StringField, \
     TextAreaWidget, StringWidget

from Products.ECQuiz.config import *
from Products.ECQuiz.permissions import *
from Products.ECQuiz.tools import *
from Products.ECQuiz.AnswerTypes.ECQBaseAnswer import ECQBaseAnswer
from Products.ECQuiz.InlineTextField import InlineTextField
from Products.ECQuiz.ECQFolder import ECQFolder


class ECQBaseQuestion(ECQFolder):
    """ A very basic question type without any evaluation functions.
    
        A question is basically a question text and a set of possible
        answers to this question or, in Plone terms, a folder with
        some additional properties such as the question text.
    """

    schema = ECQFolder.schema.copy() + Schema((
            StringField('title',
                required=False,
                searchable=True,
                default='Question',
                widget=StringWidget(
                    label_msgid='label_title',
                    description_msgid='title',
                    i18n_domain='plone'),
                read_permission=PERMISSION_STUDENT,
            ),
            InlineTextField('question', # See 'description' property
                                        # of the widget.
                searchable=True,
                required=True,
                primary=True,
                allowable_content_types=('text/plain',
                    'text/structured',
                    'text/restructured',
                    'text/html',),
                default_output_type='text/html',
                widget=TextAreaWidget(
                    label='Question',
                    label_msgid='question_label',
                    description='The question text. This is what the '
                    'candidate will see.',
                    description_msgid='question_tool_tip',
                    i18n_domain=I18N_DOMAIN,
                    rows=10,
                    ),
                validators=('isXML',),
                read_permission=PERMISSION_STUDENT,
            ),
        ),
    )

    security = ClassSecurityInfo()

    #security.declareProtected(PERMISSION_INTERROGATOR, 'contentValues')
    #security.declareProtected(PERMISSION_INTERROGATOR, 'listFolderContents')
    
    # Declaring "folderlistingFolderContents" as protected prevents
    # the answers from being listed if someone without
    # PERMISSION_INTERROGATOR tries to call the "base_view" template
    # for a question.
    security.declareProtected(PERMISSION_INTERROGATOR,
                              'folderlistingFolderContents')

    security.declareProtected(PERMISSION_STUDENT, 'UID')
    
    security.declarePrivate('makeNewTest')
    def makeNewTest(self, candidateResult, suMode):
        """generate a new quiz"""
        # This is just to register the question with result object
        candidateResult.setSuggestedAnswer(self, None)
    

    security.declareProtected(PERMISSION_STUDENT, 'haveCandidateAnswer')
    def haveCandidateAnswer(self, result):
        """
        @param result A Result object
        """
        return result.haveCandidateAnswer(self)

# Register this type in Zope
registerATCTLogged(ECQBaseQuestion)
