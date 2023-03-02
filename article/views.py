from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, \
                                  PageNotAnInteger
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector, \
                                           SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib import messages
from .utils import _checker
from markdown import markdown
from authentication.models import User
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http.response import Http404
from django.core.exceptions import ObjectDoesNotExist


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    post_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
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
                 'article/post/list.html',
                 {'posts': posts,
                  'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                            #  status=Post.Status.PUBLISHED,
                             pk=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    if request.method == "POST":
        result = _checker(request.POST)
        if result == "like":
            obj = add_likes(request, post.id)
        elif result == "dislike":
            obj = add_dislikes(request, post.id)
        elif result == "Error":
            print("Something is wrong")
        return render(request,
                  'article/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts,
                   "instance": obj})
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[:4]

    return render(request,
                  'article/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts,
                   "instance": post})


class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'article/post/list.html'


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id)
                                #    status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',
                      [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'article/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
                                #    status=Post.Status.PUBLISHED)
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
    return render(request, 'article/post/comment.html',
                           {'post': post,
                            'form': form,
                            'comment': comment})


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request,
                  'article/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})

def blog_edit(request, pk):
    if request.method == 'POST':
        try:
            post = Post.objects.get(pk=pk)
            post.title = request.POST['title']
            post.body = request.POST['body']
            post.save()
            return render(request, 'article/blog_detail.html', {"post": post})
        except ObjectDoesNotExist:
            return render(request, '404.html', {"error": ObjectDoesNotExist})
    else:
        try:
            post = Post.objects.get(pk=pk)
            return render(request, 'article/blog_edit.html', {"post": post})
        except ObjectDoesNotExist:
            return render(request, '404.html', {"error": ObjectDoesNotExist})


def blog_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        messages.success(
            request, f"{post.title} was delete successfully! by {post.author.username}")
        post.delete()
        return redirect('pages:home')
    except ObjectDoesNotExist:
        return render(request, '404.html')


def blog_add(request, username):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            title = request.POST['title']
            body = request.POST['body']
            html = markdown(body)
            print(html)
            post = Post(title=title, body=body, author=user)
            messages.success(request, f"post add successfully!")
            post.save()
            
            return redirect(post.get_absolute_url())
        except ObjectDoesNotExist:
            return render(request, '404.html', {"error": ObjectDoesNotExist})
    else:
        title = ""
        body = """
            Heading	# H1
## H2
### H3
Bold	**bold text**
Italic	*italicized text*
Blockquote	> blockquote
Ordered List	1. First item
2. Second item
3. Third item
Unordered List	- First item
- Second item
- Third item
Code	`code`
Horizontal Rule	---
Link	[title](https://www.example.com)
Image	![alt text](image.jpg)
        """
        return render(request, "article/blog_new.html",)

def user_blog(request, user_id):
    try:
        posts = get_list_or_404(Post, author=user_id)
        return render(request, 'article/blog_list.html', {"posts": posts})
    except Http404:
        messages.error(
            request, "There is no article now add it use the add new article button")
        return render(request, 'pages/home.html', {})

def add_dislikes(request, pk):
    like_obj = get_object_or_404(Post, pk=pk)
    user = request.user
    if not (str(user) == str(like_obj.author.username)):
        if user.is_authenticated:
            if user in like_obj.dislikes.all():
                like_obj.dislikes.remove(user)
                return like_obj
            else:
                like_obj.dislikes.add(user)
                return like_obj
        else:
            return redirect("auth:login")
    else:
        messages.error(request,"can't dislike your own post")
        return like_obj


def add_likes(request, pk):
    like_obj = get_object_or_404(Post, pk=pk)
    user = request.user
    if not (str(user.username) == str(like_obj.author.username)):
        if user.is_authenticated:
            if user in like_obj.likes.all():
                like_obj.likes.remove(user)
                return like_obj
            else:
                like_obj.likes.add(user)
                return like_obj
        else:
            return redirect("auth:login")
    else:
        messages.error(request,"can't like your own post")
        return like_obj
