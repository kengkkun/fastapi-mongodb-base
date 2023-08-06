from typing import List, Optional

from fastapi import APIRouter
from pydantic import UUID4

from app import schemas, crud
from app.utils.exceptions.general import IdNotFoundException

router = APIRouter()


@router.get("/", response_model=Optional[List[schemas.UserDB]])
async def get_users(
        *,
    limit: int = 20,
    skip: int = 0
):
    obj_db = await crud.user.get_multi(skip=skip, limit=limit)
    return obj_db


@router.get("/{uid}", response_model=Optional[schemas.UserDB])
async def get_user(
        *,
        uid: UUID4
):
    obj_db = await crud.user.get(uid)
    return obj_db


@router.post("/", response_model=Optional[schemas.UserDB])
async def create_user(*, obj_in: schemas.CreateUser):
    obj_db = await crud.user.create(obj_in=obj_in)
    return obj_db


@router.put("/{uid}", response_model=Optional[schemas.UserDB])
async def update_user(*, uid: UUID4, obj_in: schemas.CreateUser):
    user = await crud.user.get(uid)
    if not user:
        raise IdNotFoundException(uid)
    obj_db = await crud.user.update(db_obj=user, obj_in=obj_in)
    return obj_db


@router.delete("/{uid}", response_model=Optional[schemas.UserDB])
async def delete_user(*, uid: UUID4):
    obj_db = await crud.user.remove(uid)
    return obj_db

