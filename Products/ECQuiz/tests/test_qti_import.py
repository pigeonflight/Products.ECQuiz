# -*- coding: utf-8 -*-
#
from os.path import join

from base import ECQTestCase
from Products.ECQuiz.config import *

# find our sample files:
from Products.ECQuiz.tests import GLOBALS

from Globals import package_home
PACKAGE_HOME = package_home(GLOBALS)
SINGLE_MCQ_QTI_PACKAGE = join(PACKAGE_HOME, 'samples', 'single_mc_nopath.zip')
MCQ_QTI_PACKAGE_WITH_PATHNAMES = join(PACKAGE_HOME, 
                                      'samples', 
                                      'single_mc_withpath.zip')


class testQTIImporter(ECQTestCase):
    """ verify the functionality of the QTI importer
    """
    
    def afterSetUp(self):
        """ create a few users and an empty quiz
        """        
        ECQTestCase.afterSetUp(self)
        self.membership = self.portal.portal_membership
        self.membership.addMember('member', 'secret', ['Member'], [])
        self.membership.addMember('manager', 'secret', ['Manager'], [])
        self.login('manager')
        self._dummy = self.createEmptyQuiz()
    
    
    def testImportSingleMCQestion(self):
        """ verify that importing a small-profile Multiple-choice quiz works as expected
        """
        # at first, the test is empty and has no title
        self.failUnless(self._dummy.isEmpty(), 'The test is not empty and it should be')
        self.failIf(self._dummy.Title(), 'The test has a title and it should not yet have one')
        
        # we import a one-question quiz
        my_quiz_import = open(SINGLE_MCQ_QTI_PACKAGE, 'r')
        added = self._dummy.processQTIImport(my_quiz_import)
        
        # we should have a single question and a title as well as a single image resource
        self.failIf(self._dummy.isEmpty(), 'the test should have a question but it is empty')
        expected_title = 'Example Contentpackage with QTI v2.0 items'
        self.failUnlessEqual(self._dummy.Title(), expected_title,
                            'Incorrect Title after QTI Import')
        num_q = len(self._dummy.getAllQuestions())
        self.failUnlessEqual(num_q, 1,
                            'wrong number of questions imported %d' % num_q)
        
        expected_img_id = 'sign.png'
        quiz_contents = self._dummy.getFolderContents()
        self.failUnless(expected_img_id in [obj.id for obj in quiz_contents],
                        'expected image %s not found in quiz folder' % expected_img_id)
        self.failUnless('Image' in [obj.portal_type for obj in quiz_contents],
                        'expected portal type "Image" not found in quiz folder')
    
    
    def testImportSingleMCQestionWithPathsInZip(self):
        """ if the incoming zip file has pathnames in it, can we still import
            the QTI package?
        """
        # at first, the test is empty and has no title
        self.failUnless(self._dummy.isEmpty(), 'The test is not empty and it should be')
        self.failIf(self._dummy.Title(), 'The test has a title and it should not yet have one')
        
        # we import a one-question quiz
        my_quiz_import = open(MCQ_QTI_PACKAGE_WITH_PATHNAMES, 'r')
        added = self._dummy.processQTIImport(my_quiz_import)
        
        # we should have a single question and a title as well as a single image resource
        self.failIf(self._dummy.isEmpty(), 'the test should have a question but it is empty')
        expected_title = 'Example Contentpackage with QTI v2.0 items'
        self.failUnlessEqual(self._dummy.Title(), expected_title,
                            'Incorrect Title after QTI Import')
        num_q = len(self._dummy.getAllQuestions())
        self.failUnlessEqual(num_q, 1,
                            'wrong number of questions imported %d' % num_q)
        
        expected_img_id = 'sign.png'
        quiz_contents = self._dummy.getFolderContents()
        self.failUnless(expected_img_id in [obj.id for obj in quiz_contents],
                        'expected image %s not found in quiz folder' % expected_img_id)
        self.failUnless('Image' in [obj.portal_type for obj in quiz_contents],
                        'expected portal type "Image" not found in quiz folder')





def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite(makeSuite(testQTIImporter))
    return suite
    