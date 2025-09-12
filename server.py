from flask import Flask, jsonify
import requests
import statistics

app = Flask(__name__)
token = "8ec0b2a5dd9fd18161925ba3c9c9b8e8f12839dc8dc8dac847c81cdf71db3a1a"

# Meses en formato corto
meses_cortos = {
    "01": "ene", "02": "feb", "03": "mar", "04": "abr", "05": "may", "06": "jun",
    "07": "jul", "08": "ago", "09": "sep", "10": "oct", "11": "nov", "12": "dic"
}

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
        precios_numericos = []

        if "PVPC" in data:
            for entry in data["PVPC"]:
                # Formatear la fecha como "12 sep"
                dia = entry['Dia'].split('/')[0]  # Día del mes
                mes = entry['Dia'].split('/')[1]  # Mes
                mes_corto = meses_cortos[mes]  # Convertir mes a formato corto
                fecha = f"{dia} {mes_corto} {entry['Hora']}"

                precio_mwh_str = entry.get("PCB", "0,00")
                precio_mwh_str = precio_mwh_str.replace(',', '.')
                precio_mwh = float(precio_mwh_str)
                precio_kwh = precio_mwh / 1000
                precio_kwh_redondeado = round(precio_kwh, 3)
                precio_kwh_str = f"{precio_kwh_redondeado:.3f}".replace('.', ',')
                precios_numericos.append(precio_kwh_redondeado)

                precios.append({
                    "fecha": fecha,
                    "precio": f"{precio_kwh_str} €/kWh",
                    "precio_num": precio_kwh_redondeado,
                    "hora": entry['Hora']
                })

            if precios_numericos:
                # Calcular la media y desviación estándar
                media = statistics.mean(precios_numericos)
                desviacion = statistics.stdev(precios_numericos) if len(precios_numericos) > 1 else 0

                # Determinar umbrales para horas baratas y caras
                umbral_barato = media - 0.5 * desviacion
                umbral_caro = media + 0.5 * desviacion

                # Identificar la hora más barata y más cara
                precio_min = min(precios_numericos)
                precio_max = max(precios_numericos)

                # Añadir propiedades de estilo a cada hora
                for precio in precios:
                    if precio["precio_num"] == precio_min:
                        precio["es_hora_mas_barata"] = True
                        precio["emoji"] = "😊"
                    elif precio["precio_num"] == precio_max:
                        precio["es_hora_mas_cara"] = True
                        precio["emoji"] = "💥"
                    elif precio["precio_num"] < umbral_barato:
                        precio["es_barato"] = True
                    elif precio["precio_num"] > umbral_caro:
                        precio["es_caro"] = True
                    else:
                        precio["emoji"] = None

        return jsonify(precios)
    else:
        return jsonify({"error": f"Error al obtener los datos: {response.status_code}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

