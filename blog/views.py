from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# post views
def post_list(req):
    posts = Post.published.all()
    # Pagination
    paginator = Paginator(posts, 3)
    page_number = req.GET.get('page', 1)
    try:

        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # construction of final data object passed to page
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