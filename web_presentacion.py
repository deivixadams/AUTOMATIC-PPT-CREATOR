
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain

class WebPresentacion:
    
    def __init__(self, api_key):
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key= api_key,
            temperature=1,
            max_tokens=900,
            model_kwargs={"top_p": 0.9, "frequency_penalty": 0.4}
        )
    
    def cadena(self, data):
        prompt = PromptTemplate(
            input_variables=["tema", "cantidad"],
            template='''
                Generame {cantidad} parrafos sobre el tema {tema}. máximo 70 palabras por parrafo.
                Salida un diccionario de python por cada parrafo. Colocar los diccionarios en una lista de python con el siguiente formato:
                "title": aquí debes generar un titulo acorde al parrafo, "content": "aquí colocar el parrafo"
            '''
        )
        
        cadena = LLMChain(llm=self.llm, prompt=prompt)
        #print(cadena)
        #tipo de dato cadena
        #print(type(cadena))
        return cadena.run(data)
