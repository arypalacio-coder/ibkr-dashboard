import os
import time
import requests
import xml.etree.ElementTree as ET

token = os.environ.get("IBKR_TOKEN")
query_id = os.environ.get("IBKR_QUERY_ID")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

url_send = f"https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest?t={token}&q={query_id}&v=3"

print("Solicitando generación de reporte a IBKR...")
response = requests.get(url_send, headers=headers)
root = ET.fromstring(response.text)

status = root.find(".//Status")
if status is None:
    status = root.find(".//status")

if status is None or status.text != "Success":
    error_elem = root.find(".//ErrorMessage")
    if error_elem is None:
        error_elem = root.find(".//errorMessage")
    msg = error_elem.text if error_elem is not None else response.text
    raise Exception(f"Fallo al solicitar reporte: {msg}")

ref_elem = root.find(".//ReferenceCode")
if ref_elem is None:
    ref_elem = root.find(".//referenceCode")
reference_code = ref_elem.text

print(f"Reporte solicitado con éxito. Reference code: {reference_code}")
print("Esperando 15 segundos a que IBKR compile el CSV...")
time.sleep(15)

url_get = f"https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement?q={reference_code}&t={token}&v=3"

csv_response = requests.get(url_get, headers=headers)
with open("IBKR_Portofolio_Dashboard 2026.csv", "w", encoding="utf-8") as f:
    f.write(csv_response.text)

print("¡Archivo CSV descargado y actualizado con éxito!")
