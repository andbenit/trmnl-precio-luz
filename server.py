from flask import Flask, jsonify
import requests

app = Flask(__name__)
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
        precios = []
        precios_numericos = []  # Lista para calcular la hora más barata/cara

        if "PVPC" in data:
            for entry in data["PVPC"]:
                fecha = f"{entry['Dia']} {entry['Hora']}"
                precio_mwh_str = entry.get("PCB", "0,00")
                precio_mwh_str = precio_mwh_str.replace(',', '.')
                precio_mwh = float(precio_mwh_str)
                precio_kwh = precio_mwh / 1000
                precio_kwh_redondeado = round(precio_kwh, 3)  # Redondeamos a 3 decimales
                precio_kwh_str = f"{precio_kwh_redondeado:.3f}".replace('.', ',')
                precios_numericos.append(precio_kwh_redondeado)  # Guardamos el precio numérico

                # Determinamos si es barato o caro
                es_barato = precio_kwh_redondeado < 0.10
                es_caro = precio_kwh_redondeado > 0.20

                # Asignamos un emoji según el precio
                if es_barato:
                    emoji = "😊"
                elif es_caro:
                    emoji = "😞"
                else:
                    emoji = "😐"

                precios.append({
                    "fecha": fecha,
                    "precio": f"{precio_kwh_str} €/kWh",
                    "es_barato": es_barato,
                    "es_caro": es_caro,
                    "emoji": emoji,
                    "precio_num": precio_kwh_redondeado  # Guardamos el precio numérico para cálculos
                })

            # Identificamos la hora más barata y más cara del día
            if precios_numericos:
                precio_min = min(precios_numericos)
                precio_max = max(precios_numericos)

                # Asignamos emojis especiales a las horas más barata y cara
                for precio in precios:
                    if precio["precio_num"] == precio_min:
                        precio["emoji"] = "🥇"  # Hora más barata
                    elif precio["precio_num"] == precio_max:
                        precio["emoji"] = "💥"  # Hora más cara

        return jsonify(precios)
    else:
        return jsonify({"error": f"Error al obtener los datos: {response.status_code}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
