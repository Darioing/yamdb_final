from authentication.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .custom_validators import year_validator


class Category(models.Model):
    """Модель категорий"""

    name = models.CharField(max_length=100, verbose_name='name')
    slug = models.SlugField(unique=True, verbose_name='slug')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Genre(models.Model):
    """Модель жанров"""

    name = models.CharField(max_length=100, verbose_name='name')
    slug = models.SlugField(unique=True, verbose_name='slug')

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Title(models.Model):
    """Модель произведений"""

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, related_name='titles', verbose_name='category'
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', through_fields=('title', 'genre', ),
        verbose_name='genre'
    )
    name = models.CharField(max_length=200, verbose_name='name')
    year = models.IntegerField(
        validators=[year_validator], verbose_name='year'
    )
    description = models.TextField(verbose_name='description')

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.SET_NULL, null=True,
        related_name='genres_titles',
        verbose_name='title'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True,
        related_name='genres_titles',
        verbose_name='genre'
    )

    class Meta:
        verbose_name = 'GenreTitle'
        verbose_name_plural = 'GenresTitles'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Произведение', related_name='reviews'
    )
    text = models.TextField()
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, message='The score should be at least 1'),
            MaxValueValidator(10, message='The score souldnt be more then 10')
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date', ]
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        verbose_name='Отзыв', related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date', ]
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
