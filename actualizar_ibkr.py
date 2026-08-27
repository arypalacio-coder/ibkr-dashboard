import os
import time
import requests
import xml.etree.ElementTree as ET

token = os.environ.get("IBKR_TOKEN")
query_id = os.environ.get("IBKR_QUERY_ID")

url_send = f"https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest?t={token}&q={query_id}&v=3"

print("Solicitando generación de reporte a IBKR...")

reference_code = None
for intento in range(3):
    response = requests.get(url_send)
    root = ET.fromstring(response.text)
    
    status = root.find(".//status")
    if status is not None and status.text == "Success":
        reference_code = root.find(".//referenceCode").text
        print(Reference code obtenido: {reference_code})
        break
    else:
        error_msg = root.find(".//errorMessage")
        msg = error_msg.text if error_msg is not None else response.text
        print(f"Intento {intento+1} fallido: {msg}. Reintentando en 10 segundos...")
        time.sleep(10)

if not reference_code:
    raise Exception("No se pudo generar el reporte en IBKR tras varios intentos. Intente más tarde.")

time.sleep(5)

url_get = f"https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement?q={reference_code}&t={token}&v=3"

csv_response = requests.get(url_get)
with open("IBKR_Portofolio_Dashboard.csv", "w", encoding="utf-8") as f:
    f.write(csv_response.text)

print("¡Archivo CSV descargado y actualizado con éxito!")

if not descargado:
    print("No se pudo obtener el reporte después de los intentos programados.")
    sys.exit(1)
