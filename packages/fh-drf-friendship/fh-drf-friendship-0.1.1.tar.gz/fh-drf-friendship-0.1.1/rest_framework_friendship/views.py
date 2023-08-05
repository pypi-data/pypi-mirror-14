from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import module_loading
from friendship.models import Friend, FriendshipRequest
from rest_condition import Or
from rest_framework import permissions, viewsets, mixins, status, exceptions
from rest_framework.views import Response
from rest_framework_common.permissions import IsOwner
from rest_framework_extensions.mixins import NestedViewSetMixin

from .permissions import IsFriend
from .serializers import FriendSerializer, FriendReadSerializer
from .serializers import FriendshipRequestSerializer, FriendshipRequestReadSerializer

User = get_user_model()
UserListSerializer = module_loading.import_string(settings.DRF_FRIENDSHIP['USER_LIST_SERIALIZER'])


class FriendshipRequestViewSet(NestedViewSetMixin, mixins.ListModelMixin, mixins.CreateModelMixin,
                               mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendshipRequestReadSerializer

    def get_object(self):
        from_user = self.get_parents_query_dict().get('user')
        to_user = self.kwargs.get('pk')
        return FriendshipRequest.objects.filter(
            Q(to_user=to_user, from_user=from_user) |
            Q(to_user=from_user, from_user=to_user)
        ).distinct().first()

    def get_queryset(self):
        direction = self.request.query_params.get('direction')

        user = User.objects.get(pk=self.kwargs.get('parent_lookup_user'))

        if direction == 'inbound':
            return Friend.objects.unrejected_requests(user=user)
        if direction == 'outbound':
            return Friend.objects.sent_requests(user=user)

        return FriendshipRequest.objects.select_related('from_user', 'to_user').filter(
            Q(from_user=user) |
            Q(to_user=user, rejected__isnull=True)
        ).order_by('-created').all()

    def create(self, request, *args, **kwargs):
        request.data['from_user'] = self.get_parents_query_dict()['user']
        serializer = FriendshipRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        serializer = FriendshipRequestReadSerializer(instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        """
        Need to determine whether we sent the request and are canceling or
        if someone sent it to us and we're rejecting, django-friendship internal
        caching handles each slightly differently.
        """
        if not instance:
            raise exceptions.NotFound()

        from_user = self.get_parents_query_dict().get('user')

        if unicode(instance.from_user.pk) == from_user:
            instance.cancel()
        else:
            instance.reject()


class FriendshipRequestOutboundViewSet(NestedViewSetMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    # TODO Should only allow a user to view their own outbound
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendshipRequestReadSerializer

    def get_queryset(self):
        return Friend.objects.sent_requests(user=self.request.user)


class FriendshipRequestInboundViewSet(NestedViewSetMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    # TODO Should only allow a user to view their own outbound
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendshipRequestReadSerializer

    def get_queryset(self):
        return Friend.objects.unrejected_requests(user=self.request.user)


class FriendViewSet(NestedViewSetMixin, mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = UserListSerializer
    permission_classes = (permissions.IsAuthenticated, Or(IsOwner, IsFriend))

    def create(self, request, *args, **kwargs):
        request.data['to_user'] = self.get_parents_query_dict()['user']
        serializer = FriendSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            headers = self.get_success_headers(serializer.data)
            serializer = FriendReadSerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        # TODO This won't work if we ever allow you to look at another friends friends
        return Friend.objects.friends(self.request.user)

    def destroy(self, request, *args, **kwargs):
        to_user = User.objects.get(pk=self.get_parents_query_dict().get('user'))
        from_user = User.objects.get(pk=self.kwargs.get('pk'))
        Friend.objects.remove_friend(to_user, from_user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        to_user = User.objects.get(pk=self.get_parents_query_dict().get('user'))
        from_user = User.objects.get(pk=self.kwargs.get('pk'))
        return Friend.objects.get(to_user=to_user, from_user=from_user)
