from rest_framework import serializers
from accounts.models import User
from posts.models import Post
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
    answers_count = serializers.SerializerMethodField()
    usefull_post = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "content", "tags", "answers_count", "usefull_post",
                  "created_at", "updated_at"]
        depth = 1

    def get_usefull_post(self, post: Post):
        return len(post.usefull_post.all())

    def get_answers_count(self, post: Post):
        return len(post.answers.all())


class GetAccountProfileSerializer(serializers.ModelSerializer):
    posts = UserPostsSerializer(many=True)
    answers = answer_serializer.UserAnswerSerializer(many=True)

    class Meta:
        model = User
        fields = ["id", "username", "email",
                  "first_name", "last_name", "posts", "answers"]
