from rest_framework import viewsets, status, generics, parsers, permissions
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Message, Connection, User, Group, GroupMember
from .serializers import UserSerializer, MessageSerializer, ConnectionSerializer


class MessageViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["get"], detail=False)
    def get_last_message(self, request):
        user = request.user
        # Lấy user hiện tại
        # user = request.user
        # Lấy tất cả tin nhắn liên quan đến user hiện tại, bao gồm cả đã gửi và đã nhận
        messages = Message.objects.filter(
            Q(connection__sender=user) | Q(connection__receiver=user) | Q(group__memberships__user=user)
        ).distinct()
        # Serialize dữ liệu tin nhắn
        serializer = MessageSerializer(messages, many=True)
        # Trả về response
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True)
    def get_connection_messages(self, request, pk):

        # Lấy user hiện tại
        user = request.user
        connection = Connection.objects.filter(
            id=pk,
            sender=user
        ).first() or Connection.objects.filter(
            id=pk,
            receiver=user
        ).first()
        if connection:
            messages = Message.objects.filter(connection=connection)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

            # Không cần thiết vì get_object_or_404 đã xử lý việc nếu không tìm thấy đối tượng
        return Response({"message": "Connection not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def get_group_messages(self, request, pk):
        user = request.user

        if not Group.objects.filter(pk=pk).exists():
            return Response({"message": "Group not found."}, status=status.HTTP_404_NOT_FOUND)
        # Kiểm tra xem user có phải là thành viên của nhóm không
        if not GroupMember.objects.filter(Q(group__id=pk, user__id=user.id)).exists():
            return Response({"message": "You are not a member of this group."}, status=status.HTTP_403_FORBIDDEN)

        # Lấy tất cả tin nhắn trong nhóm
        messages = Message.objects.filter(group__id=pk)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        user = request.user

        connection_id = request.data.get('connection', None)
        group_id = request.data.get('group', None)
        message_text = request.data.get('message')

        try:
            user = User.objects.get(id=user.id)
        except User.DoesNotExist:
            return Response({"error": "Người dùng không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

        if connection_id:
            connection = Connection.objects.get(id=connection_id)
        else:
            connection = None

            # Tương tự với group_id
        if group_id:
            group = Group.objects.get(id=group_id)
        else:
            group = None

            # Đảm bảo rằng có ít nhất connection hoặc group được chỉ định
        if not connection and not group:
            return Response({"error": "Cần có kết nối hoặc nhóm để gửi tin nhắn."}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo và lưu tin nhắn mới
        message = Message.objects.create(
            user=user,
            connection=connection,
            group=group,
            message=message_text,
            is_read=False)
        message.save()

        # Trả về tin nhắn đã tạo
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


class ConnectionViewSet(viewsets.ViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], url_path='my-list-friends', detail=False)
    def my_list_friends(self, request):
        user = request.user
        connections = Connection.objects.filter(Q(sender=user) | Q(receiver=user))
        serializer = ConnectionSerializer(connections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='send-friend-request')
    def send_friend_request(self, request):
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        receiver = User.objects.get(pk=receiver_id)

        if sender == receiver:
            return Response({"error": "Bạn không thể tự gửi yêu cầu kết bạn cho chính mình."},
                            status=status.HTTP_400_BAD_REQUEST)

        if Connection.objects.filter(sender=sender, receiver=receiver).exists():
            return Response({"error": "Yêu cầu kết bạn đã được gửi trước đó."}, status=status.HTTP_400_BAD_REQUEST)

        connection = Connection.objects.create(sender=sender, receiver=receiver, accepted=False)
        return Response(ConnectionSerializer(connection).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='accept-friend-request')
    def accept_friend_request(self, request):
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        receiver = User.objects.get(pk=receiver_id)

        if sender == receiver:
            return Response({"error": "Bạn không thể tự gửi yêu cầu kết bạn cho chính mình."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Connection.objects.filter(sender=sender, receiver=receiver).exists():
            return Response({"error": "Yêu cầu kết bạn đã được gửi trước đó."}, status=status.HTTP_400_BAD_REQUEST)

        connection = Connection.objects.filter(sender=sender, receiver=receiver).first()
        connection.accepted = True
        # connection.save()
        return Response(ConnectionSerializer(connection).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='reject-friend-request')
    def decline_friend_request(self, request):
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        receiver = User.objects.get(pk=receiver_id)

        connection = Connection.objects.filter(sender=sender, receiver=receiver).first()
        connection.delete()
        # connection.save()
        return Response({"message": "Friend request rejected."}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]

    def get_permissions(self):
        if self.action in ['get_current']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current", detail=False)
    def get_current(self, request):
        return Response(UserSerializer(request.user, context={
            "request": request
        }).data, status=status.HTTP_200_OK)
