from rest_framework import serializers

from djangoTest.user_model import User

from app.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            "id",
            "name",
            "email",
            "orders"
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "photo",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
        )


class NotificationSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    from_email = serializers.EmailField()
    recipient_list = serializers.ListField(child=serializers.EmailField())
    content_type = serializers.ChoiceField(choices=["text", "html"])
    notification_type = serializers.ChoiceField(choices=["email", "outlook"])
    files = serializers.ListField(child=serializers.FileField(), required=False)

    def validate(self, attrs):
        if attrs['notification_type'] == "email":
            files_data = []
            for file in attrs['files']:
                files_data.append({
                    "name": file.name,
                    "content": file.read(),
                    "content_type": file.content_type
                })
            attrs['files'] = files_data
        return super().validate(attrs)


class RefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
