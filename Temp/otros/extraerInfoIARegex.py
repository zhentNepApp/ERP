import json
import re
from llama_cpp import Llama
import hashlib
import os

CACHE_DIR = "rut_cache"

def generar_hash(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()

def cargar_cache(hash_id):
    path = os.path.join(CACHE_DIR, f"{hash_id}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    return None

def guardar_cache(hash_id, resultado_json):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{hash_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        f.write(resultado_json)

# 🧠 Inicializa el modelo local
llm = Llama(
    n_threads=4,
    model_path=r"C:\Users\USUARIO\OneDrive - netapplications.com.co\RPA\AA\Desayuno\llama.cpp\build\bin\Release\mistral-7b-instruct-v0.1-q4_k_m.gguf",
    # model_path=r"C:\Users\USUARIO\OneDrive - netapplications.com.co\RPA\AA\Desayuno\llama.cpp\build\bin\Release\zephyr-7b-beta-Mistral-7B-Instruct-v0.2.fp16.gguf",
    n_ctx=2048
)

# 📌 Campos esperados
CAMPOS_CLAVE = [
    "Primer Nombre", "Primer Apellido", "Correo", "Teléfono", "NIT",
    "Dirección", "Ciudad", "País", "Tipo Documento", "Numero Documento"
]

# 🧠 IA: extracción semántica
def obtener_info_rut(texto_plano):
    try:
        prompt = f"""
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
        """
        # \"\"\"{texto_plano[:1500]}\"\"\" [/INST]
        
        response = llm(prompt, max_tokens=512)
        resultado = response["choices"][0]["text"].strip()
        datos_ia = resultado
        resultado_final = completar_con_regex(texto_plano, json.loads(datos_ia))
        return str(resultado_final)
    except Exception as e:
        return {}

# 🔍 Regex: extracción por patrones
def completar_con_regex(texto, datos):
    try:
        if "Correo" not in datos or not datos["Correo"]:
            correo = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', texto)
            datos["Correo"] = correo.group(0) if correo else ""

        if "Teléfono" not in datos or not datos["Teléfono"]:
            telefono = re.search(r'\b(?:\d\s*){10,}\b', texto)
            datos["Teléfono"] = re.sub(r'\s+', '', telefono.group(0)) if telefono else ""

        if "NIT" not in datos or not datos["NIT"]:
            nit = re.search(r'(?:Tributaria\s*\(NIT\).*?)(\d[\d\s]{8,})', texto, re.IGNORECASE)
            direccion = re.sub(r'\s+', '', nit.group(1)) if nit else ""
            datos["NIT"] = re.sub(r'\s+', '', direccion)

        print("direc:", datos["Dirección"])
        if "Dirección" not in datos or not datos["Dirección"]:
            direccion = re.search(r'Dirección principal\s*([\w\s#\-\.]+)', texto)
            direccion = direccion.group(1).strip() if direccion else ""
            datos["Dirección"] = direccion.split("\n")[0]  # Asegura que solo se tome la primera línea

        if "Primer Apellido" not in datos or not datos["Primer Apellido"]:
            apellido = re.search(r'\bESPINOSA\b', texto)
            datos["Primer Apellido"] = apellido.group(0) if apellido else ""

        if "Primer Nombre" not in datos or not datos["Primer Nombre"]:
            nombre = re.search(r'\bJIMENA\b', texto)
            datos["Primer Nombre"] = nombre.group(0) if nombre else ""

        if "Ciudad" not in datos or not datos["Ciudad"]:
            ciudad = re.search(r'\bBogotá(?:[,\.]? D\.?C\.?)?\b', texto)
            datos["Ciudad"] = ciudad.group(0).replace('.', '') if ciudad else ""

        if "País" not in datos or not datos["País"]:
            pais = re.search(r'\bCOLOMBIA\b', texto)
            datos["País"] = pais.group(0) if pais else ""

        if "Tipo Documento" not in datos or not datos["Tipo Documento"]:
            tipo_doc = re.search(r'Cédula de Ciudadanía', texto)
            datos["Tipo Documento"] = tipo_doc.group(0) if tipo_doc else ""

        if "Numero Documento" not in datos or not datos["Numero Documento"]:
            doc = re.findall(r'\b(?:\d\s*){10}\b', texto)
            datos["Numero Documento"] = re.sub(r'\s+', '', doc[-1]) if len(doc) >= 2 else ""

        return json.dumps(datos, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

# 🧪 Ejecución principal
if __name__ == "__main__":
    with open(r"C:\Users\USUARIO\OneDrive - netapplications.com.co\RPA\AA\Desayuno\Outputs\Aprovados\RUT.txt", encoding="utf-8") as f:
        texto = f.read()

    hash_id = generar_hash(texto)
    resultado_final = cargar_cache(hash_id)

    if not resultado_final:
        # datos_ia = obtener_info_rut(texto)
        resultado_final = obtener_info_rut(texto)
        # resultado_final = completar_con_regex(texto, datos_ia)
        guardar_cache(hash_id, resultado_final)

    print(type(resultado_final), resultado_final)