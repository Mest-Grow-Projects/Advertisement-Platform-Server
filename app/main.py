from fastapi import FastAPI

app = FastAPI(
    title="Advertisement Management Platform API Documentation",
    description="API documentation for the Advertisement Management Platform.",
    version="1.0.0",
)

@app.get(
    "/",
    tags=["App"],
    summary="Application base route"
)
def get_homepage():
    return {"message": "Welcome to the Advertisement Management Platform API!"}