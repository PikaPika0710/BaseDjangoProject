from rest_framework.permissions import BasePermission


class MyBasePermission(BasePermission):
    match_any_roles = []

    def has_permission(self, request, view):
        account = request.user
        if not self.match_any_roles:
            return True
        if account.is_anonymous:
            return False
        for role in self.match_any_roles:
            if account.role.id.hex == role.value.get('id'):
                return True
        return False
