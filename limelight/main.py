from typing import List

from fastapi import Depends, FastAPI, HTTPException
from starlette.responses import FileResponse

from .extensions import Weather, Summary
from .models import Document, Query
from .schemas import SearchResultDocument, SearchResultExtension, SearchResults

app = FastAPI()


@app.get("/")
async def index():
    return FileResponse("static/index.html")


@app.get("/search")
async def search(q: str):
    query = Query.parse_text(q)
    if not query:
        raise HTTPException(status_code=400, detail="Error processing query")
    # id = query.save()

    # Based on user search request type, we will determine the best approach to handle the request
    # For example, if the user is searching for weather-related information, we will call
    # the weather extension instead of querying the database. If user is exploring a topic, we will
    # try to collect as much information as possible from the database and summarize it for the
    # easy consumption of the user. For simple keyword-based search, we will query the database and
    # return the results as fast as possible.

    # Search result candidates in the database
    documents = Document.search(query.text)

    available_extensions = [Weather, Summary]

    # This is a runtime execution of the extensions. We can run them in background tasks
    # to speed up the response time.
    extensions: List[SearchResultExtension] = []
    for extension in available_extensions:
        ext = extension(query.text)
        if ext.enabled:
            extensions.append(
                SearchResultExtension(name=ext.name, results=await ext.run(documents=documents))
            )

    return SearchResults(
        id=query.id,
        query=query.text,
        documents=[
            SearchResultDocument(url=doc.url, title=doc.title, description=doc.text)
            for doc in documents
        ],
        extensions=extensions,
    )


@app.get("/weather")
async def weather(weather: Weather = Depends(Weather)):
    result = await weather.forecast()
    if not result:
        raise HTTPException(status_code=404, detail="Error fetching weather data")
    return result
