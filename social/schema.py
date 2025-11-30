import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Post, Comment, Like
from core.schema import UserType

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"
        filter_fields = {
            'content': ['icontains'],
            'author__username': ['exact'],
            'created_at': ['gte', 'lte'],
        }
        interfaces = (graphene.relay.Node, )

    like_count = graphene.Int()
    comment_count = graphene.Int()

    def resolve_like_count(self, info):
        return self.likes.count()

    def resolve_comment_count(self, info):
        return self.comments.count()

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = "__all__"
        interfaces = (graphene.relay.Node, )

class LikeType(DjangoObjectType):
    class Meta:
        model = Like
        fields = "__all__"
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    post = graphene.relay.Node.Field(PostType)
    all_posts = DjangoFilterConnectionField(PostType)

    def resolve_all_posts(self, info, **kwargs):

        return Post.objects.select_related('author').prefetch_related('comments', 'likes').order_by('-created_at')

class CreatePost(graphene.Mutation):
    class Arguments:
        content = graphene.String(required=True)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, content):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        

        from django.utils import timezone
        from datetime import timedelta
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_posts = Post.objects.filter(author=user, created_at__gte=one_minute_ago).count()
        if recent_posts >= 5:
            raise Exception("Rate limit exceeded: You can only create 5 posts per minute.")

        post = Post(content=content, author=user)
        post.save()
        return CreatePost(post=post)

class CreateComment(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
        text = graphene.String(required=True)

    comment = graphene.Field(CommentType)

    @classmethod
    def mutate(cls, root, info, post_id, text):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")


        from graphql_relay import from_global_id
        _, p_id = from_global_id(post_id)

        try:
            post = Post.objects.get(pk=p_id)
        except Post.DoesNotExist:
            raise Exception("Post not found")

        comment = Comment(user=user, post=post, text=text)
        comment.save()
        

        from .tasks import send_comment_notification
        if post.author.email:
             send_comment_notification.delay(post.author.email, post.id, text)

        return CreateComment(comment=comment)

class LikePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)

    like = graphene.Field(LikeType)

    @classmethod
    def mutate(cls, root, info, post_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")

        from graphql_relay import from_global_id
        _, p_id = from_global_id(post_id)

        try:
            post = Post.objects.get(pk=p_id)
        except Post.DoesNotExist:
            raise Exception("Post not found")

        if Like.objects.filter(user=user, post=post).exists():
             raise Exception("Already liked")

        like = Like(user=user, post=post)
        like.save()
        return LikePost(like=like)

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    create_comment = CreateComment.Field()
    like_post = LikePost.Field()
