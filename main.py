import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Credenciales de Spotify-API
spotify_id = os.environ.get('SPO_ID')
spotify_secret = os.environ.get('SPO_SK')

# Conexion con la API de Spotify.
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_id, client_secret=spotify_secret))

meta = ['name', 'album', 'artists', 'release_date', 'duration_ms', 'popularity']
features = ['danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness',
            'loudness', 'speechiness', 'key', 'mode', 'valence', 'tempo', 'time_signature']


def horasMinutosSegundos(ms):
    """ Metodo de conversion de milisegundos a formato H:M:S """
    return "{:02}:{:02}:{:02}".format(int((ms / 1000.0 / 3600) % 100),
                                      int((ms / 1000.0 / 60) % 60),
                                      int(ms / 1000.0 % 60))


def getTracksIdAlbum(album):
    """ Metodo que genera la lista de ids de canciones por album """
    return [item['id'] for item in sp.album(album)['tracks']['items']]


def getTracksIdPlaylist(pl):
    """ Metodo que genera la lista de ids de canciones por playlist """
    return [item['track']['id'] for item in sp.playlist(pl)['tracks']['items']]


def getTrackData(id):
    """ Metodo que obtiene los atributos de una cancion """
    # meta
    get_meta = sp.track(id)
    name = get_meta['name']
    album = get_meta['album']['name']
    artist = get_meta['album']['artists'][0]['name']
    release_date = get_meta['album']['release_date']
    length = horasMinutosSegundos(int(get_meta['duration_ms']))
    popularity = get_meta['popularity']

    # features
    get_features = sp.audio_features(id)
    danceability = get_features[0]['danceability']
    acousticness = get_features[0]['acousticness']
    energy = get_features[0]['energy']
    instrumentalness = get_features[0]['instrumentalness']
    liveness = get_features[0]['liveness']
    loudness = get_features[0]['loudness']
    speechiness = get_features[0]['speechiness']
    key = get_features[0]['key']
    mode = get_features[0]['mode']
    valence = get_features[0]['valence']
    tempo = get_features[0]['tempo']
    time_signature = get_features[0]['time_signature']

    return [name, album, artist, release_date, length, popularity, danceability, acousticness, energy,
            instrumentalness, liveness, loudness, speechiness, key, mode, valence, tempo, time_signature]


def listaTracks(lista_ids):
    """ Genera una lista de canciones con su informacion y """
    return [getTrackData(lista_ids[item]) for item in range(len(lista_ids))]


def crearCSV(dataframe):
    try:
        dataframe.to_csv("spotify.csv", sep=';', encoding='utf-8')
        print("El CSV esta listo.")
    except Exception as e:
        print(e)


if __name__ == '__main__':

    # los_nafta = 'spotify:artist:1yJIRYs4jmlSYNQkWnhWPe'
    nsg = '0ZgTSm1VI55AhE09Nzvv11'
    # playlist = '37i9dQZF1DXagUeYbNSnOA'
    #
    # id_canciones = getTracksIdAlbum(nsg)
    # lista_canciones = listaTracks(id_canciones)
    print(sp.album(nsg)['images'][0]['url'])

    # df = pd.DataFrame(lista_canciones, columns=meta+features)
    # crearCSV(df)
