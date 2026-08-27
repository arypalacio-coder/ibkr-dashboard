import os
import time
import requests
import xml.etree.ElementTree as ET

token = os.environ.get("IBKR_TOKEN")
query_id = os.environ.get("IBKR_QUERY_ID")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# 1. Petición inicial para solicitar el reporte
url_send = f"https://www.interactivebrokers.co.uk/Universal/servlet/FlexStatementService.SendRequest?t={token}&q={query_id}&v=3"

print("Solicitando generación de reporte a IBKR...")
response = requests.get(url_send, headers=headers)

# Fallback al dominio global si el regional no responde
if response.status_code != 200 or "<Status>Fail</Status>" in response.text:
    url_send = f"https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest?t={token}&q={query_id}&v=3"
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

print(f"Reporte en cola. Reference code: {reference_code}")

# 2. Polling con espera progresiva para descargar el archivo procesado
url_get = f"https://www.interactivebrokers.co.uk/Universal/servlet/FlexStatementService.GetStatement?q={reference_code}&t={token}&v=3"

statement_ready = False
for i in range(10):
    time.sleep(10)
    print(f"Verificando disponibilidad del archivo (intento {i+1}/10)...")
    res = requests.get(url_get, headers=headers)
    
    if "<ErrorCode>1001</ErrorCode>" not in res.text and "<Status>Warn</Status>" not in res.text:
        with open("IBKR_Portofolio_Dashboard.csv", "w", encoding="utf-8") as f:
            f.write(res.text)
        statement_ready = True
        print("¡Archivo CSV descargado y actualizado con éxito!")
        break

if not statement_ready:
    raise Exception("El reporte tardó demasiado en procesarse en el servidor de IBKR.")
