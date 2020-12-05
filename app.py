import os
import time

from typing import Union
from fastapi import FastAPI, Request, Response, status
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import PlainTextResponse

from api.utils.http_data_models import DummyRequest, DummyResponse
from api.utils import get_logger

app = FastAPI()

# Set API Key Authentication Related Variables
API_KEY = os.getenv("API_TOKEN")

# Setup logger
logger = get_logger()

logger.info("API is up and now listening...")


@app.middleware("http")
async def check_api_key(request: Request, call_next):
    """
    This is a FastAPI ASGI middleware function (https://fastapi.tiangolo.com/tutorial/middleware/)
    that checks if the API Key in the request is valid.

    If there is no API Key provided, a plain text response "No API Token Provided" with HTTP status 403 is returned

    If the API Key in the request is invalid, a plain text response "Wrong API Token" with HTTP status 403 is returned

    If the API Key in the response is correct, this function gets the response from the path operation function and
    returns it as-is.

    :param request: represents the
    :param call_next: a callable, the path operation function the request was originally aiming at

    :return: starlette.PlainTextResponse with HTTP status code 403 in case of error, otherwise
                response from the path operation function.
    """
    logger.info("Running API token based authentication")

    if request.url.path.strip("/") not in ['health', 'deployment_color']:
        supplied_api_key = request.headers.get("x-api-key")
        
        if supplied_api_key is None:
            logger.warning("No API token provided")
            return PlainTextResponse(
                "No API Token Provided",
                status_code=HTTP_403_FORBIDDEN
            )
        elif not supplied_api_key == API_KEY:
            logger.warning("Wrong API token provided.")
            return PlainTextResponse(
                "Wrong API Token",
                status_code=HTTP_403_FORBIDDEN
            )
        else:
            logger.info("API token verified!")
            
    start_time = time.time()

    response = await(call_next(request))

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"Request processed in {formatted_process_time}ms ")

    return response


@app.get('/deployment_color/', status_code=200, response_model=str)
def deployment_color_endpoint():
    """
    This endpoint is used to check the health of the API by monitoring and alerting services.
    """
    return_message = ""
    
    deployment_color = os.getenv("DEPLOYMENT_COLOR")
    
    if deployment_color is None:
        logger.debug("Not a colored deployment.")
        return_message = "Not a colored deployment."
    else:
        return_message = deployment_color

    logger.debug("Processed deployment color request.")

    return return_message


@app.get('/health/', status_code=200, response_model=str)
def health_endpoint():
    """
    This endpoint is used to check the health of the API by monitoring and alerting services.
    """
    logger.debug("Processed health-check request.")

    return "API health ok."


@app.get('/dummy/', status_code=200, response_model=str)
def dummy_get_endpoint():
    """
    The FastAPI path operation function that is triggered when a GET request to the
    endpoint `/dummy` is made.

    This is just a dummy endpoint. It doesn't do anything except for returning a line of text.

    It can be used to test that the app is up and the connection is working.
    """
    logger.info("Processed GET request.")

    return "API Is Accessible."


@app.post('/dummy/', status_code=200, response_model=Union[DummyResponse, str])
async def dummy_post_endpoint(request: DummyRequest, response: Response):
    """
    The FastAPI path operation function that is triggered when a POST request to the
    endpoint `/dummy` is made.

    Request must contain a JSON body like this:

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

    logger.info("Parsing received POST request and extracting data ...")
    num_responses = request.num_responses

    logger.info("Performing validation checks on input data ...")
    if not 0 < num_responses < 100:  # Note how you don't need to perform type validations; FastAPI does it for you
        error_message = f"Invalid num_responses value {num_responses}. Must be between 0 and 100 (not inclusive)."
    else:
        logger.info("Validation checks passed.")
        logger.info("Computing responses ...")

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


if __name__ == "__main__":
    from fastapi.testclient import TestClient

    client = TestClient(app)
    
    post_body = {
        "num_responses": 5
    }

    response = client.post(
        "/dummy/",
        headers={"x-api-key": os.getenv("API_TOKEN"), "Content-Type": "application/json"},
        json=post_body
    )

    print(response.status_code)