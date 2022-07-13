from rest_framework import serializers
from answers.models import Answer
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}


class AnswersSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Answer
        fields = ["id", "created_at", "updated_at",
                  "content", "likes", "deslikes", "user", "post_id"]
        read_only_fields = ["id", "user", "post_id"]

    def create(self, validated_data):

        answers = Answer.objects.create(**validated_data)
        return answers


class LikeAnswerVote(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Answer
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.likes += 1

        instance.save()
        return instance


class DeslikeAnswerVote(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Answer
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.deslike += 1

        instance.save()
        return instance


class UserAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = [
            "id",
            "created_at",
            "updated_at",
            "content",
            "likes",
            "deslikes",
            "post_id",
        ]
