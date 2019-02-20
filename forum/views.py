from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import Http404
import datetime

from django.shortcuts import(
    render,
    redirect,
)

from django.contrib.auth import (
    login as auth_login,
    authenticate,
    logout as auth_logout
)

from .forms import (
    LoginForm,
    CategoryCreationForm,
    SubcategoryCreationForm,
    ProfileForm,
    TopicCreationForm,
    CommentForm
)

from .models import (
     Category,
     SubCategory,
     Topic,
     Comment,
     Profile
)
# Create your views here.


def check_category(category):
    try:
        subcategories = Category.objects.get(name=category)
    except Category.DoesNotExist:
        raise Http404()


def check_subcategory(category, subcategory):
    try:
        subcategory = SubCategory.objects.get(name=subcategory)
        category = Category.objects.get(name=category)
    except SubCategory.DoesNotExist:
        raise Http404()
    except Category.DoesNotExist:
        raise Http404()


def check_topic(category, subcategory, topic):
    try:
        subcategory = SubCategory.objects.get(name=subcategory)
        category = Category.objects.get(name=category)
        topic = Topic.objects.get(name=topic)
    except SubCategory.DoesNotExist:
        raise Http404()
    except Category.DoesNotExist:
        raise Http404()
    except Topic.DoesNotExist:
        raise Http404()

@login_required
def profile(request):
    user_profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=user_profile, initial={'username': user_profile.user.username})

    if request.method == "POST":
        print(request.FILES, request.POST)
        form = ProfileForm(instance=user_profile, data=request.POST, files=request.FILES)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user.username = form.cleaned_data['username']
            profile.user.save()
            profile.save()

            return redirect('forum:home')

    return render(request, 'forum/profile.html', {'form': form})


@login_required
def categories(request):
    categories = Category.objects.all()

    data = {}

    for category in categories:
        data[category.name] = {'id': category.id, 'subcategories': [SubCategory.objects.filter(category=category)]}

    return render(request, 'forum/categories.html', {'data': data.items()})


@login_required
def subcategories(request, category):

    check_category(category)
    subcategories = SubCategory.objects.filter(category__name=category)

    return render(request, 'forum/sub_categories.html', {'subcategories': subcategories, 'category': category})


@login_required
def topics(request, category, subcategory):

    check_subcategory(category, subcategory)
    topics = Topic.objects.filter(subcategory__name=subcategory)

    return render(request, 'forum/topics.html', {'category': category, 'subcategory': subcategory, 'topics': topics})


@login_required
def topic(request, category, subcategory, topic):

    check_topic(category, subcategory, topic)

    form = CommentForm()
    comments = Comment.objects.all().values('profile').annotate(cc=Count('id')).values('profile__user__username', 'cc')
    print(comments)
    comments = Comment.objects.filter(topic__name=topic)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.profile = Profile.objects.get(user=request.user)
            comment.topic = Topic.objects.get(name__icontains=topic)
            comment.save()
            return redirect('forum:topic', category=category, topic=topic, subcategory=subcategory)

    return render(request, 'forum/topic_discussion.html', {'topic': topic, 'form': form, 'comments': comments})


@login_required
def create_category(request):
    form = CategoryCreationForm()

    if request.method == 'POST':
        form = CategoryCreationForm(request.POST)

        if form.is_valid():
            form.save()
            category = form.cleaned_data['name']
            return redirect('forum:subcategories', category=category)

    return render(request, 'forum/create_category.html', {'form': form})


@login_required
def create_subcategory(request, category):
    form = SubcategoryCreationForm()
    category = Category.objects.get(name=category)

    if request.method == "POST":
        form = SubcategoryCreationForm(request.POST)

        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.category = category
            subcategory.save()
            subcategory = form.cleaned_data['name']
            category = category.name
            return redirect('forum:topics', category=category, subcategory=subcategory)

    return render(request, 'forum/create_subcategory.html', {'form': form})


@login_required
def create_topic(request, category, subcategory):
    subcategory = SubCategory.objects.get(name=subcategory)
    form = TopicCreationForm()

    if request.method == 'POST':
        form = TopicCreationForm(request.POST)

        if form.is_valid():
            topic = form.save(commit=False)
            topic.subcategory = subcategory
            topic.save()
            subcategory = subcategory.name
            topic = form.cleaned_data['name']
            return redirect('forum:topic', category=category, subcategory=subcategory, topic=topic)

    return render(request, 'forum/create_topic.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('forum:home')
    form = LoginForm()

    if request.POST:
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)
                redirect_path = request.GET.get('next', 'forum:home')
                return redirect(redirect_path)

            else:

                return render(request, 'forum/login.html', {'form': form})
    else:

        return render(request, 'forum/login.html', {'form': form})


def signup(request):
    form = UserCreationForm()

    if request.user.is_authenticated:
        return redirect('forum:home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('forum:home')

    return render(request, 'forum/signup.html', {'form': form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect('forum:login')

