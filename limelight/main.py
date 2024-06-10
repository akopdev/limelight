from fastapi import Depends, FastAPI, HTTPException

from .skills import Weather

app = FastAPI()


@app.get("/query")
async def read_item(query: str):
    return {"query": query}


@app.get("/weather")
async def weather(weather: Weather = Depends(Weather)):
    result = await weather.forecast()
    if not result:
        raise HTTPException(status_code=404, detail="Error fetching weather data")
    return result
