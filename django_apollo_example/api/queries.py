from api.models import Post


def list_posts_resolver(obj, info):
    try:
        posts = [post.to_dict() for post in Post.get_queryset().all()]
        print(posts)
        payload = {"success": True, "posts": posts}
    except Exception as error:
        payload = {"success": False, "errors": [str(error)]}
    return payload
