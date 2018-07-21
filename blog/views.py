from django.shortcuts import render
from blog.forms import RegisterForm, AuthForm
from django.contrib.auth import login
from blog.models import Users
from django.shortcuts import redirect

# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return redirect('profile', username=request.user.username)
    context = {"form": RegisterForm()}
    if request.POST:        # TODO: обработки ошибок!!!
        registration_form = RegisterForm(request.POST)
        if registration_form.is_valid() and request.POST['password'] == request.POST['password_repeat']:
            new_user = registration_form.save(commit=False)
            new_user.save()
            login(request, new_user)
            return redirect('profile', username=new_user.username)
        else:
            context['form'] = registration_form
    return render(request, "register.html", context=context)


def auth(request):
    if request.user.is_authenticated:
        return redirect('profile', username=request.user.username)
    context = {"form": AuthForm()}
    if request.POST:
        auth_form = AuthForm(request.POST)
        user = Users.objects.filter(username=request.POST['username'], password=request.POST['password'])
        if user:
            user = user.get()
            login(request, user)
            return render(request, 'profile.html')
        else:
            context['form'] = auth_form
    return render(request, "auth.html", context=context)


def profile(request, username):
    context = {}
    a = request.user


    return render(request, "profile.html", context=context)