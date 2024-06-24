from typing import List

from fastapi import Depends, FastAPI, HTTPException
from starlette.responses import FileResponse

from .models import Document, Query
from .schemas import SearchResultDocument, SearchResults, SearchResultSkill
from .skills import Weather

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
    # the weather skill instead of querying the database. If user is exploring a topic, we will
    # try to collect as much information as possible from the database and summarize it for the
    # easy consumption of the user. For simple keyword-based search, we will query the database and
    # return the results as fast as possible.

    skills = [Weather]

    # Check if any skill is enabled
    skills_results: List[SearchResultSkill] = []
    for skill in skills:
        s = skill(query.text)
        if s.enabled:
            print("Running skill:", s.name)
            skills_results.append(SearchResultSkill(name=s.name, results=await s.run()))

    # If any skill results are found, return them without querying the database
    if skills_results:
        return SearchResults(
            id=query.id,
            query=query.text,
            skills=skills_results,
        )

    # Search result candidates in the database
    documents = Document.search(query.text, query.keywords)
    # if documents:
    #     # Generate a human-readable response
    #     query.summarise(documents[:3])
    #     query.save()

    return SearchResults(
        id=query.id,
        query=query.text,
        documents=[
            SearchResultDocument(url=doc.url, title=doc.title, description=doc.text)
            for doc in documents
        ],
    )


@app.get("/weather")
async def weather(weather: Weather = Depends(Weather)):
    result = await weather.forecast()
    if not result:
        raise HTTPException(status_code=404, detail="Error fetching weather data")
    return result
