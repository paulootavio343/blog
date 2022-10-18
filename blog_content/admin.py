from .models import Comentaries
from .models import Category
from django.contrib import admin
from .models import Posts
from django_summernote.admin import SummernoteModelAdmin


class PostsAdmin(SummernoteModelAdmin):
    list_display = ('id', 'title', 'user', 'update_date',
                    'publication_date', 'post_category', 'published',)
    list_editable = ('published',)
    list_display_links = ('id', 'title',)
    summernote_fields = ('content', )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')


class ComentariesAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'title', 'message',
                    'created', 'updated', 'published')
    list_editable = ('published',)
    list_display_links = ('id', 'email', 'title')


admin.site.register(Posts, PostsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comentaries, ComentariesAdmin)
