from project import settings
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count


# post views
def post_list(req, tag_slug=None):
    posts = Post.published.all()
    tag = None

    if tag_slug: 
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
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
    data = {
        'posts' : posts,
        'tag' : tag
        }
    return render(req, 'blog/post/list.html', data)


def post_detail(req, year, month, day, post):
    post = get_object_or_404(Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month = month,
        publish__day=day)
    
    comments = post.comments.filter(active=True)
    form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]


    data = {
        'post' : post,
        'comments' : comments,
        'form' : form,
        'similar_posts' : similar_posts
        }
    return render(req, 'blog/post/detail.html', data)

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(req, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if req.method == 'POST':
        form = EmailPostForm(req.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = req.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read"\
                        f"{post.title}"
            message = f"Read {post.title} at {post_url} \n\n"\
                f"{cd['name']}\'s comments: {cd['comments']}"

            print(settings.EMAIL_HOST_PASSWORD, settings.EMAIL_HOST_USER)
            send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[cd['to']], auth_password=settings.EMAIL_HOST_PASSWORD)
            sent=True

    else:
        form = EmailPostForm()
    
    data = {
        'post' : post,
        'form' : form,
        'sent' : sent
    }

    return render(req, 'blog/post/share.html', data)

@require_POST
def post_comment(req, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=req.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    data = {
        'post' : post,
        'form' : form,
        'comment' : comment
    }

    return render(req, 'blog/post/comment.html', data)