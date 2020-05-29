import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError


## Terminal commands to set up my envrionment:
# export SPOTIPY_CLIENT_ID='...'
# export SPOTIPY_CLIENT_SECRET='...'
# export SPOTIPY_REDIRECT_URI='...'

## user ID: 12153812787?si=XgtcvH_tQeisnIe9iK4bBw

## get username from terminal
username = sys.argv[1]
scope = 'playlist-modify-private'
# username = "12153812787?si=XgtcvH_tQeisnIe9iK4bBw"

## erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope)
                           # client_id='709ceb7fae174ec1ab706bf842b8e0b7',
                           # client_secret='02408dbdf50c4a62af96cd7337d46a1a',
                           # redirect_uri='http://google.com/')
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

## create spotify object
spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()
print(json.dumps(user, sort_keys=True, indent=4))

displayName = user['display_name']
follower = user['followers']['total']

# print(json.dumps(VARIABLE, sort_keys=True, indent=4))

