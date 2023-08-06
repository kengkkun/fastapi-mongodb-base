from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from umongo import Document

from app.utils import check_uuid

ModelType = TypeVar("ModelType", bound=Document)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, uid: str) -> Optional[ModelType]:
        return await self.model.find_one({"uid": str(uid)})

    async def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        cursor = self.model.find()
        return [i async for i in cursor.skip(skip).limit(limit)]

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in = check_uuid(obj_in=obj_in)
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)  # type: ignore
        await db_obj.commit()
        return db_obj

    async def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = db_obj.dump()
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        await db_obj.commit()
        return db_obj

    async def remove(self, uid: str) -> ModelType:
        obj = await self.model.find_one({"uid": str(uid)})
        await obj.delete()
        return obj
