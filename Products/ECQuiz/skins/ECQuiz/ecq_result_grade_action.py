## Script (Python) "gradeResult"
##title=
##

#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# $Id: ecq_result_grade_action.py 245805 2011-10-23 19:08:23Z amelung $
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

REQUEST  = context.REQUEST

I18N_DOMAIN = context.i18n_domain

result = context
mctest = result.aq_inner.aq_parent
decimalSeparator = context.translate(msgid = 'fraction_delimiter',
                                     domain = I18N_DOMAIN,
                                     default = '.')
            
for group in [mctest] + mctest.getQuestionGroups():
    for question in group.getQuestions(result):
        if question.isTutorGraded():
            value = REQUEST.get(question.UID())[0].strip()
            if value:
                value = value.replace(decimalSeparator, '.')
                points = float(value)
                result.setTutorPoints(question, points)
            else:
                result.unsetTutorPoints(question)
            
msgid = 'Changes saved.'
msg = context.translate(
    msgid   = msgid,
    domain  = 'plone',
    default = msgid)

target = result.getActionInfo('object/view')['url']

context.plone_utils.addPortalMessage(msg)
context.redirect('%s' % target)
