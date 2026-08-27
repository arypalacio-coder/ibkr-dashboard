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

# 1. Solicitar generación del reporte Flex
url_request = f"https://gdcdp.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest?t={TOKEN}&q={QUERY_ID}&v=3"
print("Solicitando generación de reporte a IBKR...")
res = requests.get(url_request)

if res.status_code != 200:
    print(f"Error en la solicitud HTTP: {res.status_code}")
    sys.exit(1)

root = ET.fromstring(res.content)
status = root.find(".//Status")
if status is not None and status.text != "Success":
    err_code = root.find(".//ErrorCode")
    err_msg = root.find(".//ErrorMessage")
    print(f"Error IBKR: {err_code.text if err_code is not None else ''} - {err_msg.text if err_msg is not None else ''}")
    sys.exit(1)

ref_code = root.find(".//ReferenceCode").text
print(f"Reporte en proceso. Código de referencia: {ref_code}")

# 2. Reintentar descarga hasta que el reporte esté disponible
url_statement = f"https://gdcdp.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement?q={ref_code}&t={TOKEN}&v=3"

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
            print("El reporte aún no está listo, esperando...")
            continue
        
        # Guardar archivo CSV con el nombre exacto
        with open("IBKR_Portofolio_Dashboard.csv", "wb") as f:
            f.write(rep_res.content)
        print("Archivo IBKR_Portofolio_Dashboard.csv descargado y guardado exitosamente.")
        descargado = True
    else:
        print(f"Fallo en descarga: HTTP {rep_res.status_code}")

if not descargado:
    print("No se pudo obtener el reporte tras los intentos programados.")
    sys.exit(1)
