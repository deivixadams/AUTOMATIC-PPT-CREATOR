# 1----importamos las clases que necesitamos
from tools import PresentationCreator, LeerPDF, InfoConverter, openai_langchain, WebReader
from langchain import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate


#import tools
#from texto_presentacion import TextoPresentacion  
#import openai
#import tools
#from langchain.chat_models import ChatOpenAI
#from langchain.llms import OpenAI

class Application:
    def __init__(self):
        #2---instanciamos las clases que necesitamos
        self.presentation_creator = PresentationCreator() # Create an instance of the PresentationCreator class
        self.pdf_reader = LeerPDF() # Create an instance of the LeerPDF class
        #self.texto_presentacion = TextoPresentacion(api_key=tools.API_KEY)  # Replace with actual API_KEY or a way to input it.
        self.info_converter = InfoConverter() # Create an instance of the InfoConverter class
        self.llmlc = openai_langchain() # Create an instance of the openai_langchain class
        self.web_reader = WebReader() # Create an instance of the WebReader class
    

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




    def menu(self):
        print("1. Texto a presentación")
        print("2. Pdf a presentación")
        print("3. Web a presentación")
        print("5. Salir")
    
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
        
    def pdf_a_presentacion(self):
        pass  # Implement the logic here
   


    # creando una presentación desde una página web
    '''
    Estrategia:
    1. Solicitar la URL de la página web    
    2. Obtener el texto de la página web
    3. Sacar el título de la página web
    4. Resumir todo el texto de la página web con el llm
    5. Verificar cantidad de parrafos y mostrarlos al usuario
    6. Preguntar si está de acuerdo con el texto
    7. Si está de acuerdo, crear la presentación3
    8. Si no está de acuerdo, volver al paso 1    
    '''
    
    def web_a_presentacion(self):
        #url = input("Ingresa la url ")
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
            self.texto_a_presentacion() 



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


if __name__ == "__main__":
    app = Application() # Create an instance of the Application class
    app.run() # Run the application
