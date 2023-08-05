#!/usr/bin/env python
# encoding: utf-8
import time
import graphene

from graphene import resolve_only_args
from graphql.core.type import GraphQLEnumValue

from .fixtures import AuthorsMap, CommentList, PostsList, ReplyList
from ..utils import get_time

Category = graphene.Enum('Category',
                         {
                             'METEOR': GraphQLEnumValue("meteor"),
                             'PRODUCT': GraphQLEnumValue("product"),
                             'USER_STORY': GraphQLEnumValue("user-story"),
                             'OTHER': GraphQLEnumValue("other")
                         })


class Author(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    twitter = graphene.String()


class HasAuthor(graphene.Interface):
    author = graphene.Field(Author)

    def resolve_author(self, args, info):
        return Author(**AuthorsMap[self.author])


class Comment(HasAuthor):
    id = graphene.String()
    content = graphene.String()
    replies = graphene.List('Comment')


    def resolve_replies(self, args, info):
        return [Comment(**r) for r in ReplyList]


class Post(HasAuthor):
    id = graphene.String()
    title = graphene.String()
    category = graphene.Field(Category)
    summary = graphene.String()
    content = graphene.String()
    timestamp = graphene.Float()
    comments = graphene.List(Comment, count=graphene.Int())

    def resolve_timestamp(self, args, info):
        result = get_time(self.timestamp)
        return result

    @resolve_only_args
    def resolve_comments(self, count):
        if count > 0:
            results = CommentList[:count]
        else:
            results = CommentList
        comments = []
        for r in results:
            comments.append(Comment(**r))
        return comments


def format_post(post):
    return Post(id=post["id"],
                title=post["title"],
                category=post["category"],
                summary=post["summary"],
                content=post["content"],
                timestamp=post["date"],
                author=post["author"]
                )


class Query(graphene.ObjectType):
    posts = graphene.List(Post, category=graphene.Argument(Category))
    latestPost = graphene.Field(Post)
    recentPosts = graphene.List(Post, count=graphene.Int())
    post = graphene.Field(Post, id=graphene.String())
    authors = graphene.List(Author)
    author = graphene.Field(Author, id=graphene.String())

    @resolve_only_args
    def resolve_posts(self, category):
        return [format_post(post) for post in PostsList if post['category'] == category]

    def resolve_latestPost(self, args, info):
        post = PostsList[0]
        return format_post(post)

    @resolve_only_args
    def resolve_recentPosts(self, count):
        posts = PostsList[:count]
        return [format_post(p) for p in posts]

    @resolve_only_args
    def resolve_post(self, id):
        for post in PostsList:
            if post["id"] == id:
                return format_post(post)

    def resolve_authors(self, args, info):
        results = []
        for au in AuthorsMap.values():
            results.append(Author(**au))
        return results

    @resolve_only_args
    def resolve_author(self, id):
        return Author(**AuthorsMap[id])


class CreatePost(graphene.Mutation):
    class Input:
        id = graphene.String().NonNull
        title = graphene.String().NonNull
        content = graphene.String().NonNull
        author = graphene.String().NonNull
        summary = graphene.String()
        category = graphene.Argument(Category)

    ok = graphene.Boolean()
    post = graphene.Field('Post')

    @classmethod
    def mutate(cls, instance, args, info):
        if len(filter(lambda m: m['id'] == args.get('id'), PostsList)):
            raise Exception("Post already exists: %s" % args.get('id'))
        if not AuthorsMap.get(args.get('author')):
            raise Exception("No such author: %s" % args.get('author'))
        post = Post(
            id=args.get('id'),
            title=args.get('title'),
            content=args.get('content'),
            summary=args.get('summary'),
            category=args.get('category'),
            author=args.get('author')
        )
        post.comments = []
        post.timestamp = time.time()
        ok = True
        return CreatePost(post=post, ok=ok)


class MyMutations(graphene.ObjectType):
    create_post = graphene.Field(CreatePost)


blog_schema = graphene.Schema(query=Query, mutation=MyMutations)


