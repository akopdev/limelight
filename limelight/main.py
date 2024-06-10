from fastapi import Depends, FastAPI, HTTPException

from .models import Query
from .skills import Weather

app = FastAPI()


@app.get("/query")
async def search(query: Query = Depends(Query)):
    return {"resPonse": query.process()}


@app.get("/weather")
async def weather(weather: Weather = Depends(Weather)):
    result = await weather.forecast()
    if not result:
        raise HTTPException(status_code=404, detail="Error fetching weather data")
    return result
