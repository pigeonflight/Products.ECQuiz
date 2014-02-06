# -*- coding: utf-8 -*-
#
# $Id: __init__.py 245805 2011-10-23 19:08:23Z amelung $
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

""" This file is needed in order to make Zope import this directory.
    All the following statements will be executed and finally 
    the 'initialize' function will be called.
"""
import logging

from Products.ECQuiz.tools import log
# mark start of Product initialization in log file
# for details on 'log' see Products.ECQuiz.config
log('------------------------------------------------------------------')

import os.path

from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils as cmfutils
from Products.CMFPlone.utils import ToolInit
from Products.CMFCore.DirectoryView import registerDirectory

from Products.ECQuiz.validators import *

# some global constants (in ALL_CAPS) and functions
from Products.ECQuiz import config
from Products.ECQuiz.tools import *
from Products.ECQuiz.permissions import *
from Products.ECQuiz.ECQTool import ECQTool

LOG = logging.getLogger(config.PROJECTNAME)

module = ''

# import self defined types and register them in Zope
# (the registration of the classes contained in each file
# is done via 'registerType(ClassName)' statements in the file)
try:
    # import all answer types
    #   1. import the directory ANSWER_DIR 
    #      (can only work if there is an __init__.py in the directory)
    __import__(config.ANSWER_DIR, config.GLOBALS, locals())
    #   2. import all files in the list ANSWER_TYPES (for this to work it 
    # is not necessary to write one file per class and name the 
    # file after the class)
    for entry in config.ANSWER_TYPES:
        module = config.ANSWER_DIR + '.' + str(entry)
        __import__(module, config.GLOBALS, locals())
        log('Done: importing module "%s"' % module)
    
    # import all question types
    #   1. import the directory QUESTION_DIR
    __import__(config.QUESTION_DIR, config.GLOBALS, locals())
    #   2. import all files in the list QUESTION_TYPES
    for entry in config.QUESTION_TYPES:
        module = config.QUESTION_DIR + '.' + str(entry)
        __import__(module, config.GLOBALS, locals())
        log('Done: importing module "%s"' % module)

    # import 'ECQAbstractGroup', 'ECQuiz', 'ECQGroup'
    for m in ['ECQResult',
              'ECQFolder',
              'ECQAbstractGroup',
              'ECQuiz',
              'ECQGroup',
              'ECQReference']:
        module = m
        exec('import ' + module)
        log('Done: importing module "' + module + '"')

except Exception, e:
    # log any errors that occurred
    log('Failed: importing module "' + module + '": ' + unicode(e))

""" Register the skins directory (where all the page templates, the
    '.pt' files, live) (defined in Products.ECQuiz.config)
"""
registerDirectory(config.SKINS_DIR, config.GLOBALS)

def initialize(context):
    """ The 'initialize' function of this Product.
        It is called when Zope is restarted with these files in the Products 
        directory. (I'm not sure what it does or if it is neccessary 
        at all. Best leave it alone.)
    """
    log('Start: "initialize()"')

    # Initialize portal tools
    tools = [ECQTool]
    ToolInit(PROJECTNAME +' Tools',
             tools = tools,
             icon  = 'ec_tool.png'
             ).initialize(context)

    # Init contetn types
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)
    
    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = PERMISSION_ADD_MCTEST,
        extra_constructors = constructors,
        fti                = ftis,
    ).initialize(context)
    
    log('Done: "ContentInit()"')

    # Add permissions to allow control on a per-class basis
    for i in range(0, len(content_types)):
        content_type = content_types[i].__name__
        if ADD_CONTENT_PERMISSIONS.has_key(content_type):
            context.registerClass(meta_type    = ftis[i]['meta_type'],
                                  constructors = (constructors[i],),
                                  permission   = ADD_CONTENT_PERMISSIONS[content_type])

    #~ parsers.initialize(context)
    #~ renderers.initialize(context)
    log('Done: "initialize()"')

    # Mark end of Product initialization in log file.
    log('------------------------------------------------------------------')
