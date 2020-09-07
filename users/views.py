from django.http import HttpResponse
from django.views.generic import CreateView
from django.core.mail import send_mail
from .forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(
#                 username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = "/auth/login/"
    template_name = "registration/signup.html"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        send_mail_ls(email)
        return super().form_valid(form)


def send_mail_ls(email):
    send_mail('Подтверждение регистрации Продуктовый помощник', 'Вы зарегистрированы!',
              'ProProduct.ru <admin@proproduct.ru>', [email], fail_silently=False)
