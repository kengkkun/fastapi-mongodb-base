import uuid

from umongo import Document, fields

from app.db.database import instance


@instance.register
class UserModel(Document):
    uid = fields.StringField(unique=True, allow_none=False, default=str(uuid.uuid4()))
    username = fields.StringField(required=True)
    address = fields.StringField(allow_none=True)
    phone = fields.StringField(allow_none=True)
