from fastapi import FastAPI

app = FastAPI(title="Template FastAPI", description="Description template FastAPI", version="0.1.0")

@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World"}