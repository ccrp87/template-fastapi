from typing import Callable


def customize_openapi(func: Callable[..., dict]) -> Callable[..., dict]:
    """Customize OpenAPI schema."""

    def wrapper(*args, **kwargs) -> dict:
        """Wrapper."""
        res = func(*args, **kwargs)
        for _, method_item in res.get("paths", {}).items():
            for _, param in method_item.items():
                responses = param.get("responses")
                # remove default 422 - the default 422 schema is HTTPValidationError
                if "422" in responses and responses["422"]["content"][
                    "application/json"
                ]["schema"]["$ref"].endswith("HTTPValidationError"):
                    del responses["422"]
        return res

    return wrapper


doc_responses = {
    400: {
        "description": "Validaciones de negocio fallidas",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": {
                        "message": "Message of the error",
                        "type": "BusinessLogicError",
                        "errors": [
                            {
                                "type": "string",
                                "loc": [],
                                "msg": "string",
                                "input": 1,
                            }
                        ],
                    },
                }
            }
        },
    },
    404: {
        "description": "Recurso no encontrado",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": {
                        "message": "Data not found",
                        "type": "BusinessLogicError",
                    },
                }
            }
        },
    },
    500: {
        "description": "Error interno del servidor",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": {
                        "message": "An unexpected error occurred.",
                        "type": "UnhandledError",
                    },
                }
            }
        },
    },
}
