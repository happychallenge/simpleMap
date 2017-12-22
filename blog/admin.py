from django.contrib import admin

from .models import Theme, Post, Content, Tag, Bucket
# Register your models here.
@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    class Meta:
        model = Theme
    list_display = ['id', 'name', 'author']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Meta:
        model = Post
    list_display = [ 'id', 'theme', 'lat', 'lng', 'author']


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    class Meta:
        model = Content
    list_display = ['id', 'file', 'lat', 'lng']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    class Meta:
        model = Tag
    list_display = ['id', 'tag']


@admin.register(Bucket)
class BucketAdmin(admin.ModelAdmin):
    class Meta:
        model = Bucket
    list_display = ['user', 'post']
