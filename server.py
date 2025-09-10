from flask import Flask, jsonify
import requests

app = Flask(__name__)

# El TOKEN me lo envió REDEIA por email cuando me suscribí a la API
token = "8ec0b2a5dd9fd18161925ba3c9c9b8e8f12839dc8dc8dac847c81cdf71db3a1a"

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
        precios = [{"fecha": entry["datetime"], "precio": entry["price"]} for entry in data["PVPC"]]
        return jsonify(precios)
    else:
        return jsonify({"error": f"Error al obtener los datos: {response.status_code}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
