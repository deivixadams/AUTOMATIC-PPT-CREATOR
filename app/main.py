from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from presentation_creator import PresentationCreator
from info_converter import InfoConverter
from limpia_texto import LimpiaTexto
from extractor_texto_pdf import ExtractorTextoPDF
from web_reader import WebReader
from typing import List
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import os
import aiofiles
import uuid
import requests

os.environ["OPENAI_API_KEY"] = "sk-proj-HpGwwK5I8PuaYIDKezKXT3BlbkFJpq9tGYo4wcMnX7N9l4Gd"
UNSPLASH_ACCESS_KEY = "a7rydcx5nPWZF6Hu_i9Wi1U_Pzu9bNWz7y4_-rwTwDM"

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PresentationRequest(BaseModel):
    tema: str
    cantidad: int

class PDFRequest(BaseModel):
    ruta_del_pdf: str
    paginas: str

class URLRequest(BaseModel):
    url: str

class Application:
    def __init__(self):
        self.presentation_creator = PresentationCreator()
        self.info_converter = InfoConverter()
        self.limpia_texto = LimpiaTexto()
        self.web_reader = WebReader()
        self.llmlc = self.openai_langchain()

    class openai_langchain:
        def __init__(self):
            self.chat_model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        def openai_lc(self):
            return self.chat_model

    def prompt_to_ppt(self, tema, cantidad):
        prompt_template = PromptTemplate(
            input_variables=["tema", "cantidad"],
            template='''
                Generame {cantidad} parrafos sobre el tema {tema}. máximo 70 palabras por parrafo.
                Salida un diccionario de python por cada parrafo. Colocar los diccionarios en una lista de python con el siguiente formato:
                "title": aquí debes generar un titulo acorde al parrafo, "content": "aquí colocar el parrafo", "image_url": "aquí colocar una URL de una imagen relacionada"
            '''
        )
        cadena = LLMChain(llm=self.llmlc.openai_lc(), prompt=prompt_template)
        return cadena.run({'tema': tema, 'cantidad': cantidad})

    def get_image_url(self, query):
        try:
            url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
            response = requests.get(url)
            response.raise_for_status()  # Esto lanzará una excepción si la solicitud no fue exitosa
            data = response.json()
            return data['urls']['regular']
        except requests.RequestException as e:
            print(f"Error al obtener la imagen de Unsplash: {e}")
            return None

    def create_presentation(self, tema, cantidad):
        try:
            info = self.prompt_to_ppt(tema, cantidad)
            dataslide = self.info_converter.convertir_info(info)
            dataslide = list(dataslide)[:cantidad]

            for slide in dataslide:
                image_url = self.get_image_url(tema)
                if image_url:
                    slide['image_url'] = image_url
            
            filename = f"{uuid.uuid4()}.pptx"
            filepath = os.path.join("RESULTADO", filename)
            self.presentation_creator.crear_presentacion(dataslide, filepath)
            return filepath
        except Exception as e:
            print(f"Error al crear la presentación: {e}")
            raise e

app_instance = Application()

@app.post("/create_presentation", response_class=FileResponse)
async def create_presentation(request: PresentationRequest):
    try:
        filepath = app_instance.create_presentation(request.tema, request.cantidad)
        return FileResponse(filepath, filename=os.path.basename(filepath))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
