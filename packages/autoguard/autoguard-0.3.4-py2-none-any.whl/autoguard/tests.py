# -*- coding: utf-8 -*-
# Copyright (c) Polyconseil SAS. All rights reserved.
# This code is distributed under the two-clause BSD License.

from autoguard.ldap import LDAPRemoteUserBackend

from sentry.models import User, Organization, OrganizationMember
from sentry.testutils import TestCase

class LDAPTestCase(TestCase):

    def test_remote_user_creation(self):
        user = User.objects.create(username='foobar')
        organization = Organization.objects.create(name='some-org')
        LDAPRemoteUserBackend._add_to_all_organizations(user)

        om = OrganizationMember.objects.get(user=user, organization=organization)
        self.assertFalse(om is None)
