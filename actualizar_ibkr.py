import os
import time
import requests
import xml.etree.ElementTree as ET

token = os.environ.get("IBKR_TOKEN")
query_id = os.environ.get("IBKR_QUERY_ID")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

endpoints = [
    "https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest",
    "https://www.interactivebrokers.co.uk/Universal/servlet/FlexStatementService.SendRequest"
]

reference_code = None

print("Solicitando generación de reporte a IBKR...")
for url in endpoints:
    params = {"t": token, "q": query_id, "v": "3"}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        root = ET.fromstring(response.text)
        
        status = root.find(".//Status") or root.find(".//status")
        if status is not None and status.text == "Success":
            ref = root.find(".//ReferenceCode") or root.find(".//referenceCode")
            reference_code = ref.text
            print(f"Éxito con endpoint {url}")
            print(f"Código de referencia: {reference_code}")
            break
        else:
            err = root.find(".//ErrorMessage") or root.find(".//errorMessage")
            msg = err.text if err is not None else response.text
            print(f"Respuesta de {url}: {msg}")
    except Exception as e:
        print(f"Error conectando a {url}: {e}")

if not reference_code:
    raise Exception("No se pudo generar el reporte en IBKR. Revise Query ID / Token.")

print("Esperando 20 segundos a que IBKR genere el archivo...")
time.sleep(20)

get_url = "https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement"
get_params = {"q": reference_code, "t": token, "v": "3"}

csv_response = requests.get(get_url, params=get_params, headers=headers, timeout=60)

with open("IBKR_Portofolio_Dashboard 2026.csv", "w", encoding="utf-8") as f:
    f.write(csv_response.text)

print("¡Archivo CSV descargado y guardado como 'IBKR_Portofolio_Dashboard 2026.csv' con éxito!")
