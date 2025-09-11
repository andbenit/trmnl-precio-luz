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
                fecha = f"{entry['Dia']} {entry['Hora']}"  # Usamos los nombres exactos de los campos
                precio = entry.get("PCB", 0.0)  # Precio de la luz
                precios.append({"fecha": fecha, "precio": f"{precio} €/MWh"})
        return jsonify(precios)
    else:
        return jsonify({"error": f"Error al obtener los datos: {response.status_code}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
