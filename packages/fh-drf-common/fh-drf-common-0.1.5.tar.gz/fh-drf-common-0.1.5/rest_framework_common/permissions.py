from django.core.exceptions import PermissionDenied
from rest_framework import permissions


class RequirePassword(permissions.BasePermission):
    """
    When this permission is added to a view[set] it requires that the
    `password` field also be passed as part of the request, useful for change email/password type requests
    where you want to make sure the request actually has permission.
    """
    def has_permission(self, request, view):
        password = request.data.get('password')
        if not password or not request.user.check_password(password):
            raise PermissionDenied

        return True


class IsAuthenticatedOrReadOnlyOrCreate(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request, or non-authenticated create
    """
    def has_permission(self, request, view):
        if (request.method in ['GET', 'HEAD', 'OPTIONS'] or
                (request.user and request.user.is_authenticated()) or
                    request.method == 'POST'):
            return True
        return False


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has the attribute specified as attr, otherwise
    it assumes the object itself is a User object to compare to authenticated User.
    """
    def __init__(self, user_attr=None):
        self.user_attr = user_attr

    def __call__(self):
        return self

    def has_object_permission(self, request, view, obj):
        if self.user_attr:
            return getattr(obj, self.user_attr) == request.user
        else:
            return obj == request.user
