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
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

# username = "12153812787?si=XgtcvH_tQeisnIe9iK4bBw"

## erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope)
                           # client_id='709ceb7fae174ec1ab706bf842b8e0b7',
                           # client_secret='02408dbdf50c4a62af96cd7337d46a1a',
                           # redirect_uri='http://google.com/')
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

## create spotify object
spotifyObject = spotipy.Spotify(auth=token)

# get current device
devices = spotifyObject.devices()
deviceID = devices['devices'][0]['id']
print(json.dumps(devices, sort_keys=True, indent=4))

# current track info
track = spotifyObject.current_user_playing_track()['item']
# print(json.dumps(track, sort_keys=True, indent=4))
artist = track['artists'][0]
# print("artist " + artist['name'])

if artist != "":
    print("Currently playing " + artist['name'] + " - " + track['name'])


user = spotifyObject.current_user()
# print(json.dumps(user, sort_keys=True, indent=4))

displayName = user['display_name']
followers = user['followers']['total']

# print(json.dumps(VARIABLE, sort_keys=True, indent=4))

while True:
    print()
    print(">>> Welcome to Spotipy" + displayName + "!")
    print(">>> You have " + str(followers) + " followers.")
    print()
    print("0 - Search for an artist")
    print("1 - exit")
    print()
    choice = input("Your choice: ")

    # search for the artist
    if choice == "0":
        print()
        searchQuery = input("Ok, what's their name?: ")
        print()

        # Get search results
        # search(q, limit, offset, type=track, market)
        searchResults = spotifyObject.search(searchQuery, 1, 0, "artist")
        # print(json.dumps(searchResults, sort_keys=True, indent=4))

        # Artist details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print(artist['genres'][0])
        print()
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']

        # Album and track details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract album data
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']
        # print(json.dumps(albumResults, sort_keys=True, indent=4))

        for item in albumResults:
            print("ALBUM " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            # extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z += 1
            print()

        while True:
            songSelection = input("Enter a song number to see the album art and play the song associated with it (x to exit) ")
            if songSelection == "x":
                break
            trackSelectionList = []
            trackSelectionList.append(trackURIs[int(songSelection)])
            spotifyObject.start_playback(deviceID, None, trackSelectionList)
            webbrowser.open(trackArt[int(songSelection)])

    # end program
    if choice == "1":
        break
