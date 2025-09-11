from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)
token = os.environ.get('REE_TOKEN')

@app.route('/precio-luz', methods=['GET'])
def get_precio_luz():
    url = "https://api.esios.ree.es/archives/70/download_json"
    headers = {
        "Accept": "application/json; application/vnd.esios-api-v1+json",
        "Content-Type": "application/json",
        "Authorization": f"Token token=\"{token}\"",
        "Host": "api.esios.ree.es"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        precios = []
        if "PVPC" in data:
            for entry in data["PVPC"]:
                fecha = f"{entry['Dia']} {entry['Hora']}"  # Usamos 'Dia' sin tilde
                # Convertimos el precio de formato con coma a float
                precio_mwh_str = entry.get("PCB", "0,00")  # Obtenemos el precio como cadena
                precio_mwh_str = precio_mwh_str.replace(',', '.')  # Reemplazamos la coma por punto
                precio_mwh = float(precio_mwh_str)  # Convertimos a float
                precio_kwh = precio_mwh / 1000  # Convertimos a €/kWh
                # Convertimos el precio de vuelta a formato con coma para mostrarlo
                precio_kwh_str = f"{precio_kwh:.3f}".replace('.', ',')  # Formateamos a 3 decimales y reemplazamos el punto por coma
                precios.append({"fecha": fecha, "precio": f"{precio_kwh_str} €/kWh"})
        return jsonify(precios)
    else:
        return jsonify({"error": f"Error al obtener los datos: {response.status_code}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

