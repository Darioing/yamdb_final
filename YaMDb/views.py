from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets

from .custom_viewsets import BaseModelViewSet, TitleModelViewSet
from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import AdminOrReadOnly, IsAuthorOrModeratorOrAdminOrReadOnly
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, ReviewsSerializer,
                          TitlesDetailSerializer, TitlesSerializer)


class CategoriesViewSet(BaseModelViewSet):
    """ViewSet категорий"""

    permission_classes = [AdminOrReadOnly, ]
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class GenresViewSet(BaseModelViewSet):
    """ViewSet жанров"""

    permission_classes = [AdminOrReadOnly, ]
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class TitlesViewSet(TitleModelViewSet):
    """ViewSet произведений"""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = [AdminOrReadOnly, ]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitlesSerializer
        return TitlesDetailSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdminOrReadOnly
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdminOrReadOnly,
    ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
