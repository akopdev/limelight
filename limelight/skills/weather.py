from enum import Enum
from typing import Dict, Optional

import aiohttp
from pydantic import BaseModel

from ..logger import log


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


class Weather:
    locations: Dict[str, WeatherGeocoding] = {}

    def __init__(self, city: Optional[str] = "Amsterdam"):
        self.city: str = city

    async def get_location(self) -> WeatherGeocoding:
        """Get the latitude and longitude of a city."""
        if not self.locations.get(self.city):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={"name": self.city, "count": 1},
                ) as response:
                    data = await response.json()
                    if not data.get("results"):
                        return
                    self.locations[self.city] = WeatherGeocoding(**data.get("results", [{}])[0])
        return self.locations[self.city]

    async def forecast(self, unit: Optional[Unit] = Unit.celsius) -> Optional[WeatherForecast]:
        """Get the current weather forecast for the user's location."""
        if location := await self.get_location():
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
