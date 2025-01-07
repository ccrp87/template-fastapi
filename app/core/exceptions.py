from http import HTTPStatus
from typing import Sequence
from fastapi import Request, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class BusinessLogicException(Exception):
    def __init__(
        self, message: str, code: int = HTTPStatus.BAD_REQUEST, errors: Sequence[any] = None
    ):
        self.message = message
        self.code = code
        self.errors = errors


async def business_logic_exception_handler(
    request: Request, exc: BusinessLogicException
):
    return JSONResponse(
        status_code=exc.code,
        content={
            "success": False,
            "status_code": exc.code,
            "error": {
                "message": exc.message,
                "type": "BusinessLogicError",
                "errors": exc.errors,
            },
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={
            "data": None,
            "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
            "success": False,
            "error": {
                "message": "An unexpected error occurred.",
                "type": "UnhandledError",
                "errors": exc.args,
            },
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):

    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={
            "success": False,
            "status_code": HTTPStatus.BAD_REQUEST,
            "error": {
                "message": "Datos de solicitud incorrectos",
                "type": "BusinessLogicError",
                "errors": exc.errors(),
            },
        },
    )


def setup_exception_handlers(app: FastAPI):
    """
    Registra los manejadores globales en la instancia de FastAPI.
    """
    app.add_exception_handler(BusinessLogicException, business_logic_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
