#!/usr/bin/env python3

import connexion
import logging

from rsvp_server import encoder
import os

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'RSVP API'})

    # get host to listen
    if 'RSVP_HOST' in os.environ:
        RSVP_HOST = os.environ['RSVP_HOST']
    else:
        RSVP_HOST = 'localhost'

    # get port to listen
    if 'RSVP_PORT' in os.environ:
        RSVP_PORT = int(os.environ['RSVP_PORT'])
    else:
        RSVP_PORT = 8888

    app.run(port=RSVP_PORT, host=RSVP_HOST)

if __name__ == '__main__':
    main()
