import tools
# 1----importamos las clases que necesitamos
from tools import PresentationCreator, PDFReader, InfoConverter, openai_langchain
#from texto_presentacion import TextoPresentacion  
import openai
import tools
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain, SimpleSequentialChain

class Application:
    def __init__(self):
        #2---instanciamos las clases que necesitamos
        self.presentation_creator = PresentationCreator() # Create an instance of the PresentationCreator class
        self.pdf_reader = PDFReader()
        #self.texto_presentacion = TextoPresentacion(api_key=tools.API_KEY)  # Replace with actual API_KEY or a way to input it.
        self.info_converter = InfoConverter() # Create an instance of the InfoConverter class
        self.llmlc = openai_langchain()
    

    def cadena(self, data):
        
        cantslides = data['cantidad']
        prompt = PromptTemplate(
            input_variables=["tema", "cantidad"],
            template='''
                Generame {cantidad} parrafos sobre el tema {tema}. máximo 70 palabras por parrafo.
                Salida un diccionario de python por cada parrafo. Colocar los diccionarios en una lista de python con el siguiente formato:
                "title": aquí debes generar un titulo acorde al parrafo, "content": "aquí colocar el parrafo"
            '''
        )
        
        cadena = LLMChain(llm=self.llmlc.openai_lc(), prompt=prompt)
        #print(cadena)
        #tipo de dato cadena
        #print(type(cadena))
        return cadena.run(data)


    def menu(self):
        print("1. Texto a presentación")
        print("2. Pdf a presentación")
        print("3. Web a presentación")
        print("5. Salir")
    
    def texto_a_presentacion(self):
        texto = input("Ingresa el tema: ")
        slides = int(input("Ingresa la cantidad de slides: "))
        #tomo el texto que envia texto_presentacion.cadena y lo convierto a una lista de python con el metodo convertir_info
        dataslide = self.info_converter.convertir_info(self.cadena({'tema': texto, 'cantidad': slides}))
        #ahora lo ponemos la cantidad de slides que el usuario ingreso
        dataslide = list(dataslide)[:slides] # convertir a lista y tomar los primeros slides
        print(type(dataslide))
        print(dataslide)
        input("Presiona enter para generar presentación con el texto mostrado...")
        self.presentation_creator.crear_presentacion(dataslide)
        
   
    def pdf_a_presentacion(self):
        pass  # Implement the logic here

    def web_a_presentacion(self):
        pass  # Implement the logic here
    
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
