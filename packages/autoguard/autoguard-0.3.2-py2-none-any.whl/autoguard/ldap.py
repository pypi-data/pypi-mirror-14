# -*- coding: utf-8 -*-
# Copyright (c) Polyconseil SAS. All rights reserved.
# This code is distributed under the two-clause BSD License.
"""SSO using LDAP to get access rights"""

from __future__ import absolute_import, unicode_literals
import logging
import urlparse

from django.conf import settings
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.middleware import RemoteUserMiddleware
import ldap

from sentry.models.organization import Organization
from sentry.models.organizationmember import OrganizationMember, OrganizationMemberTeam
from sentry.models.team import Team
from sentry.models.user import User


class CustomUserHeaderMiddleware(RemoteUserMiddleware):
    header = settings.REMOTE_USER_HTTP_HEADER


class LDAPRemoteUserBackend(RemoteUserBackend):
    @staticmethod
    def ldap_uri_parser(uri):
        parsed = urlparse.urlparse(uri)
        login = parsed.username
        password = parsed.password
        netloc = '{}:{}'.format(parsed.hostname, parsed.port or '').strip(':')

        return (
            urlparse.urlunparse((parsed.scheme, netloc, parsed.path, parsed.params, parsed.query, parsed.fragment)),
            (login, password) if login else None
        )

    def __init__(self):
        self.logger = logging.getLogger('{0}.{1}'.format(__name__, LDAPRemoteUserBackend))
        self.ldap_uri, self.ldap_auth = self.ldap_uri_parser(settings.LDAP['uri'])
        self.user_tpl = settings.LDAP['user_tpl']
        self.member_key = settings.LDAP['member_key']
        self.groups = settings.LDAP['groups']

        self.connection = ldap.initialize(self.ldap_uri)
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)  # connection.set_option does not work ???
        if self.ldap_auth is not None:
            self.connection.simple_bind_s(*self.ldap_auth)

    def _ldap_search(self, base, scope, filterstr='(objectClass=*)', attrlist=None, attrsonly=0):
        try:
            result = self.connection.search_s(base, scope, filterstr=filterstr, attrlist=attrlist, attrsonly=attrsonly)
            return result[0][1]
        except Exception as e:
            self.logger.exception(e)

    def _ldap_user(self, username):
        result = self._ldap_search(
            self.user_tpl.format(username=username),
            ldap.SCOPE_BASE,
            attrlist=[b'mail', b'gecos']
        )
        return {
            'email': result['mail'][0],
            'first_name': result['gecos'][0],
        }

    def _ldap_user_in_group(self, username, group):
        result = self._ldap_search(group, ldap.SCOPE_BASE, attrlist=[self.member_key.encode('UTF-8')])
        members = result[self.member_key]
        user = self.user_tpl.format(username=username)
        return user in members

    def authenticate(self, remote_user):
        if not remote_user:
            return

        try:
            user = User.objects.get(username=remote_user)
        except User.DoesNotExist:
            if not any([self._ldap_user_in_group(remote_user, group) for group in self.groups]):
                return
        user = super(LDAPRemoteUserBackend, self).authenticate(remote_user)
        self._add_to_all_organizations(user)
        return user

    @staticmethod
    def _add_to_all_organizations(user):
        if user is None:
            return

        organizations_to_add = (
            Organization.objects
            .order_by('pk')
            .exclude(members=user)
        )

        for organization in organizations_to_add:
            member, _ = OrganizationMember.objects.get_or_create(
                organization=organization,
                user=user,
                defaults={
                    'role': 'admin',
                }
            )
            teams = Team.objects.filter(organization=organization)
            for team in teams:
                OrganizationMemberTeam.objects.get_or_create(
                    team=team,
                    organizationmember=member,
                    is_active=True,
                )

    def configure_user(self, user):
        # Add email and name to user
        ldap_user_attr = self._ldap_user(user.username)
        for key, value in ldap_user_attr.items():
            setattr(user, key, value)
        user.save()

        return user
