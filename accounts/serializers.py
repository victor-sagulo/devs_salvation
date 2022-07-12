from rest_framework import serializers
from accounts.models import User
from posts.serializers import PostSerializer
from answers.serializers import UserAnswerSerializer


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}

    def validated_email(self, value):
        user_email = User.objects.filter(email__ixact=value).exists()

        if user_email:
            raise serializers.ValidationError("This email already exists")

    def create(self, validated_data):
        account = User.objects.create_user(**validated_data)
        return account


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]


class GetAccountProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)
    answers = UserAnswerSerializer(many=True)

    class Meta:
        model = User
        fields = "__all__"
