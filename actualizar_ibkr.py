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
for i in range(1, 6):
    response = requests.get(url_send, headers=headers)
    root = ET.fromstring(response.text)
    status = root.find(".//Status") or root.find(".//status")
    
    if status is not None and status.text == "Success":
        ref = root.find(".//ReferenceCode") or root.find(".//referenceCode")
        reference_code = ref.text
        print(f"Referencia obtenida con éxito: {reference_code}")
        break
    else:
        err = root.find(".//ErrorMessage") or root.find(".//errorMessage")
        msg = err.text if err is not None else response.text
        print(f"Intento {i}/5: IBKR compilando ({msg}). Esperando 20s...")
        time.sleep(20)

if not reference_code:
    raise Exception("IBKR no pudo entregar el reporte tras 5 intentos.")

time.sleep(15)

url_get = f"https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement?q={reference_code}&t={token}&v=3"

csv_response = requests.get(url_get, headers=headers)
with open("IBKR_Portofolio_Dashboard 2026.csv", "w", encoding="utf-8") as f:
    f.write(csv_response.text)

print("¡Archivo 'IBKR_Portofolio_Dashboard 2026.csv' guardado y actualizado con éxito!")
