from unittest.mock import patch, MagicMock
import pytest
import requests
from src.weather import get_city_coordinates, get_weather, main


@patch("src.weather.requests.get")
def test_get_city_coordinates_success(mock_get):
    """Teste 1: Busca de coordenadas de cidade com sucesso"""
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
    """Teste 2: Busca de cidade inexistente (retorna None)"""
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    result = get_city_coordinates("CidadeInexistente123")

    assert result is None


@patch("src.weather.requests.get")
def test_get_city_coordinates_http_error(mock_get):
    """Teste 3: Trata erro HTTP na busca de coordenadas"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
    mock_get.return_value = mock_response

    with pytest.raises(requests.exceptions.HTTPError):
        get_city_coordinates("Curitiba")


@patch("src.weather.requests.get")
def test_get_weather_success(mock_get):
    """Teste 4: Busca de dados de clima com sucesso"""
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


@patch("src.weather.requests.get")
def test_get_weather_http_error(mock_get):
    """Teste 5: Trata erro HTTP na consulta de clima"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mock_get.return_value = mock_response

    with pytest.raises(requests.exceptions.HTTPError):
        get_weather(0.0, 0.0)


@patch("builtins.input", return_value="Curitiba")
@patch("src.weather.get_weather")
@patch("src.weather.get_city_coordinates")
def test_main_interactive_flow(mock_coords, mock_weather, mock_input):
    """Teste 6: Fluxo completo da função main() interativa"""
    mock_coords.return_value = {
        "name": "Curitiba",
        "country": "Brasil",
        "latitude": -25.42778,
        "longitude": -49.27306,
    }
    mock_weather.return_value = {
        "current_units": {
            "temperature_2m": "°C",
            "relative_humidity_2m": "%",
            "wind_speed_10m": "km/h",
        },
        "current": {
            "temperature_2m": 20.0,
            "relative_humidity_2m": 65,
            "wind_speed_10m": 10.0,
        },
    }

    # Executa a função main sem erros
    main()

    mock_input.assert_called_once()
    mock_coords.assert_called_once_with("Curitiba")
    mock_weather.assert_called_once_with(-25.42778, -49.27306)
