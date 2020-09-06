from django.shortcuts import render
from .models import Post
from django.core.paginator import Paginator


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    # form = CommentsForm()
    return render(request, "indexNotAuth.html", {"page": page,
                                                 "paginator": paginator})
