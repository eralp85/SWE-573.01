from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from .forms import *
from authenticator.forms import UserEditForm, ProfileEditForm
from django.shortcuts import redirect
from django.db.models import Q, Count
from django.core.mail import send_mail
from taggit.models import Tag
from authenticator.models import Profile
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Contact
from .common.decorators import ajax_required


# from posts.common.decorators import ajax_required


# Create your views here.

@login_required
def post_list(request, tag_slug=None):

    #Getting friends of users
    friendsofUser = Contact.objects.filter(user_from=request.user).all()

    #Mapping friends of users
    friendsofUser=map(lambda x: x.user_to, friendsofUser)

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    #filtering posts
    posts = posts.filter(
        Q(author__in=friendsofUser) | Q(author=request.user)).annotate(total_comments=Count('comments')).order_by('-published_date')

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    return render(request, 'posts/post_list.html', {'posts': posts, 'tag': tag})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments

    stuff = get_object_or_404(Post, id=pk)
    total_likes = stuff.total_likes()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
        .order_by('-same_tags', '-published_date')[:10]

    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments,
                                                      'similar_posts': similar_posts, 'total_likes': total_likes})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            post.tags.add(*form.cleaned_data['tags'])

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_edit.html', {'form': form})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    # List of similar posts

    return render(request, 'posts/add_comment_to_post.html', {'form': form})


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = searched.lower()
        posts_s_ = Post.objects.filter(
            Q(title__icontains=searched) | Q(text__icontains=searched))

        # posts_s_ = Post.objects.filter(title__contains=searched | text__contains=searched)

        return render(request, 'posts/search.html', {'searched': searched, 'posts_s_': posts_s_})
    else:
        return render(request, 'posts/search.html', {})


def my_research(request):
    posts = Post.objects.filter(author_id=request.user.id).order_by('-published_date')

    most_recent_posts = Post.objects.filter(author_id=request.user.id).order_by('-published_date')[:3]

    most_commented_posts = Post.objects.filter(author_id=request.user.id).annotate(total_comments=Count('comments')).order_by('-total_comments')[:3]

    return render(request, 'posts/my_research.html', {'posts': posts, 'most_recent_posts': most_recent_posts, 'most_commented_posts': most_commented_posts})


def my_account(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'posts/my_account.html',
                  {'user_form': user_form,
                   'profile_form': profile_form}, )


def faq(request):
    return render(request, 'posts/faq.html')


def macro_economy(request):
    posts = Post.objects.filter(labels__contains='Macro')
    return render(request, 'posts/my_research.html', {'posts': posts})


def equity(request):
    posts = Post.objects.filter(labels__contains='Equity')
    return render(request, 'posts/my_research.html', {'posts': posts})


def fixed_income(request):
    posts = Post.objects.filter(labels__contains='Fixed')
    return render(request, 'posts/my_research.html', {'posts': posts})


def company_news(request):
    posts = Post.objects.filter(labels__contains='company')
    return render(request, 'posts/my_research.html', {'posts': posts})


def post_share(request, pk):
    # Retrieve post by id
    post = get_object_or_404(Post, id=pk)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{post.author} recommends you read {post.title} "

            message = f"Read {post.title} at {post_url}\n\n"

            send_mail(subject, message, 'swebogazici@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'posts/share.html', {'post': post, 'form': form, 'sent': sent})


def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'posts:my_account.html',
                  {'user_form': user_form,
                   'profile_form': profile_form},
                  'posts:my_account.html')



@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'posts/user/list.html',
                  {'section': 'people', 'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)

    all_posts = Post.objects.filter(author=user.id)
    # most_commented_posts = Post.objects.filter(author_id=request.user.id).annotate(
    #     total_comments=Count('comments')).order_by('-total_comments')[:3]
    most_commented_posts = Post.objects.filter(author_id=user.id).annotate(total_comments=Count('comments')).order_by('-total_comments')[:4]
    print(len(most_commented_posts))

    return render(request,
                  'posts/user/detail.html',
                  {'section': 'people', 'userToSee': user, 'id': user.id, 'latest_posts_db':all_posts[:4], 'count': all_posts.count(), 'most_commented_posts': most_commented_posts})


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user)

            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})

def like_post(request,pk):
    user_id = request.user.id
    post = get_object_or_404(Post , id=pk)
    if user_id:
        if post.likes.filter(id=user_id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return JsonResponse({'status': 'ok', 'likes_count': post.total_likes()})
    return JsonResponse({'status': 'error'})