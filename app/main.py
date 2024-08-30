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
PIXABAY_API_KEY = "45715592-51f10adb612126997b0608f39"

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

    def get_image_urls(self, query, count):
        try:
            url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=photo&per_page={count}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            images = [hit['webformatURL'] for hit in data['hits']]
            return images
        except requests.RequestException as e:
            print(f"Error while fetching images from Pixabay: {e}")
            return []

    def create_presentation(self, tema, cantidad):
        try:
            info = self.prompt_to_ppt(tema, cantidad)
            dataslide = self.info_converter.convertir_info(info)
            dataslide = list(dataslide)[:cantidad]

            image_urls = self.get_image_urls(tema, cantidad)
            
            for i, slide in enumerate(dataslide):

                if i < len(image_urls):
                    slide['image_url'] = image_urls[i]
                else:
                    slide['image_url'] = None
            
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
