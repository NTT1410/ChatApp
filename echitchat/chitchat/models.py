from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save


# Create your models here.

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['id']


class User(AbstractUser):

    def __str__(self):
        return self.username

    def profile(self):
        profile = Profile.objects.get(user=self)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, default="")
    last_name = models.CharField(max_length=150, default="")
    full_name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="user_images", default="default.jpg")
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.full_name == "" or self.full_name == None:
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


class Connection(BaseModel):
    sender = models.ForeignKey(
        User,
        related_name='sent_connections',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User,
        related_name='received_connections',
        on_delete=models.CASCADE
    )
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.sender.username + ' -> ' + self.receiver.username

    class Meta:
        unique_together = [['sender', 'receiver']]

    def clean(self):
        # Kiểm tra xem đã tồn tại Connection giữa 2 User theo cả hai hướng chưa
        if Connection.objects.filter(sender=self.sender, receiver=self.receiver).exists() or \
                Connection.objects.filter(sender=self.receiver, receiver=self.sender).exists():
            raise ValidationError("A connection between these users already exists.")
        # Thêm bất kỳ điều kiện ràng buộc dữ liệu nào khác ở đây nếu cần

    def save(self, *args, **kwargs):
        self.clean()
        super(Connection, self).save(*args, **kwargs)


class Group(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class GroupMember(BaseModel):
    group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} is a member of {self.group.name}'

    class Meta:
        unique_together = ('group', 'user')


class Message(BaseModel):
    connection = models.ForeignKey(Connection, related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, related_name='my_messages', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ': ' + self.message

    def clean(self):
        # Kiểm tra xem tin nhắn có thuộc về một kết nối hoặc một nhóm không
        if (self.connection is None and self.group is None) or (self.connection and self.group):
            raise ValidationError("Message must be linked to a connection or a group, not both.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
