from fastapi import BackgroundTasks, FastAPI, HTTPException
from starlette.responses import FileResponse

from .extensions import Weather
from .models import Document, Query, Summary
from .schemas import (SearchResultDocument, SearchResultExtension,
                      SearchResults, SearchSummary)

app = FastAPI()


@app.get("/")
async def index():
    return FileResponse("static/index.html")


@app.get("/search")
async def search(q: str, background_tasks: BackgroundTasks):
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

    weather = Weather(query)
    if weather.enabled:
        if weather_results := await weather.search():
            return SearchResults(
                id=query.id,
                query=query.text,
                extensions=[SearchResultExtension(name=weather.name, results=weather_results)],
            )

    documents = Document.search(query)

    summary = Summary(query=query.text, documents=[doc.id for doc in documents[:3]])
    summary.save()

    background_tasks.add_task(summary.generate)

    return SearchResults(
        id=query.id,
        query=query.text,
        documents=[
            SearchResultDocument(url=doc.url, title=doc.title, description=doc.text)
            for doc in documents[3:]
        ],
        summary=SearchSummary(
            id=summary.id,
            documents=[
                SearchResultDocument(url=doc.url, title=doc.title, description=doc.text)
                for doc in documents[:3]
            ],
        ),
    )


@app.get("/summary/{id}")
async def get_summary(id: str):
    summary = Summary.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    documents = [Document.get(doc) for doc in summary.documents]
    return SearchSummary(
        id=summary.id,
        text=summary.text,
        documents=[
            SearchResultDocument(url=doc.url, title=doc.title, description=doc.text)
            for doc in documents
        ],
    )
