from openai import OpenAI
import json


client = OpenAI(api_key="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", base_url="https://openrouter.ai/api/v1")


# response = client.responses.create(
def obtener_info_rut(texto_plano):
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": f"""
                Eres un experto en análisis de documentos RUT de la DIAN y de la Camara de Comercio. Extrae exclusivamente los siguientes campos en formato JSON. No incluyas explicaciones ni texto adicional.
                [INST] Extrae los siguientes campos en formato JSON, necesito que no me des ningún texto adicional (ni comentarios ni explicaciones, solo el JSON, además análiza muy bien el texto para que no me falte ningún campo, pues el formato de los RUTs, no es exactamente el valor frente del campo, sino que puede variar, pero por lógica puedes encontrarlo, por ejemplo, esta es la estructura donde puedes encontrar el NIT):
                Ten en cuenta que los campos pueden no estar alineados ni ordenados, pero puedes identificarlos por contexto o por patrones comunes. Algunos ejemplos útiles para inferir el NIT y otros campos ya están presentes en el texto.

                - Primer Nombre
                - Primer Apellido
                - Correo
                - Teléfono
                - NIT
                - Dirección
                - Ciudad
                - País
                - Tipo Documento
                - Numero Documento
                Solo incluye los campos que estén presentes en la anterior lista.
                Documento:
                \"\"\"{texto_plano}\"\"\" [/INST]
                """},
            ]
        )
        
        datos_ia = response.choices[0].message.content.strip()
        # resultado_final = completar_con_regex(texto_plano, json.loads(datos_ia))
        # return str(resultado_final)
        print(response.choices[0].message.content)
        
        return str(datos_ia)
        
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# 🧪 Ejecución principal
if __name__ == "__main__":
    with open(r"C:\Users\USUARIO\OneDrive - netapplications.com.co\RPA\AA\Desayuno\Outputs\Aprovados\RUT.txt", encoding="utf-8") as f:
        texto = f.read()
        
    resultado_final = obtener_info_rut(texto)