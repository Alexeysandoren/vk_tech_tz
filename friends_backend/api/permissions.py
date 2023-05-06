from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsRequestUserOrReadOlyFriends(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            obj.friend_request_receiver == request.user
            or request.method in SAFE_METHODS)