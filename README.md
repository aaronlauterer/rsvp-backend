# rsvp-backend

Backend server to handle the RSVP requests from the frontent (not yet available).

## rsvp
Handles RSVPs to invitations. Does work for one event at a time as I built this for my wedding.
 It let's the invitees manage the names of guests and add their phone number and email address.

## Configuration

### Database storage path

The `RSVP_DB_PATH` environment variable determines the path to the sqlite file. Defaults to `/tmp/rsvp.db`.

### Listen IP and HOST

The `RSVP_HOST` environment variable sets the IP on which the API server listens on.

The `RSVP_PORT` environment variable sets the PORT on which the API server listens on.

### Token secret

In order to create a [JWT](https://jwt.io) a secret needs to be set.
The `RSVP_TOKEN_SECRET` environment varialbe is expected and the server will die if it is not set.

### User

In order to manage users who can add, delete and view all invitations we need a file where we store that information.

This is handled by the `RSVP_PW_FILE` environment variable which should store the path to the file containing the users and the password hashes. If not set it defaults to `/tmp/rsvp_pw`.

The file needs to be in the following format:
```json
{
  "user1": "$2a$10$mrufUFDYdBt7oH7vZ7Ock.VRD4/D0YAjtYCMLIiTXxtIa4MSl8Ld.",
  "user2": "$2a$10$diewETIWYo9OU7IQOxGOR.mjMkQMzTAF/5wVuteiCxaUWxQ2T2HI."
}
```
The password hashing algorithm used is __bcrypt__.