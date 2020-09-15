from django.shortcuts import render
from .models import Post, Tag
from django.core.paginator import Paginator
from .forms import AddRecipeForm
from django.shortcuts import redirect
import datetime


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    # form = CommentsForm()
    return render(request, "indexNotAuth.html", {"page": page,
                                                 "paginator": paginator})


# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(
#                 request, 'Your password was successfully updated!')
#             return redirect('change_password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'registration/changePassword.html', {
#         'form': form
#     })


def add_recipe(request):
    print('Нуль') 
    if request.method == "POST":
        form = AddRecipeForm(request.POST, files=request.FILES or None)
        print(request.POST) 
        print('Первый') 
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = datetime.datetime.now()
            post.text = form.cleaned_data['text']
            post.title = form.cleaned_data['title']
            post.time = form.cleaned_data['time']
            post.slug = post.time
            post.save()
            form.save_m2m()
            print('Второй') 
            print(form.data)
            return redirect('/')
        
    else:
        form = AddRecipeForm()
        print(form.data, '!!!')
    tags = Tag.objects.all()
    return render(request, 'formRecipe.html', {'form': form, 'tags': tags})


def shop_list(request):
    return render(request, 'shopList.html',)


def favorites(request):
    return render(request, 'favorite.html',)