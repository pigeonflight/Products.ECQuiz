# -*- coding: utf-8 -*-
#
# $Id: ECQSelectionAnswer.py 245805 2011-10-23 19:08:23Z amelung $
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

#from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import Schema, TextAreaWidget

from Products.ECQuiz import config
from Products.ECQuiz import permissions
from Products.ECQuiz.tools import registerTypeLogged

from Products.ECQuiz.AnswerTypes.ECQBaseAnswer import ECQBaseAnswer
from Products.ECQuiz.InlineTextField import InlineTextField

class ECQSelectionAnswer(ECQBaseAnswer):
    """ A predefined answer that a candidate can select.
    """

    schema = ECQBaseAnswer.schema.copy() + Schema((
            InlineTextField('answer', # See 'description' property of the widget.
                searchable=True,
                required=True,
                primary=True,
                allowable_content_types=('text/plain',
                    'text/structured',
                    'text/restructured',
                    'text/html',),
                default_output_type='text/html',
                widget=TextAreaWidget(
                    label='Answer',
                    label_msgid='answer_label',
                    description='The answer text. This is what the candidate will see.',
                    description_msgid='answer_tool_tip',
                    i18n_domain=config.I18N_DOMAIN),
                validators=('isXML',),
                read_permission=permissions.PERMISSION_STUDENT,
            ),
        ),
    )
    
    # Use a custom page template for viewing.
    actions = (
        {
            'id': 'view',
            'action': 'string:${object_url}/ecq_selectionanswer_view',
        },
    )
    
    meta_type = 'ECQSelectionAnswer'    # zope type name
    portal_type = meta_type             # plone type name
    archetype_name = 'Selection Answer' # friendly type name
    

# Register this type in Zope
registerTypeLogged(ECQSelectionAnswer)
