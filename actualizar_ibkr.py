import os
import time
import requests
import xml.etree.ElementTree as ET

token = os.environ.get("IBKR_TOKEN")
query_id = os.environ.get("IBKR_QUERY_ID")

url_send = f"https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest?t={token}&q={query_id}&v=3"

print("Solicitando generación de reporte a IBKR...")

reference_code = None
max_intentos = 6
espera = 15

for intento in range(max_intentos):
    response = requests.get(url_send)
    try:
        root = ET.fromstring(response.text)
    except Exception as e:
        print(f"Error parseando respuesta XML: {response.text}")
        time.sleep(espera)
        continue

    status = root.find(".//Status")
    if status is None:
        status = root.find(".//status")
        
    if status is not None and status.text == "Success":
        ref_elem = root.find(".//ReferenceCode")
        if ref_elem is None:
            ref_elem = root.find(".//referenceCode")
        reference_code = ref_elem.text
        print(f"Código de referencia obtenido con éxito: {reference_code}")
        break
    else:
        error_elem = root.find(".//ErrorMessage")
        if error_elem is None:
            error_elem = root.find(".//errorMessage")
        msg = error_elem.text if error_elem is not None else response.text
        print(f"Intento {intento+1}/{max_intentos}: IBKR procesando ({msg}). Esperando {espera}s...")
        time.sleep(espera)

if not reference_code:
    raise Exception("IBKR tardó demasiado en compilar el reporte. Intente en unos minutos.")

# Espera para permitir la consolidación del archivo en el servidor de IBKR
time.sleep(10)

url_get = f"https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement?q={reference_code}&t={token}&v=3"

print("Descargando archivo CSV generado...")
csv_response = requests.get(url_get)

# Reintento de descarga si el archivo aún se está escribiendo
for _ in range(3):
    if "<Status>Warn</Status>" in csv_response.text or "Statement is being generated" in csv_response.text:
        print("El archivo se sigue preparando en el servidor. Esperando 10s...")
        time.sleep(10)
        csv_response = requests.get(url_get)
    else:
        break

with open("IBKR_Portofolio_Dashboard.csv", "w", encoding="utf-8") as f:
    f.write(csv_response.text)

print("¡Archivo CSV descargado y actualizado con éxito!")
