from rest_framework import serializers
from posts.models import Post
from tags.models import Tag
from tags.serializers import TagSerializer
import accounts.serializers as accounts_serializers
import answers.serializers as answers_serializers


class PostSerializer(serializers.ModelSerializer):
    user = accounts_serializers.AccountsSerializer(read_only=True)
    tags_count = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"

    def get_tags_count(self, post: Post):
        return len(post.tags.all())

    def create(self, validated_data):
        tags_data = validated_data.get("tags", [])

        tags = []

        for tag in tags_data:
            (tag, is_created) = Tag.objects.get_or_create(
                **tag)
            tags.append(tag)

        del validated_data["tags"]

        post = Post.objects.create(**validated_data)

        post.tags.set(tags)

        return post

    def update(self, instance, validated_data):

        tags_to_update = validated_data.pop('tags', [])

        for tag in tags_to_update:
            existing_tag = Tag.objects.filter(name=tag['name']).first()

            if existing_tag:
                instance.tags.add(existing_tag)
            else:
                new_tag = Tag.objects.create(**tag)
                instance.tags.add(new_tag)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class UsefullPostVoteSerializer(serializers.ModelSerializer):
    user = accounts_serializers.AccountsSerializer()

    class Meta:
        model = Post
        fields = "__all__"
        depth = 1

    def update(self, instance, validated_data):
        instance.usefull_post += 1

        instance.save()
        return instance


class GetPostInfoSerializer(serializers.ModelSerializer):
    user = accounts_serializers.AccountsSerializer()
    answers = answers_serializers.AnswersSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"
