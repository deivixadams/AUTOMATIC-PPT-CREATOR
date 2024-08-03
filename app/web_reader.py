import requests
from bs4 import BeautifulSoup
import re

class WebReader:
    def read_web(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                titulos = []
                for titulo in soup.find_all(['h1', 'h2']):
                    if len(titulos) < 1:
                        titulos.append(titulo.get_text())
                    else:
                        break
                titulo_limpio = re.sub('[^0-9a-zA-ZáéíóúÁÉÍÓÚñÑ\s-]+', '', titulos[0])
                titulo_limpio = titulo_limpio.strip()
                elementos_parrafo = [p for p in soup.find_all('p') if not p.find('a')]
                texto_completo = ''
                for elemento in elementos_parrafo:
                    texto_limpio = re.sub('[^0-9a-zA-ZáéíóúÁÉÍÓÚñÑ\s-]+', '', elemento.get_text())
                    texto_completo += texto_limpio + '\n' 
                    texto_completo = texto_completo.strip()[:7000]
                texto_final = """Del texto que te voy a enviar hacer un resumen con las conclusiones más importantes.
                solo utilizar los párrafos que formen oraciones con sentido completo.
                Debes responder en español.""" + titulo_limpio + " " + texto_completo
                return texto_final
            else:
                print("URL inválida, por favor introduzca otra URL")
        except Exception as e:
            print("Ha ocurrido un error al procesar la url:", e)
