from django.shortcuts import render
from .models import Post
from django.core.paginator import Paginator
from .forms import AddRecipeForm


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
    # if request.method == 'POST':
    #     form = AddRecipeForm()
    # return render(request, 'formRecipe.html', {'form': form})
    return render(request, 'formRecipe.html',)


def shop_list(request):
    return render(request, 'shopList.html',)


def favorites(request):
    return render(request, 'favorite.html',)