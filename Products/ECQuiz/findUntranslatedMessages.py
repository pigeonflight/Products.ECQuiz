#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# $Id: findUntranslatedMessages.py 245805 2011-10-23 19:08:23Z amelung $
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

import os, re, locale, sys

SKINS = './skins/ECQuiz/'

SKIP_DICT = {
    'archetype_name'                : SKINS + 'evaluation_scripts_widget.pt',
    'Export Item Statistics'        : SKINS + 'test_import_export.pt',
    'export_item_statistics_legend' : SKINS + 'test_import_export.pt',
    'ungrouped'                     : './ECQuiz.py',
    'I_DONT_KNOW'                   : SKINS + 'ecq_mcquestion_view.pt',
    }

DUPLICATES_SKIP_LIST = ['Add', 'Save']

MSGID = u'msgid'
QUOTES = "'" + '"'
CORE_EXPRESSION = ur'[' + QUOTES + '](?P<' + MSGID + ur'>[^' + QUOTES + ']+)' + '[' + QUOTES + ']'
EQ = ur'\s*=\s*'
PYTHON_RE = re.compile(ur'((msgid' + EQ + ur')|([' + QUOTES + ur']name[' + QUOTES + ur']\s*:\s*))' + CORE_EXPRESSION)
# i18n:translate attribute or a Python 'here.translate()' expression
PT_RE = re.compile(ur'((translate)|(msgid)|(value))' + EQ + CORE_EXPRESSION)
I18N_FILE_RE = re.compile(ur'^\s*msgid\s*' + CORE_EXPRESSION)
        
I18N_FILE_NAMES = ['../PloneTranslations/i18n/plone-de.po', '../Archetypes/i18n/archetypes-de.po', \
    'i18n/ECQuiz-de.po', 'i18n/plone-de.po']

class FileFilter(object):
    
    def __init__(self, types):
        self.types = types
        
    def filter(self, files, dirname, names):
        for fn in names:
            ext = os.path.splitext(fn)[1].lower()
            if ext in self.types:
                if dirname:
                    fn = os.path.join(dirname, fn)
                files.append(fn)
                
    
def findUntranslatedMessages(srcDir):
    i18nFileMsgidDict = {}
    for i18nFileName in I18N_FILE_NAMES:
        i18nFile = file(i18nFileName, 'r')
        lineCount = 1
        while True:
            line = i18nFile.readline()
            if not line:
                break
            match = I18N_FILE_RE.search(line)
            while match:
                msgid = match.group(MSGID)
                if (i18nFileMsgidDict.has_key(msgid)
                    and (not (msgid in DUPLICATES_SKIP_LIST))):
                    print >> sys.stderr, 'Duplicate msgid "' + msgid \
                          + '" in file ' + i18nFileName + ', ' \
                          + str(lineCount) + '. Previous definition: ' \
                          + str(i18nFileMsgidDict[msgid])
                else:
                    i18nFileMsgidDict[msgid] = i18nFileName + ', ' + str(lineCount)
                match = I18N_FILE_RE.search(line, match.end())
            lineCount += 1
        i18nFile.close()
    # print str(i18nFileMsgidDict)
    
    fileTypeList = [
        [FileFilter(['.py', '.cpy', '.vpy']).filter, PYTHON_RE],
        [FileFilter(['.pt', '.cpt', '.zpt']).filter, PT_RE]
    ]
    
    untranslatedMsgidDict = {}
    for filterFunction, regExp in fileTypeList:
        fileNamesList = []
        os.path.walk( srcDir, filterFunction, fileNamesList )
        for fileName in fileNamesList:
            f = file(fileName, 'r')
            
            foundMsgids = 0
            lineCount = 1
            while True:
                line = f.readline()
                if not line:
                    break
                match = regExp.search(line)
                while match:
                    foundMsgids += 1
                    msgid = match.group(MSGID)
                    #~ if(i == 1):
                        #~ print msgid
                    if not (i18nFileMsgidDict.has_key(msgid) or
                            untranslatedMsgidDict.has_key(msgid)):
                        untranslatedMsgidDict[msgid] = [fileName,
                                                        str(lineCount)]
                    match = regExp.search(line, match.end())
                lineCount += 1
                
            f.close()
            #~ print 'Found ' + str(foundMsgids) + ' message' + (['', 's'][foundMsgids > 1]) + ' in ' + fileName
    
    untranslatedMsgidList = []
    for key in untranslatedMsgidDict.keys():
        if (key != '#') and \
               ((not SKIP_DICT.has_key(key)) or
                SKIP_DICT[key] != untranslatedMsgidDict[key][0]):
            untranslatedMsgidList.append(key)
            
    if not untranslatedMsgidList:
        #~ print 'No untranslated messages that are not in your skip dictionary.'
        True
    else:
        print 'Untranslated messages that are not in your skip dictionary:\n'
        for key in untranslatedMsgidList: 
            print '#: ' + ', '.join(untranslatedMsgidDict[key])
            print '# Original: '
            print '#msgid "' + str(key) + '"'
            print '#msgstr ""\n'
            

if __name__ == "__main__":
    locale.setlocale( locale.LC_ALL, "" )
    srcDir = (sys.argv[1:] and sys.argv[1]) or u'.'
    findUntranslatedMessages(srcDir)
        
