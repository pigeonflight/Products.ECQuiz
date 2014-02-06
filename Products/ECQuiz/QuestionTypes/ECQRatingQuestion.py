# -*- coding: utf-8 -*-
#
# $Id: ECQRatingQuestion.py 245805 2011-10-23 19:08:23Z amelung $
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

from Acquisition import aq_base, aq_acquire, aq_inner, aq_parent

from Products.Archetypes.public import BaseFolder, BaseFolderSchema, \
BaseContent, BaseSchema, Schema, BooleanField, BooleanWidget, IntegerField, \
IntegerWidget, StringField, TextField, SelectionWidget, TextAreaWidget, \
StringWidget, RichWidget

from Products.ECQuiz.config import *
from Products.ECQuiz.permissions import *
from Products.ECQuiz.tools import *
from Products.ECQuiz.QuestionTypes.ECQSelectionQuestion \
     import ECQSelectionQuestion
from Products.ECQuiz.QuestionTypes.ECQPointsQuestion \
     import ECQPointsQuestion
from Products.ECQuiz.AnswerTypes.ECQSelectionAnswer \
     import ECQSelectionAnswer


class ECQRatingQuestion(ECQSelectionQuestion, ECQPointsQuestion):
    """ A question that asks the candidate to give a rating for something.
        'points', in this class, is the maximum rating. The answers are 
        the possible ratings (e.g. 'very good', 'OK', 'bad'). 'getCandidatePoints' 
        returns which rating(s) has (have) been selected.
    """

    schema = ECQSelectionQuestion.schema.copy() + \
             ECQPointsQuestion.schema.copy()

    def getCandidatePoints(self, candidateId):
        """ Return how many points the user got for this question.

            @param candidateId The user ID of the candidate whose points you want to know.

            If a custom evaluation script has been uploaded it will be
            invoked. Otherwise a default method will be used.
        """
        parent = getParent(self)
        customScript = parent.getEvaluationScript(self.portal_type)
        candidateAnswer = self.getCandidateAnswer(candidateId)
        if not customScript: # default
            if candidateAnswer is None:
                return None
            else:
                if(candidateAnswer == None):
                    candidateAnswer = []
                suggestedAnswers = self.getSuggestedAnswers(candidateId)
                selectedAnswers = [answer for answer in suggestedAnswers
                                   if answer.getId() in candidateAnswer]
                if not selectedAnswers:
                    # Nothig has been selected
                    return None
                elif len(selectedAnswers) > 1:
                    # If multiple answers have been selected, return a
                    # list with the answers' texts.
                    return [a.getAnswer() for a in selectedAnswers]
                else:
                    # No multiple selection -> Return the selected
                    # answer's text
                    selectedAnswerText = selectedAnswers[0].getAnswer()
                    try:
                        # If he answer is a number, return it as a number.
                        return float(selectedAnswerText)
                    except:
                        # No number -> return just the text.
                        return selectedAnswerText
        else: # use custom script
            return evalFunString(customScript,
                                 CUSTOM_EVALUATION_FUNCTION_NAME,
                                 [self, candidateId, answer])


# Register this type in Zope
registerATCTLogged(ECQRatingQuestion)
