import json
from modelo import extract_text_from_pdf
from llama_cpp import Llama

# 🧠 inicializa tu modelo local
llm = Llama(
    model_path=r"C:\Users\USUARIO\Downloads\llama.cpp\build\bin\Release\zephyr-7b-beta-Mistral-7B-Instruct-v0.2.Q2_K.gguf",  # <-- cambia esto
    n_threads=4,
    n_ctx=2048  # Asegúrate que el modelo soporte esto (ej. mistral Q4)
)

def parse_fields_with_llm(text):
    try:
        # 🧠 prompt con pocas instrucciones para no exceder el contexto
        prompt = f"""[INST] Extrae los siguientes campos en formato JSON:
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

        Documento:
        \"\"\"{text[:1500]}\"\"\" [/INST]
        """

        response = llm(prompt, max_tokens=512)
        return response["choices"][0]["text"].strip()

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)

# 🗂️ extrae texto del PDF
pdf_path = r"C:\Users\USUARIO\OneDrive - netapplications.com.co\RPA\AA\Desayuno\Outputs\Aprovados\RUT.pdf"
texto_documento = extract_text_from_pdf(pdf_path)
print(texto_documento)

# 🧪 ejecuta modelo
resultado_json = parse_fields_with_llm(texto_documento)
print(resultado_json)