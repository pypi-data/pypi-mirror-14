from friendship.models import Friend
from rest_framework import permissions

from django.contrib.auth import get_user_model

User = get_user_model()


class IsFriend(permissions.BasePermission):
    def __init__(self, user_attr=None, actions=('create', 'list')):
        self.user_attr = user_attr
        self.actions = actions

    def __call__(self):
        return self

    """
    List-level permission to only allow owners of a list of objects to edit it.
    Assumes the list URL has the attribute specified as attr, otherwise
    it assumes the list itself has parent_lookup_user (NestedViewSet) to compare to authenticated User.
    """
    def has_permission(self, request, view):
        if view.action in self.actions:
            user_attr = view.kwargs.get(self.user_attr) if self.user_attr else view.kwargs.get('parent_lookup_user')
            user_pk = int(user_attr) if user_attr else None
            filtered_on_user = User.objects.get(pk=user_pk)
            are_friends = Friend.objects.are_friends(request.user, filtered_on_user)
            return True if are_friends else False
        else:
            return super(IsFriend, self).has_permission(request, view)

    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has the attribute specified as attr, otherwise
    it assumes the object itself is a User object to compare to authenticated User.
    """
    def has_object_permission(self, request, view, obj):
        if self.user_attr:
            return getattr(obj, self.user_attr) == request.user
        else:
            return obj == request.user
