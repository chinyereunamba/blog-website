from django.db import models

from django.urls import reverse

from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.conf import settings

import PIL
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email), username=username, password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user

    def get_profile_image_filepath(self):
        return f'user_profile_img/{self.username}/{"profile_pic.png"}'

    def get_default_profile_image():
        return "profile-img/profile_pic.png"


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)

    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=60, blank=True, null=True)

    date_joined = models.DateTimeField(verbose_name="date_joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last_login", auto_now=True)

    bio = models.TextField(max_length=300, blank=True, null=True)
    profile_image = models.ImageField(
        default="profile-img/profile_pic.png",
        max_length=255,
        null=True,
        blank=True,
        upload_to="profile-img/",
    )

    linkedin = models.URLField(verbose_name='LinkedIn URL', max_length=250, blank=True)
    github = models.URLField(verbose_name='GitHub URL', max_length=250, blank=True)
    twitter = models.URLField(verbose_name='Twitter URL', max_length=250, blank=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    hide_email = models.BooleanField(default=True)

    objects = MyAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[
            str(self.profile_image).index(f"profile_img/{self.username}/")
        ]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Category(models.Model):
    category = models.CharField(max_length=200, blank=False, null=False, unique=True)
    slug = models.SlugField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category"]
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse("category")

    def save(self, *args, **kwargs):
        if self.slug == None:
            slug = slugify(self.category)

            has_slug = Category.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.category) + "-" + str(count)
                has_slug = Category.objects.filter(slug=slug).exists()

            self.slug = slug

        super().save(*args, **kwargs)


class Tag(models.Model):
    tag = models.CharField(max_length=20, blank=False, null=False, unique=True)
    slug = models.SlugField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag

    def save(self, *args, **kwargs):
        if self.slug == None:
            slug = slugify(self.tag)

            has_slug = Tag.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.tag) + "-" + str(count)
                has_slug = Tag.objects.filter(slug=slug).exists()

            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("posts")


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, blank=False, null=False)
    intro_text = models.TextField(null=False, blank=False, max_length=300)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )
    post_image = models.ImageField(default="img-3.jpg", blank=True, null=True, upload_to='post/')
    body = RichTextUploadingField(blank=True, null=True)
    read_time = models.IntegerField(default=5)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == None:
            slug = slugify(self.title)

            has_slug = Post.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.title) + "-" + str(count)
                has_slug = Post.objects.filter(slug=slug).exists()

            self.slug = slug

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["title"]


class Comment(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=60, blank=False, null=False)
    comment = models.TextField(blank=False, null=False)
    profile_image = models.ImageField(default="/profile-img/profile_pic.png")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"A new comment on {self.post}"


class Newsletter(models.Model):
    email_address = models.EmailField(blank=False, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Newsletter Email"

    def __str__(self):
        return self.email_address
