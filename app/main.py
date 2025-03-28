from fastapi import FastAPI

from app.routers import collection_router


app = FastAPI()
app.include_router(collection_router)
