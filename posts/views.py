from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm,CommentForm,ProfileForm
from django.shortcuts import redirect
from django.db.models import Q


# Create your views here.

@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'posts/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
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

            print('##########' + str(request.user.author.id))
            comment.author_id = request.user.author.id
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'posts/add_comment_to_post.html', {'form': form})

def search (request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = searched.lower()
        posts_s_ = Post.objects.filter(Q(title__icontains=searched) | Q(text__icontains=searched))

        #posts_s_ = Post.objects.filter(title__contains=searched | text__contains=searched)

        return render(request, 'posts/search.html', {'searched': searched, 'posts_s_': posts_s_})
    else:
        return render(request, 'posts/search.html', {})

def my_research(request):
    posts = Post.objects.filter(author_id=request.user.id).order_by('published_date')

    return render(request, 'posts/my_research.html', {'posts': posts})

def my_profile(request):
    author = request.user.author
    form = ProfileForm(instance=author)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,instance=author)
        if form.is_valid():
            form.save()


    context = {'form' : form}
    return render(request, 'posts/my_profile.html',context)