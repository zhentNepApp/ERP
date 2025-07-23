import pdfplumber

def extract_text_from_pdf(path):
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

import json
from llama_cpp import Llama

# 🧠 Inicializa el modelo local una sola vez
llm = Llama(
    # model_path=r"C:\Users\USUARIO\Downloads\llama.cpp\build\bin\Release\zephyr-7b-beta-Mistral-7B-Instruct-v0.2.Q2_K.gguf",
    # model_path=r"C:\Users\USUARIO\Downloads\llama.cpp\build\bin\Release\gemma-2-2b-it-Q4_0_4_4-00003-of-00003.gguf",
    model_path=r"C:\Users\USUARIO\Downloads\llama.cpp\build\bin\Release\mistral-7b-instruct-v0.1-q4_k_m.gguf",
    n_threads=4,
    n_ctx=2048
)

def obtener_info_rut(texto_plano):
    try:
        # 🧠 Prompt con bajo contexto para extracción estructurada
        prompt = f"""
        Eres un experto en análisis de documentos RUT de la DIAN. Extrae exclusivamente los siguientes campos en formato JSON. No incluyas explicaciones ni texto adicional.
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
        - Tipo de Documento
        - Número de Documento 
        Unicamente, los campos que se encuentran en el texto, no inventes ni agregues campos que no existan.
        Documento:
        \"\"\"{texto_plano[:1500]}\"\"\" [/INST]
        """

        response = llm(prompt, max_tokens=512)
        resultado = response["choices"][0]["text"].strip()

        # Asegura que el retorno sea un string legible
        return resultado

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)
    
if __name__ == "__main__":
    with open(r"C:\Users\USUARIO\OneDrive - netapplications.com.co\RPA\AA\Desayuno\Outputs\Aprovados\RUT.txt", encoding="utf-8") as f:
        texto = f.read()

    resultado = obtener_info_rut(texto)
    print(resultado)