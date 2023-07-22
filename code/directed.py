'''
author: John Hoeksema
date:   Nov 23 2020

artists = {
    'uri': {
        'name': string,
        'searched': boolean
    }
    ...
}

collabs = {
    'uri': {
        'uri': integer
    }
    ...
}
'''

from configparser import ConfigParser
from argparse import ArgumentParser
import spotipy
import spotipy.oauth2 as oauth2
import pprint
import pickle
from datetime import datetime

def get_spotify():
    config = ConfigParser()
    config.read("../data/config.cfg")
    client_id = config.get('SPOTIFY', 'CLIENT_ID')
    client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')

    auth = oauth2.SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )

    token = auth.get_access_token()
    spotify = spotipy.Spotify(auth=token)
    return spotify

def artist_searched(artists, uri):
    artists[uri]['searched'] = 1
    return artists

def get_unsearched_artists(artists):
    unsearched = []
    
    for uri in artists.keys():
        if artists[uri]['searched'] == 0:
            unsearched.append(uri)

    return unsearched

def initialize_artist(spotify, artists, collabs, uri):
    
    artist = spotify.artist(uri)
    name = artist['name']
    artist_info = {'searched': 0, 'name': name}
    
    artists[uri] = artist_info
    collabs[uri] = {}

    return artists, collabs

'''
the main fn doing things

DESCRIPTION:
    takes in artist uri, gets a list of that artist's albums, gets a list of tracks from each album, and gets any collabed artists on that track
INPUTS:
    (string) artist uri
OUTPUTS:
    (list of strings) artist uris that initial artist has collabed with
'''
def get_collab_uris(spotify, uri):

    collabs = []

    # load albums into albums dict
    results = spotify.artist_albums(uri, album_type='album')
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    # for each album, get tracks
    for album in albums:
        
        # load tracks into tracks dict
        results = spotify.album_tracks(album['id'])
        tracks = results['items']
        while results['next']:
            results = spotify.next(results)
            tracks.extend(results['items'])
        
        # for each track, get collabed artists
        for track in tracks:
            for artist in track['artists']:
                
                '''
                make sure artist is different artist from artist being searched for
                '''
                if artist['uri'] != uri:
                    collabs.append(artist['uri'])

    return collabs

def pickle_save(dictionary, filename):
    with open(filename, 'wb') as handle:
        pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)
    handle.close()

def main(args):

    pp = pprint.PrettyPrinter(indent=4)

    # establish spotify connection
    spotify = get_spotify()

    # initialize dicts to hold data
    artists = {}
    collabs = {}

    # initialize central artist
    artists, collabs = initialize_artist(spotify, artists, collabs, args.uri)
    
    # perform collab searches
    for i in range(args.depth):

        artist_uris = get_unsearched_artists(artists)
        num_artists = len(artist_uris)
        artists_processed = 0
        for artist_uri in artist_uris:

            percent = artists_processed / num_artists

            collab_uris = get_collab_uris(spotify, artist_uri)
            for collab_uri in collab_uris:

                # Q: does this collaborator exist yet?
                if collab_uri not in artists.keys():
                    artists, collabs = initialize_artist(spotify, artists, collabs, collab_uri)

                    collab_name = artists[collab_uri]['name']
                    artist_name = artists[artist_uri]['name']
                    print("d:{}\t{:.0%}\t{} collaborated with {}".format(i, percent, collab_name.ljust(40), artist_name))

                # Q: has the artist collaborated with the collaborator before?

if collab_uri not in collabs[artist_uri].keys():
                    collabs[artist_uri][collab_uri] = 0

                # The artist has worked with the collaborator on one more track
                collabs[artist_uri][collab_uri] += 1

            # save progress, artist has been fully searched
            pickle_save(artists, '../data/artists.pickle')
            pickle_save(collabs, '../data/collabs.pickle')
            artists = artist_searched(artists, artist_uri)
            artists_processed += 1

    pp.pprint(artists)
    pp.pprint(collabs)

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument("-d", "--depth", type=int, default=1, help="The depth of the connection search")
    parser.add_argument("-u", "--uri", type=str, required=True, help="The rapper uri to begin the search with")

    main(args = parser.parse_args())
