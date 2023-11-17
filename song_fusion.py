import os
import re
import time
import requests
import openai
import threading
from tqdm import tqdm
from queue import Queue

def get_lyrics_song(artist, song):
    url_id = "https://genius-song-lyrics1.p.rapidapi.com/search/"
    querystring = {"q": f'{artist} {song}', "per_page": "10", "page": "1"}
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
            url_song = "https://genius-song-lyrics1.p.rapidapi.com/song/lyrics/"
            lyrics_query = {"id": f'{id_song}', "text_format": "plain"}
            response = requests.get(url_song, headers=headers, params=lyrics_query)
            
            if response.status_code == 200:
                text_data = response.json()
                lines = text_data.get('lyrics', {}).get('lyrics', {}).get('body', {}).get('plain')
                lyrics = [line for line in lines.split('\n') if not re.match(r'^\[', line.strip())]
                return '\n'.join(lyrics)
    
    handle_error_response(response)

def get_fullname_song(artist, song):
    url_id = "https://genius-song-lyrics1.p.rapidapi.com/search/"
    querystring = {"q": f'{artist} {song}', "per_page": "10", "page": "1"}
    headers = {
        "X-RapidAPI-Key": "e14043395bmsh9164d69ed0c83c7p14d243jsn89be3b418aaf",
        "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
    }
    response = requests.get(url_id, headers=headers, params=querystring)
    
    if response.status_code == 200:
        data = response.json()
        hits = data.get('hits', [])
        if hits:
            return hits[0].get('result', {}).get('full_title')
    
    handle_error_response(response)

def handle_error_response(response):
    data = response.json()
    error = data.get('message')
    print("El error obtenido es de tipo:", response.status_code)
    print("Mensaje:", error)

def translate_lyrics(lyrics, tar_lang):
    request_params = {
        "model": "text-davinci-002",
        "prompt": f'Translate the following text into {tar_lang}: {lyrics}',
        "temperature": 0.7,
        "max_tokens": 2500,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    response = openai.completions.create(**request_params)
    lyrics_esp = response.choices[0].text.strip()
    return lyrics_esp

def interval_lines(name_artist, name_song, output_file, lang, progress_queue):
    header = get_fullname_song(name_artist, name_song)
    english_lyrics = get_lyrics_song(name_artist, name_song)

    if english_lyrics is not None:
        spanish_lyrics = translate_lyrics(english_lyrics, lang)
        interleaved_lines = [header, '']

        for eng_line, esp_line in zip(english_lyrics.split('\n'), spanish_lyrics.split('\n')):
            if eng_line == '':
                interleaved_lines.extend(['---------------', ''])
            else:
                interleaved_lines.extend([eng_line.strip(), esp_line.strip(), ''])

        # Obtener la ruta completa del archivo de salida
        output_folder = "songs"  # Puedes cambiar esto al nombre que prefieras
        os.makedirs(output_folder, exist_ok=True)  # Crear la carpeta si no existe
        output_path = os.path.join(output_folder, output_file)

        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.write('\n'.join(interleaved_lines))

        print(f'Se creó satisfactoriamente el documento en: {output_path}')
    else:
        print('No se pudo obtener la letra de la canción desde la API.')

    # Establecer el estado del hilo de la barra de progreso como completo
    progress_queue.put("Complete")

def progress_bar_thread(progress_queue):
    n = 30
    with tqdm(total=n, desc='Progress', unit='iteration') as pbar:
        for i in range(n + 1):
            time.sleep(0.2)
            pbar.update(1)
        progress_queue.put("Complete")  # Marcar como completo al finalizar

# Solicitar al usuario el nombre del artista
print("What's the name of the artist?")
name_artist = input('>')

# Solicitar al usuario el nombre de la canción
print("What's the name of the song?")
name_song = input('>')

# Solicitar al usuario el nombre del archivo de salida
print('The name of your output file is "lyrics_..."')
output_file = "lyrics_" + input('>') + ".txt"

openai.api_key = "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"
lang = "es"

# Crear una cola para comunicar el progreso
progress_queue = Queue()

# Crear un hilo para la barra de progreso
progress_thread = threading.Thread(target=progress_bar_thread, args=(progress_queue,))
progress_thread.start()

# Ejecutar la función interval_lines en el hilo principal
interval_lines(name_artist, name_song, output_file, lang, progress_queue)

# Esperar a que ambos hilos completen su ejecución
progress_thread.join()
