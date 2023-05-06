from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.mixins import (CreateListRetrieveViewSet,
                        ListDestroyViewSet)
from api.permissions import IsRequestUserOrReadOlyFriends
from api.serializers import (AddToFriendsSerializer, CreateUserSerializer,
                             CurrentOrIncomingFriendSerializer, GetUserSerializer,
                             OutRequestFriendSerializer)
from friends.models import Friends


User = get_user_model()


class UserViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'

    def get_permissions(self):
        if self.request.method == 'POST':
            return ()
        return (IsAuthenticated(),)
        
    def get_serializer_class(self):
        if self.action == 'add_to_friends':
            return AddToFriendsSerializer
        if self.request.method == 'POST':
            return CreateUserSerializer
        return GetUserSerializer

    @action(detail=True, methods=['POST'])
    def add_to_friends(self, request, username):
        friend_request_receiver = get_object_or_404(
            User, username=username)
        serializer = self.get_serializer(
            data={'friend_request_receiver': friend_request_receiver.pk,
                  'friend_request_sender': request.user.pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'success': 'Заявку на добавление в друзья отправлена '
                        f'пользователю {friend_request_receiver}'},
                        status=status.HTTP_201_CREATED)
    


class FriendViewSet(ListDestroyViewSet):
    permission_classes = [IsRequestUserOrReadOlyFriends]
    model = Friends
    lookup_field = 'friend_request_sender__username'

    def get_serializer_class(self):
        if self.action == 'out_requests':
            return OutRequestFriendSerializer
        return CurrentOrIncomingFriendSerializer

    def get_queryset(self):
        if self.action in ['approve_request',
                           'decline_request',
                           'incoming_requests']:
            return self.model.objects.filter(
                friend_request_receiver=self.request.user,
                application_status=self.model.APPLICATION_STATUS.PENDING)

        elif self.action == 'out_requests':
            return self.model.objects.filter(
                friend_request_sender=self.request.user,
                application_status=self.model.APPLICATION_STATUS.PENDING)
        return self.model.objects.filter(
            friend_request_receiver=self.request.user,
            application_status=self.model.APPLICATION_STATUS.APPROVED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'success': f'Пользователь {instance} успешно удален из друзей'},
            status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def incoming_requests(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def out_requests(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['PATCH'])
    def approve_request(self, request,
                        friend_request_sender__username=None):
        friend = self.get_object()
        friend.application_status = self.model.APPLICATION_STATUS.APPROVED
        friend.save()
        Friends.objects.get_or_create(
            friend_request_receiver=friend.friend_request_sender,
            friend_request_sender=friend.friend_request_receiver,
            application_status=friend.APPLICATION_STATUS.APPROVED
        )
        return Response({'success':
                         f'Пользователь {friend} добавлен в друзья'})

    @action(detail=True, methods=['DELETE'])
    def decline_request(self, request,
                        friend_request_sender__username=None):
        friend = self.get_object()
        friend.delete()
        return Response({'success': f'Заявка пользователя {friend} на добавление в друзья отклонена'})