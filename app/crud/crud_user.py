from app.crud.base import CRUDBase
from app.models import UserModel
from app.schemas import CreateUser, UpdateUser


class CRUDUser(CRUDBase[UserModel, CreateUser, UpdateUser]):
    ...


user = CRUDUser(UserModel)
