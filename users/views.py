from django.views.generic import CreateView
from django.core.mail import send_mail
from .forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = "/auth/login/"
    template_name = "registration/signup.html"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        send_mail_ls(email)
        return super().form_valid(form)


def send_mail_ls(email):
    send_mail('Подтверждение регистрации Продуктовый помощник',
              'Вы зарегистрированы!',
              'ProProduct.ru <admin@proproduct.ru>', [email],
              fail_silently=False)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/changePassword.html', {
        'form': form
    })


def subscribes(request):
    return render(request, "myFollow.html")
