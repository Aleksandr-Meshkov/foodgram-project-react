from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """ Разрешение для просмотра: неавторизованный пользователь
    пользователям если метод безопасный,
    остальные операции доступны только автору или админу. """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or
            obj.author == request.user or request.user.is_staff
        )
