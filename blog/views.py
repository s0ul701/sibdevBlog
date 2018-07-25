from django.shortcuts import render
from blog.forms import RegisterForm, AuthForm
from django.contrib.auth import login, logout
from blog.models import Users, Posts
from django.shortcuts import redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms.utils import ErrorDict, ErrorList
from django.forms import BaseForm


def register(request):
    if request.user.is_authenticated:
        return redirect('profile', username=request.user.username)

    context = {"form": RegisterForm()}
    if request.POST:        # TODO: обработки ошибок!!!
        registration_form = RegisterForm(request.POST)
        if registration_form.is_valid() and request.POST['password'] == request.POST['password_repeat']:
            new_user = registration_form.save(commit=False)
            new_user.password = request.POST['password']
            new_user.username = request.POST['username']
            new_user.save()
            login(request, new_user)
            return redirect('profile', username=new_user.username)
        else:
            errors = []
            for error in registration_form.errors.as_data():
                text_error = registration_form.errors.as_data()[error][0].messages[0]
                errors.append(text_error)

            if request.POST['password'] != request.POST['password_repeat']:
                errors.append("Password mismatch.")
            # registration_form = RegisterForm()
            registration_form.set_errors = errors
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
            return redirect('profile', username=user.username)
        else:
            auth_form = AuthForm()
            auth_form.errors['auth_error'] = True
            context['form'] = auth_form
    return render(request, "auth.html", context=context)


def profile(request, username):
    context = {}
    context['user'] = request.user

    return render(request, "profile.html", context=context)


def deauth(request):
    logout(request)
    return redirect('auth')


def index(request):
    context = {'user': request.user,
               # 'posts': Posts.objects.all().order_by('-published_date'),
               }
    paginator = Paginator(Posts.objects.all().order_by('-published_date'), 10)
    page = request.GET.get('page')
    try:
        context['posts'] = paginator.page(page)
    except PageNotAnInteger:
        context['posts'] = paginator.page(1)
    except EmptyPage:
        context['posts'] = paginator.page(paginator.num_pages)

    return render(request, "index.html", context=context)


def post(request, post_id):
    post = Posts.objects.get(pk=post_id)
    context = {'post': post}
    a = 0
    return render(request, 'post.html', context=context)
