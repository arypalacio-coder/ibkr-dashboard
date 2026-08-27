import os
import time
import requests
import xml.etree.ElementTree as ET

token = os.environ.get("IBKR_TOKEN")
query_id = os.environ.get("IBKR_QUERY_ID")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

url_send = f"https://ndcdyn.interactivebrokers.com/AccountManagement/FlexWebService/SendRequest?t={token}&q={query_id}&v=3"

print("Solicitando generación de reporte a IBKR...")
response = requests.get(url_send, headers=headers)
print("Respuesta IBKR:", response.text)

root = ET.fromstring(response.text)

# Búsqueda insensible a mayúsculas/minúsculas de Status
status = None
for elem in root.iter():
    if elem.tag.lower().endswith("status"):
        status = elem.text
        break

if status != "Success":
    err_msg = response.text
    for elem in root.iter():
        if elem.tag.lower().endswith("errormessage"):
            err_msg = elem.text
            break
    raise Exception(f"Fallo al solicitar reporte: {err_msg}")

# Búsqueda insensible de ReferenceCode
reference_code = None
for elem in root.iter():
    if elem.tag.lower().endswith("referencecode"):
        reference_code = elem.text
        break

if not reference_code:
    raise Exception(f"No se encontró código de referencia en el XML: {response.text}")

print(f"Reporte solicitado con éxito. Reference code: {reference_code}")
print("Esperando 15 segundos a que IBKR compile el CSV...")
time.sleep(15)

url_get = f"https://ndcdyn.interactivebrokers.com/AccountManagement/FlexWebService/GetStatement?q={reference_code}&t={token}&v=3"
csv_response = requests.get(url_get, headers=headers)

with open("IBKR_Portofolio_Dashboard 2026.csv", "w", encoding="utf-8") as f:
    f.write(csv_response.text)

print("¡Archivo 'IBKR_Portofolio_Dashboard 2026.csv' guardado y actualizado con éxito en GitHub!")
