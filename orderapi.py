import requests
import re
def get_lyric_song(artist, song):
    #Search the song_id
    url_id = "https://genius-song-lyrics1.p.rapidapi.com/search/"

    querystring = {"q": f'{artist} {song}',"per_page":"10","page":"1"}

    headers = {
	    "X-RapidAPI-Key": "e14043395bmsh9164d69ed0c83c7p14d243jsn89be3b418aaf",
	    "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
    }

    response = requests.get(url_id, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        hits = data.get('hits', [])
        if hits:
            id_song = hits[0].get('result', {}).get('id')

            #Get the lyric with the song_id
            url_song = "https://genius-song-lyrics1.p.rapidapi.com/song/lyrics/"
            lyrics_query = {"id": f'{id_song}',"text_format":"plain"}
            response = requests.get(url_song, headers=headers, params=lyrics_query)
            
            if response.status_code == 200:
                text_data = response.json()
                lines = text_data.get('lyrics', {}).get('lyrics', {}).get('body', {}).get('plain')
                lyrics = lines.split('\n')
                lyrics_old = [line for line in lyrics if not re.match(r'^\[', line.strip())]
                lyrics_new = '\n'.join(lyrics_old)

                print(lyrics_new)
                return lyrics_new
    else:
        data = response.json()
        error = data.get('message')
        print("El error obtenido es de tipo:", response.status_code)
        print("Mensaje: " + error)
        return None


    print('No se pudo obtener la letra desde Genius. Verifica tu clave de API y asegúrate de que la canción y el artista sean correctos.')
    return None

def get_fullname_song(artist, song):
    #Search the full_title
    url_id = "https://genius-song-lyrics1.p.rapidapi.com/search/"

    querystring = {"q": f'{artist} {song}',"per_page":"10","page":"1"}

    headers = {
	    "X-RapidAPI-Key": "e14043395bmsh9164d69ed0c83c7p14d243jsn89be3b418aaf",
	    "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
    }

    response = requests.get(url_id, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        hits = data.get('hits', [])
        if hits:
            full_title = hits[0].get('result', {}).get('full_title')
            print(full_title)
            return full_title
    else:
        data = response.json()
        error = data.get('message')
        print("El error obtenido es de tipo:", response.status_code)
        print("Mensaje: " + error)
        return None

    print('No se pudo obtener la letra desde Genius. Verifica tu clave de API y asegúrate de que la canción y el artista sean correctos.')
    return None

def interval_lines(name_artist, name_song, output_file, spanish_file):
    header = get_fullname_song(name_artist, name_song)
    english_lyrics = get_lyric_song(name_artist, name_song)

    if english_lyrics is not None:
        spanish_lines = []
        with open(spanish_file, 'r', encoding='utf-8') as esp_file:
            spanish_lines = esp_file.readlines()

        interleaved_lines = [header, '']
        
        for eng_line, esp_line in zip(english_lyrics.split('\n'), spanish_lines):
            if eng_line == '':
                interleaved_lines.append('---------------')
                interleaved_lines.append('')
            else:
                interleaved_lines.append(eng_line.strip())
                interleaved_lines.append(esp_line.strip())
                interleaved_lines.append('')

        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write('\n'.join(interleaved_lines))

        print('Se creó satisfactoriamente su documento')
    else:
        print('No se pudo obtener la letra de la canción desde la API.')
        

# The user say the artist
print("What's the name of the artist?")
name_artist = input('>')

# The user say song
print("What's the name of the song?")
name_song = input('>')

# The user say name of the ouput_file
print('The name of your oupuy file is "lyrics_..."' )
output_file = "lyrics_" + input('>') + ".txt"

spanish_lyrics_file = 'lyrics_spanish.txt'
interval_lines(name_artist, name_song, output_file, spanish_lyrics_file)
