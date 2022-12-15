from django.shortcuts import render, get_object_or_404
from .models import Post

# post views
def post_list(req):
    posts = Post.published.all()
    print(posts)
    data = {'posts' : posts}
    return render(req, 'blog/post/list.html', data)


def post_detail(req, year, month, day, post):
    post = get_object_or_404(Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month = month,
        publish__day=day)

    data = {'post' : post}
    return render(req, 'blog/post/detail.html', data)