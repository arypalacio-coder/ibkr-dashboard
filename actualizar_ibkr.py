import os
import sys
import time
import requests
import xml.etree.ElementTree as ET

TOKEN = os.getenv("IBKR_TOKEN")
QUERY_ID = os.getenv("IBKR_QUERY_ID")

if not TOKEN or not QUERY_ID:
    print("Error: Credenciales no configuradas.")
    sys.exit(1)

# Endpoint oficial de Flex Web Service
BASE_URL = "https://ndcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService"

# 1. Solicitar generación del reporte
url_request = f"{BASE_URL}.SendRequest?t={TOKEN}&q={QUERY_ID}&v=3"
print("Solicitando generación de reporte a IBKR...")
res = requests.get(url_request)

if res.status_code != 200:
    print(f"Error HTTP en SendRequest: {res.status_code}")
    sys.exit(1)

root = ET.fromstring(res.content)
status = root.find(".//Status")

if status is None or status.text != "Success":
    err_code = root.find(".//ErrorCode")
    err_msg = root.find(".//ErrorMessage")
    print(f"Error de IBKR: {err_code.text if err_code is not None else ''} - {err_msg.text if err_msg is not None else ''}")
    sys.exit(1)

ref_code = root.find(".//ReferenceCode").text
print(f"Reporte en proceso. Código de referencia: {ref_code}")

# 2. Descargar el archivo generado
url_statement = f"{BASE_URL}.GetStatement?q={ref_code}&t={TOKEN}&v=3"

intentos = 0
max_intentos = 10
descargado = False

while intentos < max_intentos and not descargado:
    time.sleep(3)
    intentos += 1
    print(f"Intento {intentos} de descarga...")
    rep_res = requests.get(url_statement)
    
    if rep_res.status_code == 200:
        if b"<FlexStatementResponse" in rep_res.content and b"<Status>Warn" in rep_res.content:
            print("El reporte aún se está procesando en IBKR, reintentando...")
            continue
        
        with open("IBKR_Portofolio_Dashboard.csv", "wb") as f:
            f.write(rep_res.content)
        print("Archivo IBKR_Portofolio_Dashboard.csv descargado y guardado exitosamente.")
        descargado = True
    else:
        print(f"Error HTTP en GetStatement: {rep_res.status_code}")

if not descargado:
    print("No se pudo obtener el reporte después de los intentos programados.")
    sys.exit(1)
