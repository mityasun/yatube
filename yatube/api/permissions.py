from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Проверяем юзера на авторство. Для остальных только чтение."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user or request.method
                in permissions.SAFE_METHODS
                )
