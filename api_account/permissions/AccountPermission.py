from api_account.constants import RoleData
from api_base.permissions.Permission import MyBasePermission


class AdminPermission(MyBasePermission):
    match_any_roles = [RoleData.ADMIN]


class UserPermission(MyBasePermission):
    match_any_roles = [RoleData.USER]


class BothPermission(MyBasePermission):
    match_any_roles = [RoleData.ADMIN, RoleData.USER]
