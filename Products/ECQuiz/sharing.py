from zope.interface import implements
from plone.app.workflow.interfaces import ISharingPageRole

DELEGATE_PERM='Manage portal'
try:
    # Plone 3.1x
    from plone.app.workflow import permissions
    DELEGATE_PERM = permissions.DelegateRoles
except:
    # Plone 3.0x
    pass

from Products.CMFPlone import PloneMessageFactory as _

class ECQuizResultGraderRole(object):
    implements(ISharingPageRole)
    
    title = _(u"title_ecq_can_grade", default=u"Can grade")
    required_permission = DELEGATE_PERM

class ECQuizResultViewerRole(object):
    implements(ISharingPageRole)
    
    title = _(u"title_ecq_can_view_results", default=u"Can view results")
    required_permission = DELEGATE_PERM
