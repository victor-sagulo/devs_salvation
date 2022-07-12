from rest_framework import serializers
from posts.models import Post
from tags.models import Tag
from tags.serializers import TagSerializer


class PostSerializer(serializers.ModelSerializer):

    tags_count = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True}
        }

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
