import os
import time

from typing import Union
from fastapi import FastAPI, Request, Response, status
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import PlainTextResponse

from api.utils.http_data_models import DummyRequest, DummyResponse
from api.utils.http_data_models import SentenceComparatorRequest, SentenceComparatorResponse
from api.utils import get_logger
from api.utils.setup import setup_api, setup_resources
from model import SentenceComparator

logger = get_logger()

sentence_transformer = setup_resources()
sentence_comparator = SentenceComparator(sentence_transformer)
logger.info("Model resources are loaded and initialized...")

app = FastAPI()
setup_api(app)
logger.info("API is now up and listening...")


@app.get('/deployment_color/', status_code=200, response_model=str)
def deployment_color_endpoint():
    """
    This endpoint is used to check the color of the deployment.
    """
    return_message = ""
    
    deployment_color = os.getenv("DEPLOYMENT_COLOR")
    
    if deployment_color is None:
        logger.debug("Received a request for the deployment color, but this is not a colored deployment.")
        return_message = "Not a colored deployment."
    else:
        return_message = deployment_color

    logger.debug("Processed deployment color request.")

    return return_message


@app.get('/health/', status_code=200, response_model=str)
def health():
    """
    This endpoint is used to check the health of the API by monitoring and alerting services.
    """
    logger.debug("Processed health-check request.")

    return "API health ok."


@app.get('/api_token_check/', status_code=200, response_model=str)
def api_token_check():
    """
    This endpoint is used to test that the API Token in the request is correct.
    """
    logger.info("Processed GET request.")

    return "API Token is correct."


@app.post('/dummy/', status_code=200, response_model=Union[DummyResponse, str])
async def dummy(request: DummyRequest, response: Response):
    """
    Request JSON body should look like this:

    {
        "num_responses" : 4
    }

    The value against the `"num_responses"` key must contain an integer greater than 0 and less than 100
    in order to get a valid response with HTTP status 200.

    :return: Response Sample:
                {
                    "response_values" : [1, 2, 3, 4],
                    "message" : "Retrieved 4 response values"
                }

            In normal circumstances, a JSON like the above is returned with HTTP status 200.
                `"response_values"`will contain an array of integers starting from 1 to the value in `"num_responses"`

            In case of an invalid request, an error message (a string) with HTTP client error status 422 is returned.

    :rtype: dict (conforming to DummyResponse Pydantic model), or str
    """

    response_body = {}
    error_message = ""

    logger.info("Parsing received POST request and extracting data...")
    num_responses = request.num_responses

    logger.info("Performing validation checks on input data...")
    if not 0 < num_responses < 100:  # Note how you don't need to perform type validations; FastAPI does it for you
        error_message = f"Invalid num_responses value {num_responses}. Must be between 0 and 100 (not inclusive)."
    else:
        logger.info("Validation checks passed")
        logger.info("Computing response...")

        response_body = {
            "response_values": [x for x in range(1, num_responses+1)],
            "message": f"Retrieved {num_responses} responses."
        }

    logger.info("Processed POST request.")
    if error_message:
        logger.warning(error_message)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        response_body = error_message

    return response_body


@app.post('/sentence_compare/', status_code=200, response_model=Union[SentenceComparatorResponse, str])
async def sentence_compare(request: SentenceComparatorRequest, response: Response):
    """
    Request JSON body should look like this:

    {
        "sentence_1" : "This is the first sentence.",
        "sentence_2": "This is the second sentence"
    }

    :return: Response Sample:
                {
                    "sentence_similarity_score": "0.6019590497016907"
                }

            In normal circumstances, a JSON like the above is returned with HTTP status 200.
                `"sentence_similarity_score"`will contain a stringified floating point number

    :rtype: dict (conforming to DummyResponse Pydantic model), or str
    """

    response_body = {}

    logger.info("Parsing received POST request and extracting data...")
    sentence_1 = request.sentence_1
    sentence_2 = request.sentence_2

    logger.info("Computing response...")
    sentence_similarity_score = sentence_comparator.get_similarity(sentence_1, sentence_2)
    response_body = {
        "sentence_similarity_score": str(sentence_similarity_score)
    }
    logger.info("Processed POST request")

    return response_body


if __name__ == "__main__":
    from fastapi.testclient import TestClient

    client = TestClient(app)
    
    post_body = {
        "num_responses": 5
    }

    response = client.post(
        "/dummy/",
        headers={
            "x-api-key": os.getenv("API_TOKEN"), 
            "Content-Type": "application/json"
        },
        json=post_body
    )

    print(response.status_code)