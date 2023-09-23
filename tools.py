
import json
import os
import re
import nltk
from PyPDF2 import PdfReader
from pptx import Presentation
from pptx.util import Inches
from datetime import datetime
import json
import openai
import tools
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain, SimpleSequentialChain


API_KEY = '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'
SERPER_KEY = 'e8644d7bc36c8d548e0a3e8813a8827d3083933f09fb742a784cbcce84e0f901'



class LimpiaTexto:
    def limpiar_texto(self, texto):
        pattern = re.compile('[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ.,?!¡¿ ]')
        texto_limpio = pattern.sub('', texto)
        return texto_limpio


class openai_langchain:
    def openai_lc(self):
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key= API_KEY,
            temperature=1,
            max_tokens=900,
            model_kwargs={"top_p": 0.9, "frequency_penalty": 0.4}
        )
        return self.llm


class InfoConverter:
    def convertir_info(self, info):
        try:
            return json.loads(info)
        except json.JSONDecodeError:
            print("La cadena no está en un formato JSON válido.")

class PresentationCreator:

    def crear_presentacion(self, info):
        #infojson = self.convertir_info(info)
        print("Creando presentación...\n")
        prs = Presentation()
        ahora = datetime.now()
        fecha_hora = ahora.strftime("fecha-%d-%m-%Y_hora-%H-%M-%S")
        
        for slide_info in info:
            slide_layout = prs.slide_layouts[5]
            slide = prs.slides.add_slide(slide_layout)
            title_box = slide.shapes.title
            title_box.text = slide_info["title"]
            left = Inches(1)
            top = Inches(1.5)
            width = height = Inches(6)
            txBox = slide.shapes.add_textbox(left, top, width, height)
            tf = txBox.text_frame
            p = tf.add_paragraph()
            p.text = slide_info["content"]
        
        nombre_archivo = f"{fecha_hora}.pptx"
        ruta_guardado = os.path.join("RESULTADO", nombre_archivo)
        try:
            prs.save(ruta_guardado)
            if os.path.exists(ruta_guardado):
                print(f"He creado el archivo:{fecha_hora}")
        except PermissionError:
            print("No se pudo crear el archivo, probablemente esté abierto.")


class PDFReader:
    def leer_y_limpiar_pdf(self, ruta_pdf):
        texto = ""
        try:
            with open(ruta_pdf, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    texto += reader.pages[page_num].extract_text()
            texto = self.limpiar_texto(texto)
        except FileNotFoundError:
            print("Archivo no encontrado")
        return texto
        
    def pdf_a_presentacion(self):
        ruta_pdf = input("Ingresa la ruta del PDF: ")
        slides = int(input("Ingresa la cantidad de slides: "))
        texto = self.leer_y_limpiar_pdf(ruta_pdf)
        self.presentation_creator.crear_presentacion(texto, slides)
    
    def leer_libro(self, file_path):
        if not os.path.isfile(file_path):
            print("Error: Libro no encontrado, por favor vuelva a cargar")
            return
        nltk.download('punkt')
        try:
            with open(file_path, "rb") as f:
                pdf_reader = PdfReader(f)
                text = ""
                num_paginas = len(pdf_reader.pages)
                if num_paginas <= 10:
                    cant_paginas_para_parrafo = 1
                else:
                    cant_paginas_para_parrafo = 10

                for page_num in range(len(pdf_reader.pages))[:10]:
                    text += pdf_reader.pages[page_num].extract_text()
                tokens = nltk.sent_tokenize(text)
                num_parrafos = int(num_paginas / cant_paginas_para_parrafo)
                
                for i in range(num_parrafos):
                    inicio = i * cant_paginas_para_parrafo
                    fin = inicio + cant_paginas_para_parrafo
                    texto_parrafo = "".join(tokens[inicio:fin])
                    print(f"Párrafo {i+1}:\n{texto_parrafo}\n")
        except FileNotFoundError:
            print("Error: Libro no encontrado, por favor vuelva a cargar")
