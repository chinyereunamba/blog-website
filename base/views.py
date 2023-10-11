from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate, logout

from .models import *
from .forms import *

# Create your views here.


def home(request):
    post = Post.objects.filter(featured=True)[0:3]

    if not post:
        post = Post.objects.all()[0:3]

    category = Category.objects.all()
    tags = Tag.objects.all()
    recent_post = Post.objects.order_by("-date_created")[0:4]
    newsletter = NewsletterForm()

    if request.method == "POST":
        newsletter = NewsletterForm(request.POST)
        if newsletter.is_valid():
            newsletter.save()
            return redirect("home")

    context = {
         "posts": post,
        "category": category,
        "tags": tags,
        "recent_post": recent_post,
        "newsletter": newsletter,
    }
    return render(request, "base/index.html", context)


def custom_404(request, exception):
    return render(request, "base/404.html", status=404)

def custom_500(request, exception):
    return render(request, "base/500.html", status=500)


def loginView(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

    context = {}

    return render(request, "base/login.html", context)


def logoutView(request):
    logout(request)
    return redirect("home")


@login_required(login_url="/login")
def userSettings(request):
    user = Account.objects.get(email=request.user.email)
    form = UserSettingForm(instance=user)

    if request.method == "POST":
        form = UserSettingForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}

    return render(request, "base/create.html", context)


@login_required(login_url="/login")
def createPost(request):
    user = Post.objects.create(user=request.user)
    form = PostForm(instance=user)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("posts")

    context = {"form": form}

    return render(request, "base/post_form.html", context)


@login_required(login_url="/login")
def updatePost(request, slug):
    model = Post.objects.get(slug=slug)
    form = PostForm(instance=model)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=model)
        if form.is_valid():
            form.save()

        return redirect("post", slug=model.slug)

    context = {"form": form}

    return render(request, "base/post_form.html", context)


@login_required(login_url="/login")
def deletePost(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == "POST":
        post.delete()
        return redirect("posts")

    context = {"item": post}

    return render(request, "base/delete.html", context)


def viewPost(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comment = Comment.objects.filter(post__in=[post])
    commentCount = comment.count()
    form = CommentForm()
    newsletter = NewsletterForm()

    if request.method == "POST":
        newsletter = NewsletterForm(request.POST)
        comments = Comment(post=post)
        form = CommentForm(request.POST, instance=comments)

        if form.is_valid():
            form.save()
        return redirect("post", slug=post.slug)

        if newsletter.is_valid():
            newsletter.save()
            return redirect("post", slug=post.slug)

    context = {
        "post": post,
        "form": form,
        "comments": comment,
        "commentCount": commentCount,
        "newsletter": newsletter,
    }

    return render(request, "base/post.html", context)


def posts(request):
    posts = Post.objects.filter(active=True)
    category = Category.objects.all()
    tags = Tag.objects.all()
    recent_post = Post.objects.order_by("-date_created")[0:4]
    query = request.GET.get("search")
    newsletter = NewsletterForm()
    if request.method == "POST":
        newsletter = NewsletterForm(request.POST)
        if newsletter.is_valid():
            newsletter.save()

            return redirect("posts")

    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(intro_text__icontains=query)
            | Q(body__icontains=query)
        )

    page = request.GET.get("page")

    paginator = Paginator(posts, 6)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "posts": posts,
        "category": category,
        "tags": tags,
        "recent_post": recent_post,
        "newsletter": newsletter,
    }

    return render(request, "base/posts.html", context)


def categoryList(request, slug):
    category = Category.objects.get(slug=slug)
    posts = Post.objects.filter(category__in=[category])
    postCount = posts.count()
    category = Category.objects.all()
    tags = Tag.objects.all()
    recent_post = Post.objects.order_by("-date_created")[0:4]
    newsletter = NewsletterForm()
    if request.method == "POST":
        newsletter = NewsletterForm(request.POST)
        if newsletter.is_valid():
            newsletter.save()
            return redirect("category", slug=slug)

    context = {
        "posts": posts,
        "category": category,
        "tags": tags,
        "recent_post": recent_post,
        "newsletter": newsletter,
        "postCount": postCount,
    }

    return render(request, "base/categoryList.html", context)


def category(request):
    category = Category.objects.all()

    recent_post = Post.objects.order_by("-date_created")[0:4]
    tags = Tag.objects.all()
    newsletter = NewsletterForm()
    if request.method == "POST":
        newsletter = NewsletterForm(request.POST)
        if newsletter.is_valid():
            newsletter.save()
        return redirect("category")

    context = {
        "category": category,
        "recent_post": recent_post,
        "tags": tags,
        "newsletter": newsletter,
    }

    return render(request, "base/category.html", context)


def tags(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)

    category = Category.objects.all()
    tags = Tag.objects.all()
    recent_post = Post.objects.order_by("-date_created")[0:4]
    newsletter = NewsletterForm()
    if request.method == "POST":
        newsletter = NewsletterForm(request.POST)
        if newsletter.is_valid():
            newsletter.save()
            return redirect("category", slug=slug)

    context = {
        "posts": posts,
        "category": category,
        "tags": tags,
        "tag": tag,
        "recent_post": recent_post,
        "newsletter": newsletter,
    }

    return render(request, "base/tagList.html", context)


def contact(request):
    form = ContactForm()
    newsletter = NewsletterForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        name = request.POST.get("name")
        sender_email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        newsletter = NewsletterForm(request.POST)
        if newsletter.is_valid():
            newsletter.save()
            return redirect("contact")
        if form.is_valid():
            print(f"{name} {sender_email} {subject} {message}")
            return redirect("home")

    context = {
        "form": form,
        "newsletter": newsletter,
    }

    return render(request, "base/contact.html", context)


class CreateTag(SuccessMessageMixin, CreateView, LoginRequiredMixin):
    model = Tag
    form_class = TagForm
    template_name = "base/create.html"
    success_message = "Item %(tag)s created successfully"


class CreateCategory(SuccessMessageMixin, CreateView, LoginRequiredMixin):
    model = Category
    form_class = CategoryForm
    template_name = "base/create.html"
    success_message = "Item %(category)s created successfully"
    success_url = "/category/"


def about(request):
    newsletter = NewsletterForm()
    if request.method == "POST":
        newsletter = NewsletterForm(request.POST)
        if newsletter.is_valid():
            newsletter.save()

            return redirect("about")
    context = {"newsletter": newsletter}
    return render(request, "base/about.html", context)


def thanks(request):
    return render(request, "base/thanks.html")
