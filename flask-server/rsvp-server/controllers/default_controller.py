import connexion
import six

from rsvp-server.models.error import Error  # noqa: E501
from rsvp-server.models.invitation import Invitation  # noqa: E501
from rsvp-server import util


def add_invite(invitation):  # noqa: E501
    """adds an invitation

    Adds an invitation # noqa: E501

    :param invitation: 
    :type invitation: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        invitation = Invitation.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_all_invites():  # noqa: E501
    """get all invitations

    Get all invitations # noqa: E501


    :rtype: List[Invitation]
    """
    return 'do some magic!'


def get_invite(id):  # noqa: E501
    """get invitation

    Get an invitation  # noqa: E501

    :param id: 
    :type id: str

    :rtype: Invitation
    """
    return 'do some magic!'


def update_invite(updateinvitation=None):  # noqa: E501
    """update invitation

    Updates an invitiation. # noqa: E501

    :param updateinvitation: 
    :type updateinvitation: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        updateinvitation = Invitation.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
