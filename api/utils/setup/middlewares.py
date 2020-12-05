import os
import time

from fastapi import Request
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api.utils import get_logger

logger = get_logger()


class ApiTokenMiddleware(BaseHTTPMiddleware):
    """An ASGI middleware that checks for the API Token. Certain paths are exempt from this check.

    Attributes
    ----------
    API_KEY : str
        The expected API Key
    excluded_paths : List[str]
        The set of paths (with '/' characters stripped) for which API Token will not be checked 

    Methods
    -------
    dipatch():
        Overridden from BaseHTTPMiddleware. Encapsulates the primary functionality for this middleware.
    """
    API_KEY: str = os.getenv("API_TOKEN")
    excluded_paths: list[str] = ['health', 'deployment_color']

    async def dispatch(self, request: Request, call_next):
        """
        If there is no API Key provided, a plain text response "No API Token Provided" with HTTP status 403 is returned

        If the API Key in the request is invalid, a plain text response "Wrong API Token" with HTTP status 403 is returned

        If the API Key in the response is correct, this function gets the response from the path operation function and
        returns it as-is.
        """
        logger.info("Running API token based authentication")

        if request.url.path.strip("/") not in self.excluded_paths:
            supplied_api_key = request.headers.get("x-api-key")
            
            if supplied_api_key is None:
                logger.warning("No API token provided")
                return PlainTextResponse("No API Token Provided", status_code=HTTP_403_FORBIDDEN)
            elif not supplied_api_key == self.API_KEY:
                logger.warning("Wrong API token provided.")
                return PlainTextResponse("Wrong API Token", status_code=HTTP_403_FORBIDDEN)
            else:
                logger.info("API token verified!")
                
        response = await(call_next(request))

        return response


class TimingMiddleware(BaseHTTPMiddleware):
    """An ASGI middleware that logs the time taken to process a request.

    Methods
    -------
    dipatch():
        Overridden from BaseHTTPMiddleware. Encapsulates the primary functionality for this middleware.
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await(call_next(request))

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        logger.info(f"Request processed in {formatted_process_time}ms ")
        
        return response
