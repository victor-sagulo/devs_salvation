from rest_framework import serializers
from answers.models import Answer
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name"]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}


class AnswersSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "created_at", "updated_at",
                  "content", "likes", "dislikes", "user", "post_id"]
        read_only_fields = ["id", "likes", "dislikes", "post_id"]

    def create(self, validated_data):
        post = validated_data.pop("posts")
        print(post)
        answers = Answer.objects.create(**validated_data)
        return answers

    def update(self, instance, validated_data):
        non_editable_key = ["likes", "dislikes"]

        for key, value in validated_data.items():
            if key in non_editable_key:
                raise serializers.ValidationError(
                    {f'{key}': f"You cannot update {key} key"})
            setattr(instance, key, value)

        instance.save()
        return instance


class LikeAnswerVote(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Answer
        fields = "__all__"

    def update(self, instance, validated_data):
        user = validated_data.get("data")

        if(user in instance.likes.all()):
            instance.likes.remove(user)
        else:
            instance.likes.add(user)

        instance.save()
        return instance


class DislikeAnswerVote(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Answer
        fields = "__all__"

    def update(self, instance, validated_data):
        user = validated_data.get("data")

        if(user in instance.dislikes.all()):
            instance.dislikes.remove(user)
        else:
            instance.dislikes.add(user)

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
            "dislikes",
            "post_id",
        ]
