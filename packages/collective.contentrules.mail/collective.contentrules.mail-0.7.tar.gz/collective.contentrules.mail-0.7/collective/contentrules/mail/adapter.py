# -*- coding: utf-8 -*-
# Copyright (c) 2008 Ingeniweb

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from zope.interface import implements
from zope.component import adapts

from Products.CMFCore.WorkflowTool import WorkflowException
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IDublinCore
from collective.contentrules.mail.interfaces import IMailReplacer


class MailReplacer(object):
    """Provides attributes which can be used in a mail model"""

    implements(IMailReplacer)
    adapts(IDublinCore)

    def __init__(self, context):
        self.context = context
        self.utool = getToolByName(context, "portal_url")
        self.portal = self.utool.getPortalObject()
        self.mtool = getToolByName(context, "portal_membership")
        self.gtool = getToolByName(context, "portal_groups")
        self.wtool = getToolByName(context, "portal_workflow")
        self.acl_users = getToolByName(context, "acl_users")

    def _getRoleEmails(self, roles):
        # Returns a list of emails for users having the specified roles
        # @param roles: Set of roles
        roles = set(roles)
        local_roles = self.acl_users._getAllLocalRoles(self.context)
        emails = []

        for role in roles:
            members = self.acl_users.portal_role_manager.listAssignedPrincipals(role)
            for member_id in members:
                emails += self._getPrincipalEmail(member_id)

        for item_id, item_roles in local_roles.items():
            # Check if local roles has those that we wanted to extract
            if not roles.intersection(item_roles):
                continue

            emails += self._getPrincipalEmail(item_id)

        return set(emails)

    def _getPrincipalEmail(self, principal_id):
        emails = set()
        members = set()
        member = self.mtool.getMemberById(principal_id)

        if member is not None:
            members.add(member)
        else:
            # Member does not exist. Check if it is a group
            group = self.gtool.getGroupById(principal_id)

            if group is not None:
                members = members.union(group.getGroupMembers())

        # Get all emails from fetched members
        for member in members:
            email = member.getProperty('email', None)
            if not email:
                continue

            emails.add(email)

        return emails

    @property
    def owner_emails(self):
        return ", ".join(self._getRoleEmails(['Owner']))

    @property
    def reader_emails(self):
        return ", ".join(self._getRoleEmails(['Reader']))

    @property
    def contributor_emails(self):
        return ", ".join(self._getRoleEmails(['Contributor']))

    @property
    def editor_emails(self):
        return ", ".join(self._getRoleEmails(['Editor']))

    @property
    def reviewer_emails(self):
        return ", ".join(self._getRoleEmails(['Reviewer']))

    @property
    def review_state(self):
        try:
            return self.wtool.getInfoFor(self.context, "review_state")
        except WorkflowException:
            return ''

    @property
    def id(self):
        return self.context.getId()

    @property
    def title(self):
        return self.context.title_or_id()

    @property
    def description(self):
        return self.context.Description()

    @property
    def url(self):
        return self.context.absolute_url()

    @property
    def relative_url(self):
        return self.utool.getRelativeUrl(self.context)

    @property
    def portal_url(self):
        return self.utool()

    @property
    def owner_id(self):
        return self.context.Creator()

    @property
    def owner_fullname(self):
        owner = self.mtool.getMemberById(self.owner_id)

        if owner is None:
            # Owner is not registered in portal_metadata, so fullname can't
            # be retrieved
            return self.owner_id

        # Returns fullname
        return owner.getProperty('fullname')

    @property
    def default_from_email(self):
        return self.portal.getProperty('email_from_address')

    @property
    def default_from_name(self):
        return self.portal.getProperty('email_from_name', 'Administrator')
