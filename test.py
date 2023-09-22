
    '''
        # Agregue una imagen
        image = slide.shapes.add_image(r"C:\imagen.jpg")
        image.width = 500
        image.height = 500
    '''


'''
# definiendo el acceso a la API de OpenAI
llm = OpenAI(model_name=""
        ,openai_api_key = API_KEY
        ,temperature=0.9 #definimos que tan creativo es el modelo. 1 es más creativo, 0 es más conservador
        ,max_tokens=700 #definimos el máximo de tokens que puede generar el modelo
        ,top_p=1 #definimos la probabilidad de que el modelo elija la siguiente palabra. Si es 1, el modelo elige la palabra con la probabilidad más alta. Si es 0, el modelo elige la palabra con la probabilidad más baja.
        ,frequency_penalty=0.4 #definimos la probabilidad de que el modelo repita palabras. Si es 1, el modelo no repite palabras. Si es 0, el modelo repite palabras.  
        )
'''
