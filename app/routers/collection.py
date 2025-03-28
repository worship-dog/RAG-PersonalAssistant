from fastapi import APIRouter, Depends

from app.utils import get_db


router = APIRouter(
    prefix="/collection",
    tags=["collection"],
    dependencies=[Depends(get_db)]
)


@router.post("/")
def create_collection():
    pass
