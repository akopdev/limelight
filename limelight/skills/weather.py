from enum import Enum
from typing import Dict, Optional

import aiohttp
from pydantic import BaseModel

from ..logger import log
from .base import BaseSkill


class Unit(str, Enum):
    celsius = "celsius"
    fahrenheit = "fahrenheit"


class WeatherForecast(BaseModel):
    """Weather forecast data."""

    temperature: float
    wind: float


class WeatherForecastResponse(BaseModel):
    """Response from the Open-Meteo API."""

    temperature_2m: float
    wind_speed_10m: float


class WeatherGeocoding(BaseModel):
    """Response from the Open-Meteo API."""

    latitude: float
    longitude: float


class Weather(BaseSkill):
    locations: Dict[str, WeatherGeocoding] = {}

    __name__ = "weather"
    __keywords__ = [
        "snow",
        "snowfall",
        "rain",
        "raining",
        "rainfall",
        "showers",
        "wind",
        "windy",
        "temperature",
        "heatwave",
        "cold",
        "weather",
        "forecast",
        "climate",
        "humidity",
        "uv index",
        "storm",
        "hurricane",
        "tornado",
        "barometric pressure",
        "outdoor",
        "sunrise",
        "sunset",
        "air quality",
        "heat",
        "meteorological",
        "rainy",
        "accumulation",
        "precipitation",
        "thunderstorm",
        "fog",
        "cloudy",
        "overcast",
        "sunny",
    ]

    async def get_location(self, city: str) -> WeatherGeocoding:
        """Get the latitude and longitude of a city."""
        if not self.locations.get(city):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={"name": city, "count": 1},
                ) as response:
                    data = await response.json()
                    if not data.get("results"):
                        return
                    self.locations[city] = WeatherGeocoding(**data.get("results", [{}])[0])
        return self.locations[city]

    async def run(
        self, city: Optional[str] = "Amsterdam", unit: Optional[Unit] = Unit.celsius
    ) -> Optional[WeatherForecast]:
        """Get the current weather forecast for the user's location."""
        if location := await self.get_location(city):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": location.latitude,
                        "longitude": location.longitude,
                        "current": "temperature_2m,wind_speed_10m",
                        "temperature_unit": unit.value,
                    },
                ) as response:
                    try:
                        if response.status == 200:
                            result = await response.json()
                            resp = WeatherForecastResponse(**result.get("current", {}))
                            return WeatherForecast(
                                temperature=resp.temperature_2m, wind=resp.wind_speed_10m
                            )
                    except Exception as e:
                        log.error(e)
