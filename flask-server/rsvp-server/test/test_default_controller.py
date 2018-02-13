# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from rsvp-server.models.error import Error  # noqa: E501
from rsvp-server.models.invitation import Invitation  # noqa: E501
from rsvp-server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_add_invite(self):
        """Test case for add_invite

        adds an invitation
        """
        invitation = Invitation()
        response = self.client.open(
            '/aaron-lauterer/rsvp/1.0.0/invitation',
            method='POST',
            data=json.dumps(invitation),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_invites(self):
        """Test case for get_all_invites

        get all invitations
        """
        response = self.client.open(
            '/aaron-lauterer/rsvp/1.0.0/allinvites',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_invite(self):
        """Test case for get_invite

        get invitation
        """
        query_string = [('id', 'id_example')]
        response = self.client.open(
            '/aaron-lauterer/rsvp/1.0.0/invitation',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_invite(self):
        """Test case for update_invite

        update invitation
        """
        updateinvitation = Invitation()
        response = self.client.open(
            '/aaron-lauterer/rsvp/1.0.0/updateinvite',
            method='POST',
            data=json.dumps(updateinvitation),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
