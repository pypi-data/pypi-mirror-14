# -*- coding: utf-8 -*-
from collections import defaultdict

import re


class PloneAPIChecker(object):
    name = 'flake8_plone_api'
    version = '0.1'
    message = 'P001 found "{0}" consider replacing it with: {1} ' \
              '(since plone.api version {2})'

    character = re.compile(r'\w')

    def __init__(self, tree, filename):
        self.filename = filename
        self.mapping = PloneAPIChecker._get_mapping()

    def run(self):
        with open(self.filename) as f:
            lines = f.readlines()

            for lineno, line in enumerate(lines, start=1):
                for old_approach in self.mapping['data']:
                    found = self.check_line(line, old_approach)
                    if found != -1:
                        new = self.mapping['data'][old_approach]
                        msg = self.message.format(
                            old_approach,
                            ' or '.join(new),
                            self.mapping['since'][new[0]]
                        )
                        yield lineno, found, msg, type(self)

    def check_line(self, line, old_approach):
        found = line.find(old_approach)
        if found == -1:
            return found

        # Check if our found term is already at the end of the line.
        # Then further checks are not necessary
        next_character_position = found + len(old_approach) + 1
        if next_character_position >= len(line):
            return found

        # check that the method is not a substring of another
        # method, i.e getSite and getSiteManager
        next_character = line[next_character_position]
        if self.character.search(next_character) is not None:
            return -1

        return found

    @staticmethod
    def _get_mapping():
        """Create a mapping between old usages that can be replaced by plone.api

        It basically reverses DATA (see below) so that each old approach will
        be a key in the resulting dictionary and all plone.api method calls
        that can be a potential replacement are listed as its value. i.e.

            {'getToolByName': ['plone.api.portal.get_tool']

        DATA variable is meant to be an easy way to add replacements.
        The output of this function is meant to be an easy way to find those
        replacements.
        """
        mapping = {
            'data': defaultdict(list),
            'since': {},
        }

        for api_method in DATA:
            method_call = 'plone.api.{0}'.format(api_method)
            for old_approach in DATA[api_method]['replace']:
                # do not add the empty entries
                if old_approach is None:
                    continue
                mapping['data'][old_approach].append(method_call)
                mapping['since'][method_call] = DATA[api_method]['since']

        return mapping


DATA = {
    'content.create': {
        'since': '1.0',
        'replace': [
            'invokeFactory(',
            'createContentInContainer(',
        ],
    },
    'content.get': {
        'since': '1.0',
        'replace': [
            'restrictedTraverse(',
        ],
    },
    'content.move': {
        'since': '1.0',
        'replace': [
            'manage_cutObjects(',
            'manage_pasteObjects(',
        ],
    },
    'content.rename': {
        'since': '1.0',
        'replace': [
            'manage_renameObject(',
        ],
    },
    'content.copy': {
        'since': '1.0',
        'replace': [
            'manage_copyObjects(',
        ],
    },
    'content.delete': {
        'since': '1.0',
        'replace': [
            'manage_delObjects(',
        ],
    },
    'content.get_state': {
        'since': '1.0',
        'replace': [
            'getInfoFor(',
        ],
    },
    'content.transition': {
        'since': '1.0',
        'replace': [
            'doActionFor(',
        ],
    },
    'content.get_view': {
        'since': '1.0',
        'replace': [
            None,
        ],
    },
    'content.get_uuid': {
        'since': '1.0',
        'replace': [
            'IUUID(',
        ],
    },
    'content.find': {
        'since': '1.3.3',
        'replace': [
            '.catalog(',
            'searchResults(',
        ],
    },
    'user.create': {
        'since': '1.0',
        'replace': [
            'addMember(',
        ],
    },
    'user.get': {
        'since': '1.0',
        'replace': [
            'getMemberById(',
            'get_member_by_login_name(',
        ],
    },
    'user.get_current': {
        'since': '1.0',
        'replace': [
            'getAuthenticatedMember(',
        ],
    },
    'user.get_users': {
        'since': '1.0',
        'replace': [
            'listMembers(',
            'getGroupMembers(',
        ],
    },
    'user.delete': {
        'since': '1.0',
        'replace': [
            'deleteMembers(',
        ],
    },
    'user.is_anonymous': {
        'since': '1.0',
        'replace': [
            'isAnonymousUser(',
        ],
    },
    'user.get_roles': {
        'since': '1.0',
        'replace': [
            'getRolesInContext(',
            'getRoles(',
            'get_local_roles_for_userid(',
        ],
    },
    'user.get_permissions': {
        'since': '1.0',
        'replace': [
            'checkPermission(',
        ],
    },
    'user.has_permission': {
        'since': '1.3',
        'replace': [
            'checkPermission(',
        ],
    },
    'user.grant_roles': {
        'since': '1.0',
        'replace': [
            'setSecurityProfile(',
            'manage_setLocalRoles(',
        ],
    },
    'user.revoke_roles': {
        'since': '1.0',
        'replace': [
            'setSecurityProfile(',
            'manage_setLocalRoles(',
            'manage_delLocalRoles(',
        ],
    },
    'group.create': {
        'since': '1.0',
        'replace': [
            'addGroup(',
        ],
    },
    'group.get': {
        'since': '1.0',
        'replace': [
            'getGroupById(',
        ],
    },
    'group.get_groups': {
        'since': '1.0',
        'replace': [
            'getGroupsForPrincipal(',
            'listGroups(',
        ],
    },
    'group.delete': {
        'since': '1.0',
        'replace': [
            'removeGroup(',
        ],
    },
    'group.add_user': {
        'since': '1.0',
        'replace': [
            'addPrincipalToGroup(',
        ],
    },
    'group.remove_user': {
        'since': '1.0',
        'replace': [
            'removePrincipalFromGroup(',
        ],
    },
    'group.get_roles': {
        'since': '1.0',
        'replace': [
            'getRoles(',
            'getRolesInContext(',
        ],
    },
    'group.grant_roles': {
        'since': '1.0',
        'replace': [
            'setRolesForGroup(',
            'manage_setLocalRoles(',
        ],
    },
    'group.revoke_roles': {
        'since': '1.0',
        'replace': [
            'setRolesForGroup(',
            'manage_setLocalRoles(',
            'manage_delLocalRoles(',
        ],
    },
    'portal.get': {
        'since': '1.0',
        'replace': [
            'getSite(',
        ],
    },
    'portal.get_navigation_root': {
        'since': '1.0',
        'replace': [
            'getNavigationRootObject(',
        ],
    },
    'portal.get_tool': {
        'since': '1.0',
        'replace': [
            'getToolByName(',
        ],
    },
    'portal.send_email': {
        'since': '1.0',
        'replace': [
            None,
        ],
    },
    'portal.get_localized_time': {
        'since': '1.0',
        'replace': [
            'ulocalized_time(',
        ],
    },
    'portal.show_message': {
        'since': '1.0',
        'replace': [
            'IStatusMessage(',
        ],
    },
    'portal.get_registry_record': {
        'since': '1.0',
        'replace': [
            'IRegistry(',
            '.forInterface(',
        ],
    },
    'portal.set_registry_record': {
        'since': '1.0',
        'replace': [
            'IRegistry(',
            '.forInterface(',
        ],
    },
    'portal.translate': {
        'since': '1.5',
        'replace': [
            '.utranslate(',
        ],
    },
    'portal.get_default_language': {
        'since': '1.5',
        'replace': [
            'default_language',
        ],
    },
    'portal.get_current_language': {
        'since': '1.5',
        'replace': [
            '.Language(',
        ],
    },
    'env.adopt_user': {
        'since': '1.0',
        'replace': [
            'setSecurityManager(',
            'getSecurityManager(',
            'newSecurityManager(',
        ],
    },
    'env.adopt_roles': {
        'since': '1.0',
        'replace': [
            'getSecurityManager(',
        ],
    },
    'env.debug_mode': {
        'since': '1.0',
        'replace': [
            'DevelopmentMode(',
        ],
    },
    'env.test_mode': {
        'since': '1.0',
        'replace': [
            None,
        ],
    },
    'env.plone_version': {
        'since': '1.2',
        'replace': [
            None,
        ],
    },
    'env.zope_version': {
        'since': '1.2',
        'replace': [
            None,
        ],
    },
}
