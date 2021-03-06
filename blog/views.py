from django.shortcuts import render
from blog.forms import RegisterForm, AuthForm, PostForm, ProfileEditForm
from django.contrib.auth import login, logout, hashers
from blog.models import Users, Posts, BlockedIP
from django.shortcuts import redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

salt = '1234567'    # соль для хэширования паролей


def register(request):
    if request.user.is_authenticated:
        return redirect('profile', username=request.user.username)

    context = {"form": RegisterForm()}
    if request.POST:
        registration_form = RegisterForm(request.POST)
        if registration_form.is_valid() and request.POST['password'] == request.POST['password_repeat']:
            new_user = registration_form.save(commit=False)
            # new_user.password = request.POST['password']
            # new_user.set_password(request.POST['password'])
            new_user.password = hashers.make_password(request.POST['password'], salt=salt)
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
            registration_form.set_errors = errors
            context['form'] = registration_form
    return render(request, "register.html", context=context)


def auth(request):
    if request.user.is_authenticated:
        return redirect('profile', username=request.user.username)

    if request.POST:
        if BlockedIP.objects.filter(ip=request.META['REMOTE_ADDR']) and BlockedIP.objects.get(ip=request.META['REMOTE_ADDR']).is_blocked:
            if not AuthForm(request.POST).is_valid():
                auth_form = AuthForm()
                auth_form.is_need_captcha = True
                auth_form.error_captcha = True

                context = {'form': auth_form}
                return render(request, "auth.html", context=context)

        user = Users.objects.filter(username=request.POST['username'], password=hashers.make_password(request.POST['password'], salt=salt))
        if user:
            if BlockedIP.objects.filter(ip=request.META['REMOTE_ADDR']):
                BlockedIP.objects.get(ip=request.META['REMOTE_ADDR']).delete()
            user = user.get()
            login(request, user)
            return redirect('profile', username=user.username)
        else:
            auth_form = AuthForm()
            auth_form.errors['auth_error'] = True

            if BlockedIP.objects.filter(ip=request.META['REMOTE_ADDR']):
                blocked_ip = BlockedIP.objects.get(ip=request.META['REMOTE_ADDR'])
                blocked_ip.attempts = blocked_ip.attempts + 1
                blocked_ip.save(update_fields=['attempts'])
            else:
                blocked_ip = BlockedIP(ip=request.META['REMOTE_ADDR'], is_blocked=False, attempts=1)
                blocked_ip.save()

            if BlockedIP.objects.get(ip=request.META['REMOTE_ADDR']).attempts >= 5:
                auth_form.is_need_captcha = True
                blocked_ip.is_blocked = True
                blocked_ip.save(update_fields=['is_blocked'])

            context = {'form': auth_form}
            return render(request, "auth.html", context=context)
    else:
        auth_form = AuthForm()
        auth_form.is_need_captcha = False
        if BlockedIP.objects.filter(ip=request.META['REMOTE_ADDR']):
            if BlockedIP.objects.get(ip=request.META['REMOTE_ADDR']).is_blocked:
                auth_form.is_need_captcha = True
        context = {'form': auth_form}
        return render(request, "auth.html", context=context)


def deauth(request):
    logout(request)
    return redirect('auth')


def profile(request, username):     # TODO: настроить страницу профиля
    context = {}
    context['user'] = request.user
    context['username'] = username
    user = Users.objects.get(username=username)
    context['posts'] = Posts.objects.filter(author_id=user.id).order_by('-published_date')
    paginator = Paginator(Posts.objects.filter(author_id=user.id).order_by('-published_date'), 5)
    page = request.GET.get('page')
    try:
        context['posts'] = paginator.page(page)
    except PageNotAnInteger:
        context['posts'] = paginator.page(1)
    except EmptyPage:
        context['posts'] = paginator.page(paginator.num_pages)

    return render(request, "profile.html", context=context)


def index(request):
    context = {'user': request.user}
    paginator = Paginator(Posts.objects.all().order_by('-published_date'), 5)
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
    return render(request, 'post.html', context=context)


def edit(request, post_id):
    if request.user == Posts.objects.get(pk=post_id).author:
        if request.POST:
            form = PostForm(request.POST)
            post = Posts.objects.get(pk=post_id)
            post.title = request.POST['title']
            post.text = request.POST['text']
            post.pretext = request.POST['pretext']
            post.save(update_fields=['title', 'text', 'pretext'])
            return redirect('profile', request.user.username)
        else:
            form = PostForm(initial={
                'title': Posts.objects.get(pk=post_id).title,
                'pretext': Posts.objects.get(pk=post_id).pretext,
                'text': Posts.objects.get(pk=post_id).text,
            })
            context = {'form': form, 'user': request.user, 'post_id': post_id}
            return render(request, 'edit.html', context=context)
    else:
        return redirect('index')


def create(request):
    if request.user.is_authenticated:
        if request.POST:
            form = PostForm(request.POST)
            post = Posts()
            post.title = request.POST['title']
            post.pretext = request.POST['pretext']
            post.text = request.POST['text']
            post.author = request.user
            post.save()
            return redirect('profile', request.user.username)
        else:
            form = PostForm()
            context = {'form': form, 'user': request.user}
            return render(request, 'create.html', context=context)
    else:
        return redirect('index')


def edit_profile(request):
    if request.user.is_authenticated:
        errors = []
        successes = []
        if request.POST:
            if request.POST['first_name'] and request.POST['first_name'] != request.user.first_name:
                request.user.first_name = request.POST['first_name']
                successes.append('First name successfully changed.')
                request.user.save(update_fields=['first_name'])

            if request.POST['last_name'] and request.POST['last_name'] != request.user.last_name:
                request.user.last_name = request.POST['last_name']
                successes.append('Last name successfully changed.')
                request.user.save(update_fields=['last_name'])

            if request.POST['email'] != request.user.email:
                if not Users.objects.filter(email=request.POST['email']):
                    request.user.email = request.POST['email']
                    successes.append('E-mail successfully changed.')
                    request.user.save(update_fields=['email'])
                else:
                    errors.append('User with this e-mail already exists.')

            if request.POST['current_password']:
                if hashers.make_password(request.POST['current_password'], salt=salt) == request.user.password:
                    if request.POST['new_password'] == request.POST['new_password_repeat']:
                        successes.append('Password successfully changed.')
                        request.user.password = request.POST['new_password']
                        request.user.save(update_fields=['password'])
                    else:
                        errors.append('Password mismatch.')

                else:

                    errors.append('Wrong current password.')

            form = ProfileEditForm(initial={
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            })
            form.set_errors = errors
            form.set_successes = successes
            context = {'form': form, 'user': request.user}
            return render(request, 'edit_profile.html', context=context)
        else:
            form = ProfileEditForm(initial={
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            })
            context = {'form': form, 'user': request.user}
            return render(request, 'edit_profile.html', context=context)
    else:
        return redirect('index')
