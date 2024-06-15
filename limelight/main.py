from fastapi import Depends, FastAPI, HTTPException

from .models import Document, Query
from .skills import Weather
from .utils import combine_response

app = FastAPI()


@app.get("/search")
async def search(q: str):
    query = Query.parse_text(q)
    # id = query.save()

    weather_related_keywords = [
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

    # Check if we need to call query
    if any(keyword in query.keywords for keyword in weather_related_keywords):
        # Call the weather skill with the query
        result = await Weather().forecast()
        return result

    # Search result candidates in the database
    documents = Document.search(query.text, query.keywords)

    return combine_response(documents[:3], query)
    # Generate a human-readable response

    return documents


@app.get("/weather")
async def weather(weather: Weather = Depends(Weather)):
    result = await weather.forecast()
    if not result:
        raise HTTPException(status_code=404, detail="Error fetching weather data")
    return result
