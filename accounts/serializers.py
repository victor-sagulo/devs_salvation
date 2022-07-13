from rest_framework import serializers
from accounts.models import User
from posts.models import Post
# from posts.serializers import UserPostsSerializer
import answers.serializers as answer_serializer


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email",
                  "first_name", "last_name", "password"]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}

    def validated_email(self, value):
        user_email = User.objects.filter(email__ixact=value).exists()

        if user_email:
            raise serializers.ValidationError("This email already exists")

    def create(self, validated_data):
        account = User.objects.create_user(**validated_data)
        return account


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserPostsSerializer(serializers.ModelSerializer):
    # answers = answers_serializers.AnswersSerializer(many=True)
    # tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"
        depth = 1


class GetAccountProfileSerializer(serializers.ModelSerializer):
    posts = UserPostsSerializer(many=True)
    answers = answer_serializer.UserAnswerSerializer(many=True)

    class Meta:
        model = User
        fields = ["id", "username", "email",
                  "first_name", "last_name", "posts", "answers"]
