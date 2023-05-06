from django.contrib.auth import get_user_model
from rest_framework import serializers

from friends.models import Friends

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class GetUserSerializer(serializers.ModelSerializer):
    friendship_status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'friendship_status')

    def get_friendship_status(self, obj):
        current_user = self.context['request'].user
        friend_request_sent = Friends.objects.filter(
            friend_request_sender=current_user, friend_request_receiver=obj).exists()

        friend_request_received = Friends.objects.filter(
            friend_request_sender=obj, friend_request_receiver=current_user).exists()

        if friend_request_sent and friend_request_received:
            return 'Уже друзья'
        elif friend_request_sent:
            return 'Есть исходящий запрос в друзья'
        elif friend_request_received:
            return 'Есть входящий запрос в друзья'
        return 'Нет запросов на дружбу'


class AddToFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ('friend_request_receiver', 'friend_request_sender')

    def create(self, validated_data):
        user = self.context['request'].user
        friend_request_receiver = validated_data[
            'friend_request_receiver'].username
        if validated_data['friend_request_receiver'] == user:
            raise serializers.ValidationError(
                {'error': 'Вы не можете добавить себя в друзья'})
        if self.Meta.model.objects.filter(
                application_status=Friends.APPLICATION_STATUS.PENDING,
                friend_request_receiver=validated_data[
                    'friend_request_receiver'],
                friend_request_sender=user).exists():
            raise serializers.ValidationError(
                {'error': 'Заявка на добавление в друзья пользователя '
                          f'{friend_request_receiver} уже отправлена'})
        return self.Meta.model.objects.create(
            friend_request_receiver=validated_data['friend_request_receiver'],
            friend_request_sender=user)


class CurrentOrIncomingFriendSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='friend_request_sender.username',
        read_only=True
    )

    class Meta:
        model = Friends
        fields = ('username',)


class OutRequestFriendSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='friend_request_receiver.username',
        read_only=True
    )

    class Meta:
        model = Friends
        fields = ('username',)