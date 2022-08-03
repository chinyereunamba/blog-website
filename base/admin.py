from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

from .models import *
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined',
                    'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'date_created']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['email', 'post', 'date_created']
    search_fields = ['user', 'post']


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'active', 'date_created']
    list_filter = ['active', 'featured']
    search_fields = ['title']


admin.site.register(Account, AccountAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Newsletter)
