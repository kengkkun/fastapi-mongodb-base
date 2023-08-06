import uuid


def check_uuid(obj_in):
    if not obj_in.uid:
        obj_in.uid = str(uuid.uuid4())
    return obj_in
