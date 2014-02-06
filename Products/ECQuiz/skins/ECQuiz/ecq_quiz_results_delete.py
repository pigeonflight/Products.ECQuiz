## Script (Python) "ecq_quiz_results_delete"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# $Id: ecq_quiz_results_delete.py 245805 2011-10-23 19:08:23Z amelung $
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

if not REQUEST.has_key('ids'):
    msg = context.translate(
        msgid   = 'select_item_delete',
        domain  = I18N_DOMAIN,
        default = 'Please select one or more items to delete first.')
else:
    ids = REQUEST['ids']
    context.deleteResultsById(ids)
    if len(ids) == 1:
        msg = context.translate(
            msgid   = 'item_deleted',
            domain  = I18N_DOMAIN,
            default = 'Item deleted.')
    else:
        msg = context.translate(
            msgid   = 'items_deleted',
            domain  = I18N_DOMAIN,
            default = 'Items deleted.')

target = context.getActionInfo('object/results')['url']
context.redirect('%s?portal_status_message=%s' % (target, msg))
