# -*- coding: utf-8 -*-
#
# $Id:validators.py 1255 2009-09-24 08:47:42Z amelung $
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

import re
from xml.dom.minidom import parseString

from zope.interface import implements
from Products.validation.interfaces.IValidator import IValidator

#from tools import log
from Products.ECQuiz.tools import registerValidatorLogged
from Products.ECQuiz import config

class XMLValidator:
    """A validator for XML fragments."""
    
    implements(IValidator)
    
    def __init__(self, name):
        self.name = name
    
    def __call__(self, value, *args, **kwargs):
        # First we have to find out if this is meant to be text/html
        instance = kwargs.get('instance', None)
        field    = kwargs.get('field',    None)
        if instance and field:
            request     = getattr(instance, 'REQUEST', None)
            formatField = "%s_text_format" % field.getName()
            if request and ( request.get(formatField, 
                '').strip().lower() == 'text/html' ):
                # Aha! The format was set to 'text/html'
                if isinstance(value, str):
                    string = '<a>' + value + '</a>'
                else:
                    string = u'<a>' + value + u'</a>'
                try:
                    doc = parseString(string)
                    doc.unlink() # Destroy the document object so the garbage
                    # collector can delete it
                    return 1
                except:
                    return """Please use XHTML conformant markup."""
        # The format was not 'text/html' or something went wrong
        return True

# Register this validator in Zope
registerValidatorLogged(XMLValidator, 'isXML')


class PositiveIntegerValidator:
    """A validator for positive integers."""
    
    implements(IValidator)
    
    def __init__(self, name):
        self.name = name
    
    def __call__(self, value, *args, **kwargs):
        if (not re.compile(r'^[1-9]\d*$').match(value)):
            return """Please enter a positive integer."""
        return True

# Register this validator in Zope
registerValidatorLogged(PositiveIntegerValidator, 'isPositiveInt')


class PercentageValidator:
    """A validator for percentages, ."""

    implements(IValidator)
    
    def __init__(self, name):
        self.name = name
        
    def __call__(self, value, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            decimalSeparator = \
                instance.translate(msgid = 'fraction_delimiter',
                                   domain = config.I18N_DOMAIN,
                                   default = '.')
            res = None
            match = re.match('^[0-9]+(\\'
                             + decimalSeparator
                             + r')?[0-9]*\s*%$', value)
            if match:
                return None
            else:
                return instance.translate(
                           msgid   = 'invalid_percentage',
                           domain  = config.I18N_DOMAIN,
                           default = 'Not a percentage: %s') % value
        else:
            return True

# Register this validator in Zope
registerValidatorLogged(PercentageValidator, 'percentage')


class ClearPointsCache:
    """A dummy validator that clears cached points for a question (and
    its question group and the quiz) from result objects."""
    
    implements(IValidator)
    
    def __init__(self, name):
        self.name = name
        
    def __call__(self, value, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            # [unsetCachedQuestionPoints] is found through acquisition magic
            instance.unsetCachedQuestionPoints(instance)
        return True

# Register this validator in Zope
registerValidatorLogged(ClearPointsCache, 'clearPointsCache')


class ClearWholePointsCache:
    """A dummy validator that clears any cached points from result objects."""

    implements(IValidator)
    
    def __init__(self, name):
        self.name = name
        
    def __call__(self, value, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            instance.unsetAllCachedPoints()
        return True

# Register this validator in Zope
registerValidatorLogged(ClearWholePointsCache, 'clearWholePointsCache')

class GradingScaleValidator:
    """A validator for grading scales."""

    implements(IValidator)
    
    def __init__(self, name):
        self.name = name
        
    def __call__(self, value, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            decimalSeparator = \
                instance.translate(msgid = 'fraction_delimiter',
                                   domain = config.I18N_DOMAIN,
                                   default = '.')
            res = None
            non_empty = [v for v in value
                         if v['score'].strip() or v['grade'].strip()]
            
            for row in non_empty:
                grade = row['grade'].strip()
                if not grade:
                    label = instance.translate(
                        msgid   = 'grade',
                        domain  = config.I18N_DOMAIN,
                        default = "Grade")
                    res = instance.translate(
                        msgid   = 'error_required',
                        domain  = 'archetypes',
                        default = '%s is required, please correct.' % label,
                        mapping = {'name': label},)
                    break
                        
                score = row['score'].strip()
                if row is non_empty[-1]: # last score field should be empty
                    if len(score) != 0:
                        res = instance.translate(
                            msgid   = 'minimum_score_not_empty',
                            domain  = config.I18N_DOMAIN,
                            default = 'The minimum score column of the '
                            'last row must be empty.')
                else:
                    match = re.match('^[0-9]+(\\'
                                     + decimalSeparator
                                     + r')?[0-9]*\s*%?$', score)
                    if not match:
                        res = instance.translate(
                            msgid   = 'invalid_minimum_score',
                            domain  = config.I18N_DOMAIN,
                            default = 'Not a percentage or an absolute '
                            'value: %s') % score
                        break
            return res
        else:
            return True

# Register this validator in Zope
registerValidatorLogged(GradingScaleValidator, 'gradingScale')
