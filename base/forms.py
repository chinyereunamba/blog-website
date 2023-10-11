from django import forms

from .models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        exclude = ["user", "date_created"]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post Title"}),
            "intro_text": forms.Textarea(attrs={"placeholder": "post intro"}),
            "slug": forms.TextInput(attrs={"placeholder": "slug"}),
            "tags": forms.CheckboxSelectMultiple(),
            "active": forms.CheckboxInput(),
            "featured": forms.CheckboxInput(),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["tag"]

    widgets = {"tag": forms.TextInput(attrs={"placeholder": "Tag"})}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        exclude = ["slug"]


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ["email_address"]

        widgets = {
            "email_address": forms.TextInput(attrs={"placeholder": "Email address..."})
        }


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "your name"}),
    )
    email = forms.EmailField(
        max_length=60,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "your email"}),
    )
    subject = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Subject"}),
    )
    message = forms.CharField(
        max_length=500, widget=forms.Textarea(attrs={"placeholder": "Your message"})
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "comment"]

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "email": forms.TextInput(
                attrs={"placeholder": "Your email (will not be published)"}
            ),
            "comment": forms.Textarea(attrs={"placeholder": "Your comment"}),
        }


class UserSettingForm(forms.ModelForm):
    # email = forms.EmailField(read_only=True)
    linkedin = forms.URLField(empty_value="https://")

    class Meta:
        model = Account
        fields = "__all__"
        exclude = [
            "password",
            "is_admin",
            "is_staff",
            "is_superuser",
            "is_active",
            "hide_email",
        ]
