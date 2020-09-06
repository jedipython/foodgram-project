from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentsForm
from django.contrib.auth.decorators import login_required
from posts.models import Post, Group, User, Comment, Follow
from django.shortcuts import redirect
import datetime
from django.core.paginator import Paginator
import random

def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    form = CommentsForm()
    return render(request, "index.html", {"page": page, "paginator": paginator, 'form': form})

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list_group = Post.objects.filter(group=group).order_by("-pub_date").all()
    paginator = Paginator(post_list_group, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "page": page, "paginator": paginator})

@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = datetime.datetime.now()
            post.group = form.cleaned_data['group']
            post.text = form.cleaned_data['text']
            post.title = form.cleaned_data['title']
            post.save()
            return redirect('/')
    else:
        form = PostForm()
    title_post = 'Новый пост'
    send_buttom = 'Отправить'
    return render(request, "new_post.html", {'form': form, 'title_post': title_post, 'send_buttom': send_buttom})

def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    subscribe = random.randint(1,27)
    sub = random.randint(1,5)
    amount_posts = Post.objects.filter(author__username=username).count()
    user_posts = Post.objects.filter(author__username=user_profile).order_by("-pub_date").all()
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    user = request.user.id
    author = User.objects.get(username=username)
    following = Follow.objects.filter(user=user, author=author.id).exists()

    return render(request, "profile.html", {'user_profile': user_profile, 'subscribe': subscribe, 'sub': sub, 'amount_posts': amount_posts, 'page':  page, 'paginator': paginator, 'following': following, })

def post_view(request, username, post_id):
    user_profile = get_object_or_404(User, username=username)
    amount_posts = Post.objects.filter(author__username=username).count()
    post = Post.objects.get(author__username=user_profile, id=post_id )
    form = CommentsForm()
    items = None
    if Comment.objects.filter(post=post_id).count():
        items = Comment.objects.filter(post=post_id)
    return render(request, "post.html", {'form': form,'user_profile': user_profile, 'amount_posts': amount_posts, 'post': post,'items': items})

@login_required
def post_edit(request, username, post_id):
    user_profile = get_object_or_404(User, username=username) 
    title_post = 'Редактирование поста' 
    post = get_object_or_404(Post, id=post_id) 
    send_buttom = 'Сохранить' 
    if request.user == user_profile and post.author == user_profile:
        if request.method == "POST": 
            form = PostForm(request.POST, files=request.FILES or None, instance=post)
            if form.is_valid():
                 post = form.save(commit=False) 
                 post.author = request.user 
                 post.group = form.cleaned_data['group'] 
                 post.text = form.cleaned_data['text'] 
                 post.save() 
                 return redirect('post', username=username, post_id=post_id) 
        else: 
             form = PostForm(instance=post) 
    else: 
        return redirect('post', username=username, post_id=post_id) 
    return render(request, "new_post.html", {'form': form,'post': post, 'title_post': title_post, 'send_buttom': send_buttom})

def page_not_found(request, exception):
        # Переменная exception содержит отладочную информацию, 
        # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)

def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) 
            comment.author = request.user
            comment.post = post
            comment.save()     
            return redirect('post', username=post.author, post_id=post_id)
        else:
            form = CommentsForm()
        
    else:
        return redirect('post', username=username, post_id=post_id)
    return render(request, "post.html", {'form': form, 'post':post})

@login_required
def follow_index(request):
        follow = Follow.objects.filter(user=request.user).all() #На кого юзер подписан
        favorits = [favorit.author.id for favorit in follow]
        posts = Post.objects.filter(author__in=favorits).order_by("-pub_date").all()
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, "follow.html", {'paginator': paginator, 'page': page})

@login_required
def profile_follow(request, username):
    if request.user.username != username:
        user = request.user.id
        author = User.objects.get(username=username)
        follower_check = Follow.objects.filter(user=user, author=author.id).count()
        if not follower_check == 1: #исправил на if not  == 1, но почему так лучше? Ведь прежний вариант аналогичен этому.Спасибо
            Follow.objects.create(author=author, user=request.user)
        return redirect('profile', username=username)
    else:
        return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
        user = request.user.id
        author = User.objects.get(username=username)
        Follow.objects.filter(author=author, user=request.user).delete()
        return redirect('profile', username=username)