import json

class InfoConverter:
    def convertir_info(self, info):
        try:
            return json.loads(info)
        except json.JSONDecodeError:
            print("La cadena no está en un formato JSON válido.")
