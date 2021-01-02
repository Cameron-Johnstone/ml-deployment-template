from typing import List
from pydantic import BaseModel

"""
The classes in this file are all Pydantic models.

FastAPI can use these Pydantic models to validate arguments (requests) and returned objects (responses)
from the path operation functions (the functions decorated with @app.get, @app.post, etc.).
"""


class DummyRequest(BaseModel):
    """
    This model represents the JSON body of POST request to endpoint `/dummy`
    """
    num_responses: int


class DummyResponse(BaseModel):
    """
    This model represents the JSON body of valid responses to POST requests made to the endpoint `/dummy`
    """
    response_values: List[int]
    message: str


class SentenceComparatorRequest(BaseModel):
    """
    This model represents the JSON body of POST request to endpoint `/sentence_compare`
    """
    sentence_1: str
    sentence_2: str


class SentenceComparatorResponse(BaseModel):
    """
    This model represents the JSON body of valid responses to POST requests made to the endpoint `/sentence_compare`
    """
    sentence_similarity_score: str