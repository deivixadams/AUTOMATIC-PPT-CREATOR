'''
    "proyecto": "Nombre del Proyecto",
    "autor": "Deivsi Adames",
    "descripcion": "Una aplicación para crear presentaciones desde tres fuentes: modelos de lenguajes, web y PDF.",
    "ano": "2023",
    "licencia": "MIT",
    "contacto": "tu_email@ejemplo.com"
'''


'''
PARTE I - [{importacioens}]
'''
# 1----importamos las clases que necesitamos
from tools import PresentationCreator, ExtractorTextoPDF, InfoConverter, openai_langchain, WebReader
from langchain import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate


class Application:
    def __init__(self):
        #2---instanciamos las clases que necesitamos
        self.presentation_creator = PresentationCreator() # Create an instance of the PresentationCreator class
        #self.pdf_reader = LeerPDF() # Create an instance of the LeerPDF class
        #self.texto_presentacion = TextoPresentacion(api_key=tools.API_KEY)  # Replace with actual API_KEY or a way to input it.
        self.info_converter = InfoConverter() # Create an instance of the InfoConverter class
        self.llmlc = openai_langchain() # Create an instance of the openai_langchain class
        self.web_reader = WebReader() # Create an instance of the WebReader class
        #nota: la de pdf la instancion en el metodo pdf_a_presentacion
        
    

    '''
    PARTE 1 - [{PROMPT PARA LLM A TRAVES DE LANGCHAIN}]
    '''
    def PromptLC_Text2ppt(self, datagpt):
        #cantslides = data['cantidad']
        prompt = PromptTemplate(
            input_variables=["tema", "cantidad"],
            template='''
                Generame {cantidad} parrafos sobre el tema {tema}. máximo 70 palabras por parrafo.
                Salida un diccionario de python por cada parrafo. Colocar los diccionarios en una lista de python con el siguiente formato:
                "title": aquí debes generar un titulo acorde al parrafo, "content": "aquí colocar el parrafo"
            '''
        )
        
        cadena = LLMChain(llm=self.llmlc.openai_lc(), prompt=prompt)
        return cadena.run(datagpt)


    #----------------dataweb--------------------------------
    def PromptLC_Web2ppt(self, dataweb):
        prompt = PromptTemplate(
            input_variables=["tema", "tono"],
            template='''
                Hacer un resumen de {tema} en este tono: {tono}. máximo 70 palabras por parrafo.
                Salida un diccionario de python por cada parrafo. Colocar los diccionarios en una lista de python con el siguiente formato:
                "title": aquí debes generar un titulo acorde al parrafo, "content": "aquí colocar el parrafo"
            '''
        )
        
        cadena = LLMChain(llm=self.llmlc.openai_lc(), prompt=prompt)
        return cadena.run(dataweb)


        #----------------dataPDF--------------------------------
    def PromptLC_PDF2ppt(self, datapdf):
        prompt = PromptTemplate(
            input_variables=["tema"],
            template='''
                Hacer un resumen en español del {tema}. máximo 25 palabras por parrafo.
                Salida un diccionario de python por cada parrafo. Colocar los diccionarios en una lista de python con el siguiente formato:
                "title": aquí debes generar un titulo acorde al parrafo, "content": "aquí colocar el parrafo"
            '''
        )
        
        cadena = LLMChain(llm=self.llmlc.openai_lc(), prompt=prompt)
        return cadena.run(datapdf)
    
    '''
    PARTE 2 - [{Metodos que ejecutan los prompts y crean la presentación desde Modelo, web o pdf}]
    '''

    def texto_a_presentacion(self):
        texto = input("Ingresa el tema: ")
        slides = int(input("Ingresa la cantidad de slides: "))
        #tomo el texto que envia texto_presentacion.cadena y lo convierto a una lista de python con el metodo convertir_info
        dataslide = self.info_converter.convertir_info(self.PromptLC_Text2ppt({'tema': texto, 'cantidad': slides}))
        #ahora lo ponemos la cantidad de slides que el usuario ingreso
        dataslide = list(dataslide)[:slides] # convertir a lista y tomar los primeros slides
        #print(type(dataslide))
        print("_"*50)
        print("\n")
        print("Este es el texto que usaremos en la presentación: \n")
        print(dataslide)
        print("\n"*2)
        estadeacuerdo = input("¿Está de acuerdo con el texto? (s/n):")
        if estadeacuerdo == 's':
            self.presentation_creator.crear_presentacion(dataslide)
        else:
            self.texto_a_presentacion() 
        
    # creando una presentación desde una página web
    def web_a_presentacion(self):
        #url = input("Ingresa la url: ")
        url = "https://es.wikipedia.org/wiki/Python"
        tono = input("Ingresa el tono de la presentación (formal, casual, divertida) ")
        
        #asignamos la data desde a web a una variable:
        dataweb = self.web_reader.read_web(url)
        #print(f"texto desde web sin convertir--->: {dataweb} \n")
        #Enviamos el texto al modelo de lenguaje para que devuelva un resumen en formato json
        dataweb = self.info_converter.convertir_info(self.PromptLC_Web2ppt({'tema': dataweb, 'tono': tono}))

        #El texto leio desde la pagina web debe ser convertido a una lista de diccionarios de python
        #dataweb = self.info_converter.convertir_info(dataweb)
        print("_"*50)
        print("\n")
        print(f"Este es el texto que usaremos en la presentación: {dataweb} \n")
        estadeacuerdo = input("¿Está de acuerdo con el texto? (s/n):")
        if estadeacuerdo == 's':
            self.presentation_creator.crear_presentacion(dataweb)
        else:
            self.web_a_presentacion() 


    def pdf_ruta_paginas(self):
        ruta_del_pdf = input("Ingresar la ruta del pdf: ")
        ruta_del_pdf = r"{}".format(ruta_del_pdf)
        paginas = input("Ingresar las páginas a extraer (ejemplo: 1, 2, 3-5): ")
        #paginas = self.extractor_texto_pdf.convertir_paginas(paginas)
        return ruta_del_pdf, paginas
    
    #pdf a presentación
    
    def pdf_a_presentacion(self):
        ruta_del_pdf, paginas = self.pdf_ruta_paginas()
        self.extractor_texto_pdf = ExtractorTextoPDF(ruta_del_pdf, paginas) # Create an instance of the ExtractorTextoPDF class y le pasamos la ruta del pdf y las paginas
        #Escribir un metodo que reciba un pdf como parametro y extraiga el texto del mismo   
        #exit()
        #asignamos la data desde a web a una variable:
        datapdf = self.extractor_texto_pdf.extraer_texto()
        #print(f"texto desde web sin convertir--->: {dataweb} \n")
        #Enviamos el texto al modelo de lenguaje para que devuelva un resumen en formato json
        datapdf = self.info_converter.convertir_info(self.PromptLC_PDF2ppt({'tema': datapdf}))

        #El texto leio desde la pagina web debe ser convertido a una lista de diccionarios de python
        #dataweb = self.info_converter.convertir_info(dataweb)
        print("_"*50)
        print("\n")
        print(f"Este es el texto que usaremos en la presentación: {datapdf} \n")
        estadeacuerdo = input("¿Está de acuerdo con el texto? (s/n):")
        if estadeacuerdo == 's':
            self.presentation_creator.crear_presentacion(datapdf)
        else:
            self.pdf_a_presentacion()     


    '''
    PARTE 3 - [{Menú y bucle infinito}]
    '''
    def menu(self):
        print("1. Texto a presentación")
        print("2. Pdf a presentación")
        print("3. Web a presentación")
        print("5. Salir")
    
    def run(self):
        while True:
            self.menu()
            opcion = input("Selecciona una opción: ")
            if opcion == '1':
                self.texto_a_presentacion()
            elif opcion == '2':
                self.pdf_a_presentacion()
            elif opcion == '3':
                self.web_a_presentacion()
            elif opcion == '5':
                break
            else:
                print("Opción inválida")


    '''
    PARTE 3 - [{inicio de la aplicación}]
    '''
if __name__ == "__main__":
    app = Application() # Create an instance of the Application class
    app.run() # Run the application
