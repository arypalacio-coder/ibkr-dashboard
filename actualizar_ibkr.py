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

reference_code = None
for intento in range(1, 6):
    response = requests.get(url_send, headers=headers)
    try:
        root = ET.fromstring(response.text)
        status = root.find(".//Status") or root.find(".//status")
        
        if status is not None and status.text == "Success":
            ref = root.find(".//ReferenceCode") or root.find(".//referenceCode")
            reference_code = ref.text
            print(f"Código de referencia obtenido: {reference_code}")
            break
        else:
            err = root.find(".//ErrorMessage") or root.find(".//errorMessage")
            msg = err.text if err is not None else response.text
            print(f"Intento {intento}/5: IBKR respondió '{msg}'. Reintentando en 15s...")
    except Exception as e:
        print(f"Intento {intento}/5: Error de conexión ({e}). Reintentando en 15s...")
    
    time.sleep(15)

if not reference_code:
    raise Exception("No se pudo obtener el código de referencia tras varios intentos.")

print("Esperando 15 segundos para la consolidación del archivo...")
time.sleep(15)

url_get = f"https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement?q={reference_code}&t={token}&v=3"

statement_downloaded = False
for intento in range(1, 6):
    csv_response = requests.get(url_get, headers=headers)
    if "<ErrorCode>" in csv_response.text or "<Status>Warn</Status>" in csv_response.text:
        print(f"Intento {intento}/5: El archivo aún se está generando. Esperando 10s...")
        time.sleep(10)
    else:
        with open("IBKR_Portofolio_Dashboard 2026.csv", "w", encoding="utf-8") as f:
            f.write(csv_response.text)
        statement_downloaded = True
        print("¡Archivo CSV descargado y guardado como 'IBKR_Portofolio_Dashboard 2026.csv' con éxito!")
        break

if not statement_downloaded:
    raise Exception("El servidor de IBKR no entregó el archivo a tiempo.")
