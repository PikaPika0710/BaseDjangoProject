from enum import Enum


class RoleData(Enum):
    USER = {
        "id": "aef45b7b6f9745428594caa9ed3ec5f8",
        "name": "USER"
    }
    ADMIN = {
        "id": "af63504a122c406f9fd9f3b7162b7591",
        "name": "ADMIN"
    }

    # @classmethod
    # def get_by_id(cls, role_id):
    #     for role in RoleData:
    #         if role.value.get('id') == role_id:
    #             return role
    #     return None
