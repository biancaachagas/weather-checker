import requests

def get_city_coordinates(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,
        "language": "pt",
        "format": "json"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if "results" not in data or not data["results"]:
        return None

    return data["results"][0]


def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def main():
    city_input = input("Digite o nome da cidade: ").strip()
    if not city_input:
        print("Nome da cidade inválido.")
        return

    try:
        city = get_city_coordinates(city_input)

        if not city:
            print(f"❌ Cidade '{city_input}' não encontrada.")
            return

        print(f"\n--- 📍 {city.get('name')} ({city.get('country', 'N/A')}) ---")
        print(f"Latitude: {city['latitude']} | Longitude: {city['longitude']}")

        weather_data = get_weather(city["latitude"], city["longitude"])
        current = weather_data["current"]
        units = weather_data.get("current_units", {})

        print("\n--- 🌤️ Clima Atual ---")
        print(f"Temperatura: {current['temperature_2m']} {units.get('temperature_2m', '°C')}")
        print(f"Umidade:     {current['relative_humidity_2m']} {units.get('relative_humidity_2m', '%')}")
        print(f"Vento:       {current['wind_speed_10m']} {units.get('wind_speed_10m', 'km/h')}")

    except requests.RequestException as e:
        print(f"❌ Erro de conexão com a API: {e}")


if __name__ == "__main__":
    main()