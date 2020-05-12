# Spotify AdMuter
# by Michal Rajzer

import spotipy
import spotipy.util as util
import time
from pycaw.pycaw import AudioUtilities
from pygame import mixer

# Need To Quieten the pink2.wav

# ===============================================SETUP=====================================================

# Spotify IDs

[spotifyUsername, spotifyClientID, spotifyClientSecret] = [line.strip('\n') for line in
                                                           open('SpotifyCred.txt', 'r').readlines()]

spotifyAccessScope = 'user-read-currently-playing user-modify-playback-state'
spotifyRedirectURI = 'http://google.com/'
mixer.init(96000, 16, 2, 1024)


def setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI):
    token = util.prompt_for_user_token(username, scope, clientID, clientSecret, redirectURI)
    return spotipy.Spotify(auth=token)


def main():
    global spotifyObject
    global playWav

    try:
        trackInfo = spotifyObject.current_user_playing_track()
    except:
        print("Token Expired")
        spotifyObject = setupSpotifyObject(spotifyUsername, spotifyAccessScope, spotifyClientID, spotifyClientSecret,
                                           spotifyRedirectURI)
        trackInfo = spotifyObject.current_user_playing_track()

    try:
        if trackInfo['currently_playing_type'] == 'ad':
            if not playWav:
                MuteSpotifyTab(True)
                print("Playing pink panther")
                mixer.music.load('PinkPanther.wav')
                mixer.music.play()
                playWav = True
        else:
            MuteSpotifyTab(False)
            if playWav:
                print("Stopping pink panther")
                mixer.music.stop()
                playWav = False

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
    playWav = False
    while True:
        main()
        time.sleep(1)
