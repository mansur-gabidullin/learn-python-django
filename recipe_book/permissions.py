from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS


class IsReadOnly(BasePermission):
    """
    The request is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)


class DeleteOnlyAdminUser(IsAdminUser):
    """
    The request is a read-only request.
    """

    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return super(DeleteOnlyAdminUser, self).has_permission(request, view)
        return True
