from rest_framework import permissions


class IsOwnerOrModerator(permissions.BasePermission):
    """
    Разрешает доступ к объекту, если пользователь является владельцем
    или входит в группу 'Moderators'.
    """

    def has_object_permission(self, request, view, obj):
        # Модератор может редактировать любой объект
        if request.user.groups.filter(name="Moderators").exists():
            return True
        # Владелец объекта может редактировать только свои объекты
        return obj.owner == request.user


class IsModerator(permissions.BasePermission):
    """
    Разрешает доступ только модераторам.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderators").exists()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Позволяет редактировать объект только владельцу.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
