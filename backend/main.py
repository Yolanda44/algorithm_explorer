from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .algorithms import utils


class SortRequest(BaseModel):
    numbers: List[float]
    algorithm: str


class SearchRequest(BaseModel):
    numbers: List[float]
    target: float
    algorithm: str


app = FastAPI(title="Algorithm Explorer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health() -> dict:
    return {"status": "ok"}


@app.post("/sort")
def sort_numbers(request: SortRequest) -> dict:
    algo_key = utils.normalize_algorithm(request.algorithm)
    sorter = utils.SORTING_ALGORITHMS.get(algo_key)
    if sorter is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported sorting algorithm. Choose from: {', '.join(sorted(set(utils.SORTING_ALGORITHMS)))}",
        )
    return sorter(request.numbers)


@app.post("/search")
def search_numbers(request: SearchRequest) -> dict:
    algo_key = utils.normalize_algorithm(request.algorithm)
    searcher = utils.SEARCHING_ALGORITHMS.get(algo_key)
    if searcher is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported searching algorithm. Choose from: {', '.join(sorted(set(utils.SEARCHING_ALGORITHMS)))}",
        )
    return searcher(request.numbers, request.target)
