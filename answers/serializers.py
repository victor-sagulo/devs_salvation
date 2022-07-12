from msilib.schema import SelfReg
from rest_framework import serializers
from answers.models import Answer
from posts.serializers import PostSerializer
from accounts.serializers import AccountsSerializer


class AnswersSerializer(serializers.ModelSerializer):
    user = AccountsSerializer()

    class Meta:
        model = Answer
        fields = ["id", "created_at", "updated_at",
                  "content", "likes", "deslikes", "user", "post_id"]
        read_only_fields = ["id", "user", "post_id"]

    def create(self, validated_data):

        answers = Answer.objects.create(**validated_data)
        return answers


class LikeAnswerVote(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.likes += 1

        instance.save()
        return instance


class DeslikeAnswerVote(serializers.ModelSerializer):
    def update(self, instance, validated_dataa):
        instance.deslike += 1

        instance.save()
        return instance


class UserAnswerSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = Answer
        fields = [
            "id",
            "created_at",
            "updated_at",
            "content",
            "likes",
            "deslikes",
            "post",
        ]
        read_only_fields = ["id", "post"]
