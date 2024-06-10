import re

import pytest
from aioresponses import aioresponses

from limelight.skills import Weather


@pytest.mark.asyncio()
async def test_weather_geocoding():
    weather = Weather(city="Amsterdam")
    with aioresponses() as m:
        m.get(
            "https://geocoding-api.open-meteo.com/v1/search?name=Amsterdam&count=1",
            payload={"results": [{"latitude": 52.379189, "longitude": 4.899431}]},
        )
        result = await weather.get_location()
        assert result
        assert result.latitude == 52.379189
        assert result.longitude == 4.899431
    # Test caching by triggering the api without mocking
    assert await weather.get_location() == result


@pytest.mark.asyncio()
async def test_weather_forecast():
    with aioresponses() as m:
        m.get(
            re.compile(r"^https://geocoding-api\.open-meteo\.com/v1/search\?.*"),
            payload={"results": [{"latitude": 52.379189, "longitude": 4.899431}]},
        )
        m.get(
            re.compile(r"^https://api\.open-meteo\.com/v1/forecast\?.*"),
            payload={"current": {"temperature_2m": 10.0, "wind_speed_10m": 6.0}},
        )
        weather = Weather(city="Amsterdam")
        result = await weather.forecast()
        assert result
        assert result.temperature == 10.0
        assert result.wind == 6.0
