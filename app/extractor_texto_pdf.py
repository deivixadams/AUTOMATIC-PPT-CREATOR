import fitz  # fitz es el módulo principal de PyMuPDF

class ExtractorTextoPDF:
    def __init__(self, ruta_del_pdf: str, paginas: str):
        self.ruta_del_pdf = ruta_del_pdf
        self.texto = ""
        self.paginas = self.parsear_paginas(paginas)
        self.extraer_texto()

    def parsear_paginas(self, paginas: str):
        lista_paginas = []
        for x in paginas.split(','):
            if '-' in x:
                inicio, fin = map(int, x.split('-'))
                lista_paginas.extend(range(inicio, fin + 1))
            else:
                lista_paginas.append(int(x))
        return sorted(set(lista_paginas))
        
    def extraer_texto(self):
        try:
            doc = fitz.open(self.ruta_del_pdf)
            for num_pagina in self.paginas:
                if num_pagina > doc.page_count:
                    print(f"La página {num_pagina} no existe")
                    continue
                try:
                    pagina = doc.load_page(num_pagina - 1)  # -1 porque las páginas en PyMuPDF comienzan desde 0
                    self.texto += pagina.get_text()
                except Exception as e:
                    print(f"La página {num_pagina} no se puede extraer: {str(e)}")
            doc.close()
        except Exception as e:
            print(f"Ocurrió un error al intentar abrir el PDF: {e}")
        return self.texto
