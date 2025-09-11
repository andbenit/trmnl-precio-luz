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
        # Imprimimos la estructura de los datos para depurar:
        print("Estructura de los datos:", data.keys())  # Ver qué claves tiene el JSON principal
        if "PVPC" in data:
            print("Primer elemento de PVPC:", data["PVPC"][0].keys())  # Ver las claves del primer precio
        # Devolvemos los datos crudos para verlos en el navegador:
        return jsonify(data)
    else:
        return jsonify({"error": f"Error al obtener los datos: {response.status_code}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
