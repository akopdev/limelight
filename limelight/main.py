from fastapi import Depends, FastAPI, HTTPException

from .skills import Weather
from .models import Query
from .query import process_query

app = FastAPI()


@app.get("/query")
async def search(q: str):

    query = await process_query(q)

    # q = Query(keywords=",".join(query.keywords), text=query.query)
    #
    # q.save()
    #
    # result = Query.search("lama")
    #
    # return result


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
    results = collection.query(
        query_texts=[query.query],
        n_results=10,
    )

    return results.get("documents", [])


@app.get("/weather")
async def weather(weather: Weather = Depends(Weather)):
    result = await weather.forecast()
    if not result:
        raise HTTPException(status_code=404, detail="Error fetching weather data")
    return result
