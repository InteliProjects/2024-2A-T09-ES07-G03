import textwrap
import google.generativeai as genai
import os
import json

LLM_API_KEY = os.getenv("LLM_API_KEY")

class Llm():

    def __init__(self):        
        genai.configure(api_key=LLM_API_KEY)

        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def interpret_lrr(self, text): 

        #    Converta a lista de textos para uma única string, caso `text` seja uma lista
        if isinstance(text, list):
            text = "\n".join(text)

        response = self.model.generate_content(
        textwrap.dedent("""\                
            Agora você faz parte de uma equipe de Compliance de um banco para ajudar a entender as novas regulamentações.                                            
            
            Por favor, retorne JSON descrevendo lrr (Legal, Regulatório e de Risco) usando o seguinte esquema:
            
            ENUM ('oficio', 'comunicado', 'instrucao normativa', 'resolucao', 'informe')

            {"publication_date": date, "effective_date": date, "lrr_type": enum, "lrr_explanation": string, "regulator": string, "repealed_lrr": boolean}

            Exemplo de output: {
            "regulator": "B3",
            "publication_date": "2024-09-25",
            "effective_date": "2024-10-01",
            "lrr_type": "comunicado"
            "lrr_explanation": "Regulamentação sobre áreas protegidas.",
            "repealed_lrr": false
            }

            Seja direto e preciso na explicação do documento. No máximo uma frase.

            Responda em PT-BR.

            Todos os campos são necessários.

            Importante: Retorne apenas um JSON válido.

            Aqui está o texto do documento:

            """) + text,
        generation_config={'response_mime_type':'application/json'}
        )

        json_str = response._result.candidates[0].content.parts[0].text

    # Converte a string JSON para um objeto Python
        json_obj = json.loads(json_str)
        formatted_response = json.dumps(json_obj, indent=4, ensure_ascii=False)

        return formatted_response    

    def tagging(self, text, tags): 

        if isinstance(text, list):
            text = "\n".join(text)

        response = self.model.generate_content(
        textwrap.dedent(f"""\                
            Agora você faz parte de uma equipe de Compliance de um banco para ajudar a entender as novas regulamentações.                                            
            
            Dado essas tags pré selecionadas: {tags}, selecione as tags que estão relacionada ao texto: {text}, e retorne em um array usando o seguinte esquema:
            
            [tag1, tag5, tag9]

            Retorne no mínimo uma tag, dessas 

            Importante: Retorne apenas um array válido.
            """) + text,
        generation_config={'response_mime_type':'application/json'}
        )

        array_str = response._result.candidates[0].content.parts[0].text

        return array_str    
