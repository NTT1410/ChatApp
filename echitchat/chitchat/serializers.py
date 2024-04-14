from rest_framework import serializers

from .models import Message, User, Connection, Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data['password'])
        user.save()

        return user


class ConnectionSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()
    class Meta:
        model = Connection
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    connection = ConnectionSerializer()
    user = UserSerializer()

    class Meta:
        model = Message
        fields = '__all__'

# class FriendSerializer(serializers.ModelSerializer):
#