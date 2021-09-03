from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    list_display = ('description', 'year', 'name', 'category', )
    search_fields = ('name', )
    list_filter = ('year', )
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('text', 'pub_date', 'author', 'score')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'text', 'pub_date')
    search_fields = ('text', )
    list_filter = ('text', )
    empty_value_display = '-пусто-'
