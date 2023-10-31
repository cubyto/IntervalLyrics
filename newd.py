def interleave_lyrics(file1, file2, output_file):
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2, open(output_file, 'w', encoding='utf-8') as f_out:
        lyrics1 = f1.read().split('\n\n')
        lyrics2 = f2.read().split('\n\n')
        
        if len(lyrics1) != len(lyrics2):
            print("Error: The files do not have the same number of stanzas.")
            return
        
        for i in range(len(lyrics1)):
            lines1 = lyrics1[i].strip().split('\n')
            lines2 = lyrics2[i].strip().split('\n')
            
            for line1, line2 in zip(lines1, lines2):
                f_out.write(line1 + '\n')
                f_out.write(line2 + '\n')
            
            f_out.write('\n')
            f_out.write('\n')

# Example usage
interleave_lyrics('lyrics_english.txt', 'lyrics_spanish.txt', 'interleaved_lyrics.txt')


# Example usage
