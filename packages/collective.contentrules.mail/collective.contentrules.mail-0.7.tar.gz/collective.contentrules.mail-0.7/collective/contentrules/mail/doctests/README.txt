========
Doctests
========

First create a content rule::

    >>> from zope.component import getUtility
    >>> from plone.contentrules.engine.interfaces import IRuleStorage
    >>> storage = getUtility(IRuleStorage)
    >>> from plone.app.contentrules.rule import Rule
    >>> storage[u'foo'] = Rule()
    >>> rule = self.portal.restrictedTraverse('++rule++foo')
    >>> rule
    <Rule at ...++rule++foo>

Add mail action to this rule::

    >>> from plone.contentrules.rule.interfaces import IRuleAction
    >>> element = getUtility(IRuleAction, name='collective.contentrules.mail.actions.Mail')
    >>> from zope.component import getMultiAdapter
    >>> adding = getMultiAdapter((rule, self.portal.REQUEST), name='+action')
    >>> addview = getMultiAdapter((adding, self.portal.REQUEST), name=element.addview)
    >>> from collective.contentrules.mail.actions.mail import MailAddForm
    >>> isinstance(addview, MailAddForm)
    True

Add a simple mail action with no word substitution::

    >>> addview.createAndAdd(data={
    ...    'model': 'collective.contentrules.mail.model.base',
    ...    'mimetype': 'plain',
    ...    'source': 'foo-source@bar.com',
    ...    'recipients': 'foo@bar.com,bar@foo.com',
    ...    'subject': 'Foo subject',
    ...    'message': 'Foo'})
    >>> basic = rule.actions[0]
    >>> from collective.contentrules.mail.actions.mail import MailAction
    >>> isinstance(basic, MailAction)
    True
    >>> basic.model
    'collective.contentrules.mail.model.base'
    >>> basic.mimetype
    'plain'
    >>> basic.source
    'foo-source@bar.com'
    >>> basic.recipients
    'foo@bar.com,bar@foo.com'
    >>> basic.subject
    'Foo subject'
    >>> basic.message
    'Foo'

Edit this mail action and change message::

    >>> element = getUtility(IRuleAction, name='collective.contentrules.mail.actions.Mail')
    >>> editview = getMultiAdapter((basic, self.portal.REQUEST), name=element.editview)
    >>> from collective.contentrules.mail.actions.mail import MailEditForm
    >>> isinstance(editview, MailEditForm)
    True
    >>> editview.context.message = 'Foo message'
    >>> basic.message
    'Foo message'

Trigger an event using your mail action to send an email::
First create a dummy mail host to simulate mail sent::

    >>> from Products.SecureMailHost.SecureMailHost import SecureMailHost
    >>> class DummySecureMailHost(SecureMailHost):
    ...     meta_type = 'Dummy secure Mail Host'
    ...
    ...     def __init__(self, id):
    ...         self.id = id
    ...         self.sent = []
    ...
    ...     def _send(self, mfrom, mto, messageText, debug=False):
    ...         self.sent.append(messageText)
    ...
    >>> from zope.component import getSiteManager
    >>> sm = getSiteManager(self.portal)
    >>> from Products.MailHost.interfaces import IMailHost
    >>> sm.unregisterUtility(provided=IMailHost)
    True
    >>> dummyMailHost = DummySecureMailHost('dMailhost')
    >>> sm.registerUtility(dummyMailHost, IMailHost)
    >>> mailhost = getUtility(IMailHost)
    >>> isinstance(mailhost, DummySecureMailHost)
    True

Create four users ::

    >>> membership = self.portal.portal_membership
    >>> membership.addMember('dummy', 'secret', 'Manager', [])
    >>> dummy_member = membership.getMemberById('dummy')
    >>> dummy_member.setMemberProperties({'fullname': 'dummy fullname',
    ...                                   'email':'dummy@foo.com'})
    >>> membership.addMember('dummy2', 'secret', 'Contributor', [])
    >>> dummy2_member = membership.getMemberById('dummy2')
    >>> dummy2_member.setMemberProperties({'fullname': 'dummy2 fullname',
    ...                                    'email':'dummy2@foo.com'})
    >>> membership.addMember('dummy3', 'secret', 'Reviewer', [])
    >>> dummy3_member = membership.getMemberById('dummy3')
    >>> dummy3_member.setMemberProperties({'fullname': 'dummy3 fullname',
    ...                                    'email':'dummy3@foo.com'})
    >>> membership.addMember('dummy4', 'secret', 'Editor', [])
    >>> dummy4_member = membership.getMemberById('dummy4')
    >>> dummy4_member.setMemberProperties({'fullname': 'dummy4 fullname',
    ...                                    'email':'dummy4@foo.com'})

Make sure we won't barf on a non-ASCII string.

    >>> self.portal._setProperty('default_charset', 'utf-8')

Then create a dummy folder in portal::

    >>> self.setRoles(('Manager',))
    >>> self.portal.invokeFactory(type_name='Folder', id='folder', title='Foo folder', description='A w\xc3\xb8rd')
    'folder'
    >>> self.portal.folder
    <ATFolder at .../folder>
    >>> self.portal.folder.setCreators(['dummy'])
    >>> self.portal.folder.Creator()
    'dummy'


Assign local roles on dummy folder so we can test our content rule::

    >>> self.portal.folder.manage_setLocalRoles('dummy2', ['Contributor'])
    >>> self.portal.folder.manage_setLocalRoles('dummy3', ['Reviewer'])
    >>> self.portal.folder.manage_setLocalRoles('dummy4', ['Editor'])

And finally execute mail action on this dummy folder::

    >>> from zope.component.interfaces import IObjectEvent
    >>> from zope.interface import implements
    >>> class DummyEvent(object):
    ...     implements(IObjectEvent)
    ...
    ...     def __init__(self, object):
    ...         self.object = object
    ...
    >>> from plone.contentrules.rule.interfaces import IExecutable
    >>> ex = getMultiAdapter((self.portal, basic, DummyEvent(self.portal.folder)), IExecutable)
    >>> ex()
    True
    >>> mail = dummyMailHost.sent[0]

    >>> mail.get('Content-Type')
    'text/plain; charset="utf-8"'
    >>> mail.get('From')
    'foo-source@bar.com'
    >>> mail.get('To')
    'foo@bar.com,bar@foo.com'
    >>> mail.get('Subject')
    '=?utf-8?q?Foo_subject?='
    >>> mail.get_payload(decode=True)
    'Foo message'

Previous email was sent in text/plain but you can change it to text/html::
    >>> basic.mimetype = 'html'
    >>> dummyMailHost.sent = []
    >>> ex = getMultiAdapter((self.portal, basic, DummyEvent(self.portal.folder)), IExecutable)
    >>> ex()
    True
    >>> mail = dummyMailHost.sent[0]
    >>> mail.get('Content-Type')
    'text/html; charset="utf-8"'

Previous email actions were very basic : mail actions provides also word subsitution feature.
Email action uses IEmailReplacer adapter on each triggered event object to extract some variables.

    >>> from collective.contentrules.mail.interfaces import IMailReplacer
    >>> self.setRoles(('Member',))
    >>> replacer = IMailReplacer(self.portal.folder)
    >>> self.failUnless(replacer.id == 'folder')
    >>> self.failUnless(replacer.title == 'Foo folder')
    >>> self.failUnless(replacer.description == 'A w\xc3\xb8rd')
    >>> self.failUnless(replacer.url == 'http://nohost/plone/folder')
    >>> self.failUnless(replacer.relative_url == 'folder')
    >>> self.failUnless(replacer.portal_url == 'http://nohost/plone')
    >>> self.failUnless(replacer.owner_id == 'dummy')
    >>> self.failUnless(replacer.owner_fullname == 'dummy fullname')
    >>> self.failUnless(replacer.contributor_emails == 'dummy2@foo.com')
    >>> self.failUnless(replacer.reviewer_emails == 'dummy3@foo.com')
    >>> self.failUnless(replacer.editor_emails == 'dummy4@foo.com')

Execute email action with word substitution::

    >>> action = MailAction()
    >>> self.portal._updateProperty('email_from_address', 'foo-manager@bar.com')
    >>> action.model = 'collective.contentrules.mail.model.base'
    >>> action.mimetype = 'html'
    >>> action.source = ''
    >>> action.recipients = 'foo@bar.com'
    >>> action.subject = 'New object : "${title}"'
    >>> action.message = 'A <a href="http://foo/${relative_url}">new object</a> has been added by ${owner_fullname}.'
    >>> dummyMailHost.sent = []
    >>> ex = getMultiAdapter((self.portal, action, DummyEvent(self.portal.folder)), IExecutable)
    >>> ex()
    True
    >>> mail = dummyMailHost.sent[0]
    >>> mail.get('Content-Type')
    'text/html; charset="utf-8"'
    >>> mail.get('From')
    '=?utf-8?q?Site_Administrator_?=<foo-manager@bar.com>'
    >>> mail.get('To')
    'foo@bar.com'
    >>> mail.get('Subject')
    '=?utf-8?q?New_object_=3A_=22Foo_folder=22?='
    >>> mail.get_payload(decode=True)
    'A <a href="http://foo/folder">new object</a> has been added by dummy fullname.'
