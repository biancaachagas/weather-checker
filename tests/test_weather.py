from unittest.mock import patch, MagicMock
from src.weather import get_city_coordinates, get_weather


@patch("src.weather.requests.get")
def test_get_city_coordinates_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [
            {
                "name": "Curitiba",
                "country": "Brasil",
                "latitude": -25.42778,
                "longitude": -49.27306,
            }
        ]
    }
    mock_get.return_value = mock_response

    result = get_city_coordinates("Curitiba")

    assert result is not None
    assert result["name"] == "Curitiba"
    assert result["country"] == "Brasil"
    assert result["latitude"] == -25.42778
    assert result["longitude"] == -49.27306


@patch("src.weather.requests.get")
def test_get_city_coordinates_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    result = get_city_coordinates("CidadeInexistente123")

    assert result is None


@patch("src.weather.requests.get")
def test_get_weather_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "current_units": {
            "temperature_2m": "°C",
            "relative_humidity_2m": "%",
            "wind_speed_10m": "km/h",
        },
        "current": {
            "temperature_2m": 18.5,
            "relative_humidity_2m": 70,
            "wind_speed_10m": 12.0,
        },
    }
    mock_get.return_value = mock_response

    weather = get_weather(-25.42778, -49.27306)

    assert "current" in weather
    assert weather["current"]["temperature_2m"] == 18.5
    assert weather["current"]["relative_humidity_2m"] == 70
    assert weather["current"]["wind_speed_10m"] == 12.0
