from fastapi import Depends, FastAPI, HTTPException
from starlette.responses import FileResponse

from .models import Document, Query
from .schemas import SearchResultItem, SearchResults
from .skills import Weather

app = FastAPI()


@app.get("/")
async def index():
    return FileResponse("static/index.html")


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
    if query.keywords and any(keyword in query.keywords for keyword in weather_related_keywords):
        # Call the weather skill with the query
        result = await Weather().forecast()
        return result

    # Search result candidates in the database
    documents = Document.search(query.text, query.keywords)
    # if documents:
    #     # Generate a human-readable response
    #     query.summarise(documents[:3])

    return SearchResults(
        id=query.id,
        query=query.text,
        results=[
            SearchResultItem(url=doc.url, title=doc.title, description=doc.text)
            for doc in documents
        ],
    )


@app.get("/weather")
async def weather(weather: Weather = Depends(Weather)):
    result = await weather.forecast()
    if not result:
        raise HTTPException(status_code=404, detail="Error fetching weather data")
    return result
