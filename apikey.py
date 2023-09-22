
import openai

'''
    https://python.langchain.com/docs/modules/model_io/models/llms/integrations/huggingface_hub
'''

API_KEY = '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'
SERPER_KEY = 'e8644d7bc36c8d548e0a3e8813a8827d3083933f09fb742a784cbcce84e0f901'


def completion(texto):
    #pass
    #return texto
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=
        [
            {
                "role" : "user", 
                "content" : texto            
            }
        ]
    )
    
    return completion.choices[0].message["content"].strip()
