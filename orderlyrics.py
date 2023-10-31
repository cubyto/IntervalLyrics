def interleave_lyrics(english_file, spanish_file, output_file, header):
    # Leer el contenido de los archivos de texto
    with open(english_file, 'r', encoding='utf-8') as eng_file, open(spanish_file, 'r', encoding='utf-8') as esp_file:
        english_lines = eng_file.readlines()
        spanish_lines = esp_file.readlines()

    # Crear una lista para almacenar las líneas intercaladas
    interleaved_lines = []

    interleaved_lines.append(header)
    interleaved_lines.append('')
    # Iterar sobre las líneas de los archivos de texto
    for eng_line, esp_line in zip(english_lines, spanish_lines):
        # Agregar las líneas en el orden especificado
        if eng_line == '\n':
            interleaved_lines.append('---------------')
            interleaved_lines.append('')
        else:
            interleaved_lines.append(eng_line.strip())
            interleaved_lines.append(esp_line.strip())
            interleaved_lines.append('')

    # Escribir el resultado en un nuevo archivo de texto
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write('\n'.join(interleaved_lines))

    print('Se creo satisfactoriamente su documento')
# pedimos el titulo
print("What's the name of the artist?")
artist_song = input('>')
print("What's the name of the song?")
title_song = input('>')
header = artist_song + ' - ' + title_song
# Archivos de texto de entrada
english_lyrics_file = 'lyrics_english.txt'
spanish_lyrics_file = 'lyrics_spanish.txt'

# Archivo de texto de salida
output_file = 'interleaved_lyrics.txt'

# Interlevar las letras de las canciones
interleave_lyrics(english_lyrics_file, spanish_lyrics_file, output_file, header)
