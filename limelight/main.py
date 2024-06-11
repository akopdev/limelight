from fastapi import Depends, FastAPI, HTTPException

from .skills import Weather
from .storage import collection
from .query import process_query

app = FastAPI()


@app.get("/query")
async def search(q: str):

    query = await process_query(q)

    weather_related_keywords = [
        "weather",
        "forecast",
        "temperature",
        "humidity",
        "wind",
        "raining",
        "snow",
        "storm",
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
