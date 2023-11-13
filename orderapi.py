import requests

def get_lyrics_from_genius(artist, title, api_key):
    base_url = 'https://api.genius.com'
    search_url = '/search'
    
    headers = {'Authorization': 'Bearer ' + api_key}
    params = {'q': f'{artist} {title}'}
    
    response = requests.get(base_url + search_url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        hits = data.get('response', {}).get('hits', [])

        if hits:
            song_id = hits[0].get('result', {}).get('id')
            lyrics_url = f'/songs/{song_id}'
            response = requests.get(base_url + lyrics_url, headers=headers)
            
            if response.status_code == 200:
                lyrics_data = response.json()
                lyrics = lyrics_data.get('response', {}).get('song', {}).get('lyrics', {}).get('plain')
                return lyrics

    print('No se pudo obtener la letra desde Genius. Verifica tu clave de API y asegúrate de que la canción y el artista sean correctos.')
    return None

def interleave_lyrics(artist, title, spanish_file, output_file, api_key):
    header = f'{artist} - {title}'
    english_lyrics = get_lyrics_from_genius(artist, title, api_key)

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

# Solicitar al usuario el nombre del artista y la canción
print("What's the name of the artist?")
artist_song = input('>')
print("What's the name of the song?")
title_song = input('>')

# Reemplazar 'TU_CLAVE_DE_API_AQUI' con tu clave de API de Genius
api_key = 'daueY-wzu3AyaLNE4y13kNn2d8Z6UTOu5JO9w-F0bJxvD63cyH3mztVVJvTfQdmq'

# Archivo de texto en español
spanish_lyrics_file = 'lyrics_spanish.txt'

# Archivo de texto de salida
output_file = 'interleaved_lyrics.txt'

# Obtener la letra desde Genius y realizar la intercalación
interleave_lyrics(artist_song, title_song, spanish_lyrics_file, output_file, api_key)

