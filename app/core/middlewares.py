from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware



class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            # Aquí puedes registrar el error en un sistema de logs
            print(f"Error: {exc}")
            raise



def setup_meddlewares_handlers(app: FastAPI):
    app.add_middleware(ErrorLoggingMiddleware)
