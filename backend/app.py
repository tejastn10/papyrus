from fastapi import FastAPI

from routers import health

app = FastAPI(
    title="Papyrus",
    description="Secure API for removing and adding passwords from and to PDF",
    version="0.0.1",
)

app.include_router(health.router)
