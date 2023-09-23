import openai
from apikey import API_KEY  # API_KEY
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain import HuggingFaceHub
from langchain import PromptTemplate
#importando librerías de chain
from langchain.chains import LLMChain, SimpleSequentialChain

#leyendo la API_KEY
openai.api_key = API_KEY

llm = ChatOpenAI(model_name="gpt-3.5-turbo"
        ,openai_api_key = API_KEY
        ,temperature=1 #definimos que tan creativo es el modelo. 1 es más creativo, 0 es más conservador
        ,max_tokens=900 #definimos el máximo de tokens que puede generar el modelo
        ,model_kwargs={"top_p": 0.9, "frequency_penalty": 0.4} #definimos la probabilidad de que el modelo elija la siguiente palabra. Si es 1, el modelo elige la palabra con la probabilidad más alta. Si es 0, el modelo elige la palabra con la probabilidad más baja.#definimos la probabilidad de que el modelo repita palabras. Si es 1, el modelo no repite palabras. Si es 0, el modelo repite palabras.  
        )

def cadena(data):
    prompt = PromptTemplate(
    input_variables=["tema", "cantidad"], 
    template=
    '''
        Generame {cantidad} parrafos sobre el tema {tema}. máximo 70 palabras por parrafo.
        Salida un diccionario de python por cada parrafo. Colocar los diccionarios en una lista de python con el siguiente formato:
        "title": aquí debes generar un titulo acorde al parrafo, "content": "aquí colocar el parrafo"
    '''
    )
    cadena = LLMChain(llm=llm, prompt=prompt)
    return cadena.run(data)





