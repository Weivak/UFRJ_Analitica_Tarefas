import requests
import json

BASE_URL = 'https://theaudiodb.com/api/v1/json/2/'
URL_API_ALBUM = 'album.php?i={}'
URL_API_ARTIST = 'search.php?s={}'
URL_API_TRACK = 'track.php?m={}'

# Função criada antes da modificação da API
def get_artist_id(artist_name):
    """ 
    Função que retorna o id do artista ao passar o nome 

    Args:
        artist_name (str): nome do artista

    Returns:
        artist_id: id do artista
    """
    artist_name = artist_name.replace(' ', '')
    artist_response = requests.get(f'{BASE_URL}{URL_API_ARTIST.format(artist_name)}')

    artist = artist_response.json()

    artist_id = artist['artists'][0]['idArtist']

    return artist_id

def get_id(artist_name):
    artist_id_by_name = {
        'Coldplay': 111239,
        'Miley Cyrus': 113672,
        'The Weeknd': 112024,
        'Lady Gaga': 111236,
        'Rihanna': 111305,
        'Justin Bieber': 111626,
        'Imagine Dragons': 114415,
        'Drake': 111718,
        'Beyoncé': 114364,
        'Madonna': 111255
    }

    return artist_id_by_name[artist_name]

def get_album(artist_id):  
    """ 
    Função que retorna o nome do album, id do album e ano
    do album mais recente do artista

    Args:
        artist_id (int): id do artista

    Returns:
        album_name: nome do album
        album_id: id do album
        album_year: ano do album
    """
    response = requests.get(f'{BASE_URL}{URL_API_ALBUM.format(artist_id)}')
    album_response = response.json()

    # o ultimo resultado é o album mais recente, dessa forma não é necessário ordenar
    for album in album_response['album']:
        if album['strReleaseFormat'] == 'Album':
            album_name = album['strAlbum']
            album_id = album['idAlbum']
            album_year = album['intYearReleased']

    return album_name, album_id, album_year

def get_tracks(album_id):
    """ 
    Função que retorna todas as músicas de um album

    Args:
        album_id (int): id do album

    Returns:
        track_list: lista com todas as músicas do album
    """
    response = requests.get(f'{BASE_URL}{URL_API_TRACK.format(album_id)}')
    track_response = response.json()
    track_list = []

    for track in track_response['track']:
        track_list.append(track['strTrack'])

    return track_list

def generate_data(artist_name):
    """
    Gera um dicionário com os dados do artista

    Args:
        artist_name (str): nome do artista

    Returns:
        data: dicionário com os dados
    """
    try:
        artist_id = get_id(artist_name)
        album_name, album_id, album_year = get_album(artist_id)
        track_list = get_tracks(album_id)

        data = {
            'artist': artist_name,
            'latest-album': album_name,
            'album-year': album_year,
            'album-tracks': track_list
        }

        return data
    except:
        print('Artista não encontrado')
        return None
    
def save_data(artist_name):
    """
    Salva os dados do artista em um arquivo json
    Args:
        artist_name (str): nome do artista
    """
    data = generate_data(artist_name)
    with open('data1.json', 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    artist_name = input('Digite o nome do artista: ')
    # salvando os dados em um arquivo json
    save_data(artist_name)
    print('Dados salvos com sucesso')