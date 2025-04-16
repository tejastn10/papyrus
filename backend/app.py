from fastapi import FastAPI

from routers import health

app = FastAPI(
    title="Papyrus",
    description="PDF editor and viewer",
    version="0.0.1",
)


@app.get("/")
async def root():
    return {"message": "Welcome to Papyrus!"}


app.include_router(health.router)
