import connexion
import six

from rsvp_server.models.error import Error  # noqa: E501
from rsvp_server.models.invitation import Invitation  # noqa: E501
from rsvp_server.models.login import Login  # noqa: E501
from rsvp_server import util
import json
from datetime import datetime, timedelta
import sqlalchemy.exc as sexc
import os
import bcrypt
import sys
import jwt

import rsvp_server.db.db as db

s = db.session()

# get toke secret
if 'RSVP_TOKEN_SECRET' in os.environ:
    RSVP_TOKEN_SECRET = os.environ['RSVP_TOKEN_SECRET']
else:
    sys.exit("Need RSVP_TOKEN_SECRET environment variable set!")

# get db path
if 'RSVP_PW_FILE' in os.environ:
    RSVP_PW_FILE = os.environ['RSVP_PW_FILE']
else:
    RSVP_PW_FILE = '/tmp/rsvp_pw'

def check_token():
    if 'Authorization' in connexion.request.headers:
        t = connexion.request.headers['Authorization']
        token = str(t.split()[1])

        try:
            decoded_token = jwt.decode(token.encode(), RSVP_TOKEN_SECRET, algorithms='HS256')
        except jwt.exceptions.DecodeError as error:
            return False

        if decoded_token['exp'] < datetime.utcnow().strftime('%s'):
            return False

        return Truen
    else:
        return False

def add_invite(invitation):  # noqa: E501
    """adds an invitation

    Adds an invitation # noqa: E501

    :param invitation: 
    :type invitation: dict | bytes

    :rtype: None
    """
    if not check_token():
        return 'Access token missing or invalid', 401

    if connexion.request.is_json:
        new_invitation = db.invitation(**connexion.request.get_json())
        try:
            s.add(new_invitation)
            s.commit()
        except sexc.IntegrityError as error:
            s.rollback()
            return 'Invitation with that code already exists', 409
        except Exception as error:
            return error.message, 500

        return 'done', 201

def get_all_invites():  # noqa: E501
    """get all invitations

    Get all invitations # noqa: E501


    :rtype: List[Invitation]
    """
    if not check_token():
        return 'Access token missing or invalid', 401

    invitations = s.query(db.invitation).all()

    return json.dumps([i.serialize for i in invitations])

def get_invite(id):  # noqa: E501
    """get invitation

    Get an invitation  # noqa: E501

    :param id: 
    :type id: str

    :rtype: Invitation
    """
    try:
        invitation = s.query(db.invitation).filter(db.invitation.id == id)
        if invitation.count() == 0:
            return 'No invitiation found.', 404
    except Exception as error:
        return error.message, 500
    return json.dumps(invitation.one().serialize)

def del_invite(delid):  # noqa: E501
    """deletes an invitation

    Deletes an invitation # noqa: E501

    :param delid: 
    :type delid: str

    :rtype: None
    """
    if not check_token():
        return 'Access token missing or invalid', 401

    try:
        s.query(db.invitation).filter(db.invitation.id == delid).delete()
        s.commit()
    except Exception as error:
        return error.message, 500
    return 'done'

def update_invite(updateinvitation=None):  # noqa: E501
    """update invitation

    Updates an invitiation. # noqa: E501

    :param updateinvitation: 
    :type updateinvitation: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        protected_keys = ['id', 'table', 'date']
        data = connexion.request.get_json()

        if s.query(db.invitation).filter(db.invitation.id == data['id']).count() == 0:
            return 'Invitation not found.', 404

        update = {}
        for key, val in data.items():
            if key not in protected_keys:
                update[key] = val
            update['date'] = datetime.utcnow()


        try:
            s.query(db.invitation).filter(db.invitation.id == data['id']).update(update)
            s.commit()
        except Exception as error:
            return error.message, 500
    return 'done'

def login(login=None):  # noqa: E501
    """login admin user

     # noqa: E501

    :param login: 
    :type login: dict | bytes

    :rtype: str
    """

    with open(RSVP_PW_FILE, 'r') as f:
        userlist = json.load(f)


    if connexion.request.is_json:
        login = Login.from_dict(connexion.request.get_json())  # noqa: E501

        if login.user not in userlist:
            return 'Login failed.', 400

        if bcrypt.checkpw(login._pass.encode(), userlist[login.user].encode()):
            payload = {}
            payload['exp'] = (datetime.utcnow() + timedelta(days=2)).strftime('%s')
            payload['sub'] = login.user

            return jwt.encode(payload, RSVP_TOKEN_SECRET, algorithm='HS256').decode()


    return 'Login failed.', 400
