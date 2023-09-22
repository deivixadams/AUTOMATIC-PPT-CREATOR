import creappt  # Importa el módulo pptllm.py que necesitas crear.
import PyPDF2
import re
from prompt2text import *
from creappt import crear_presentacion 

def menu():
    print("1. Texto a presentación")
    print("2. Pdf a presentación")
    print("3. Web a presentación")
    print("4. word a presentación")
    print("5. Salir")

def Texto_a_presentacion():
    texto = input("Ingresa el tema: ")
    slides = int(input("Ingresa la cantidad de slides: "))
    dataslide = cadena({'tema':texto, 'cantidad': slides})
    print(dataslide) 
    print("\n"*2)
    input("Presiona enter para generar presentación con el texto mostrado...")
    crear_presentacion(dataslide)


def limpiar_texto(texto):
    # Limpia el texto de caracteres no deseados y lo retorna.
    # Puedes ajustar esto para que se ajuste a tus necesidades.
    pattern = re.compile('[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ.,?!¡¿ ]')
    texto_limpio = pattern.sub('', texto)
    return texto_limpio


def leer_y_limpiar_pdf(ruta_pdf):

    texto = ""
    try:
        with open(ruta_pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                texto += reader.pages[page_num].extract_text()
        texto = limpiar_texto(texto)
    except FileNotFoundError:
        print("Archivo no encontrado")
    return texto

def Pdf_a_presentacion():
    ruta_pdf = input("Ingresa la ruta del PDF: ")
    slides = int(input("Ingresa la cantidad de slides: "))
    # Lee y limpia el contenido del PDF.
    texto = leer_y_limpiar_pdf(ruta_pdf)
    creappt.pdf_a_presentacion(texto, slides)

def Web_a_presentacion():
    pass

def word_a_presentacion():
    pass


def main():
    while True:
        menu()
        opcion = input("Selecciona una opción: ")
        if opcion == '1':
            Texto_a_presentacion()
        elif opcion == '2':
            Pdf_a_presentacion()
        elif opcion == '3':
            Web_a_presentacion()
        elif opcion == '4':
            word_a_presentacion()
        elif opcion == '5':
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()
