import http
import logging

from fastapi import FastAPI
from pydantic import ValidationError
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from schemas.error_schema import ErrorSchema
from scripts.seed_data import seed_data
from src.web.routes import main_router
from web.dependencies.db_dependency import DBDependency

logger = logging.getLogger(__name__)
seed_data(DBDependency())

app = FastAPI()
app.include_router(main_router)

@app.exception_handler(ValidationError)
def validation_error_exception_handler(_: Request, exc: ValidationError):
    """Handler for Pydantic validation errors.
    
    Returns 400 Bad Request response with validation error details.
    """
    logger.error("Validation Error. %s", str(exc))
    status_code = status.HTTP_400_BAD_REQUEST
    error = ErrorSchema(
        status_code=status_code,
        error=http.HTTPStatus(status_code).phrase,
        details=exc.errors(include_input=False),
    )

    return JSONResponse(content=error.model_dump(), status_code=status_code)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_: Request, exc: StarletteHTTPException):
    """Handler for FastAPI/Starlette HTTP exceptions.
    
    Returns response with appropriate HTTP status code.
    Details are not included for 500 errors.
    """
    logger.error("Starlette HTTPException. %s", str(exc))
    status_code = exc.status_code
    details = []

    if status_code != status.HTTP_500_INTERNAL_SERVER_ERROR:
        details.append(exc.detail)

    error = ErrorSchema(
        status_code=status_code,
        error=http.HTTPStatus(status_code).phrase,
        details=details,
    )

    return JSONResponse(error.model_dump(), status_code)


@app.exception_handler(Exception)
async def global_exception_handler(_: Request, exc: Exception):
    """Global handler for all unhandled exceptions.
    
    Returns 500 Internal Server Error response without details
    (for security, does not expose internal error information).
    """
    logger.error("Unknown Exception. %s", str(exc))

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error = ErrorSchema(
        status_code=status_code,
        error=http.HTTPStatus(status_code).phrase,
        details=None,
    )
    return JSONResponse(error.model_dump(), status_code)

