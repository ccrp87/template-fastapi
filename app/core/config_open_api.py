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
                if "422" in responses and responses["422"]["content"]["application/json"]["schema"]["$ref"].endswith("HTTPValidationError"):
                    del responses["422"]
        return res

    return wrapper


doc_responses = {
    200:{
        "description": "Operación exitosa",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": {
                        "user_name": "john.doe",
                        "email": "john.doe@localhost",
                        "token": "eyJ0eXAi.8XhQ4zZQ.v9vz5"
                        
                        },
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
                    }}}}
    },
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
    401: {
        "description": "No autorizado",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": {
                        "message": "Message of the error",
                        "type": "BusinessLogicError",
                    },
                }
            }
        },
    },
    403: {
        "description": "No permitido",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": {
                        "message": "Message of the error",
                        "type": "BusinessLogicError",
                    },
                }
    }}},
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
