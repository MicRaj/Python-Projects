# Spotify AdMuter
# by Michal Rajzer

import spotipy
import spotipy.util as util
import time
from pycaw.pycaw import AudioUtilities

# ===============================================SETUP=====================================================

# Spotify IDs
# username = sys.argv[1] from command line

spotifyUsername = ''
spotifyAccessScope = 'user-read-currently-playing user-modify-playback-state'
spotifyClientID = ''
spotifyClientSecret = ''
spotifyRedirectURI = 'http://google.com/'


def setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI):
    token = util.prompt_for_user_token(username, scope, clientID, clientSecret, redirectURI)
    return spotipy.Spotify(auth=token)


def main():
    global spotifyObject

    try:
        trackInfo = spotifyObject.current_user_playing_track()
    except:
        print("Token Expired")
        spotifyObject = setupSpotifyObject(spotifyUsername, spotifyAccessScope, spotifyClientID, spotifyClientSecret,
                                           spotifyRedirectURI)
        trackInfo = spotifyObject.current_user_playing_track()

    try:
        if trackInfo['currently_playing_type'] == 'ad':
            MuteSpotifyTab(True)
        else:
            MuteSpotifyTab(False)
    except TypeError:
        pass


def MuteSpotifyTab(mute):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "Spotify.exe":
            if mute:
                volume.SetMute(True, None)
            else:
                volume.SetMute(False, None)


if __name__ == '__main__':
    spotifyObject = setupSpotifyObject(spotifyUsername, spotifyAccessScope, spotifyClientID, spotifyClientSecret,
                                       spotifyRedirectURI)
    while True:
        main()
        time.sleep(1)
