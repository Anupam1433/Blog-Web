from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage,\
    PageNotAnInteger
from .forms import CommentForm
from django.views.decorators.http import require_POST

# Create your views here.


def post_list(request):
    posts = Post.published.all()

    # Pagination with 3 posts per page
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
     # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
     # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post found.")

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()     
                        
    return render(request,
                  'blog/post/detail.html',
                  {'post': post, 'comments': comments,
                   'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
    # Assign the post to the comment
        comment.post = post
    # Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})
