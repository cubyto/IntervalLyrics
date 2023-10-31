import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_pdf(input_file, output_file):
    # Leer el archivo de texto
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Crear el objeto Story para agregar los elementos al PDF
    story = []

    # Estilo de párrafo centrado
    styles = getSampleStyleSheet()
    centered_style = styles['Normal']
    centered_style.alignment = 1  # 0-izquierda, 1-centrado, 2-derecha

    # Agregar cada línea del archivo de texto al Story
    lines = content.splitlines()
    for line in lines:
        if line.strip() !='\n':
            story.append(Paragraph(line, centered_style))
            print('hola')
        else:
            story.append(Paragraph('\n'))
            
        
            # Agregar una línea de texto centrada

    # Crear el archivo PDF con el contenido del Story
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    doc.build(story)


# Ruta del archivo de texto generado previamente
input_file = 'interleaved_lyrics.txt'
# Ruta y nombre del archivo PDF de salida
output_file = 'centered_lyrics.pdf'

# Generar el archivo PDF
create_pdf(input_file, output_file)
