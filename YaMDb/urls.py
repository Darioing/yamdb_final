from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CommentsViewSet, GenresViewSet,
                    ReviewsViewSet, TitlesViewSet)

v1_router = DefaultRouter()
v1_router.register('categories', CategoriesViewSet, 'Categories')
v1_router.register('genres', GenresViewSet, 'Genres')
v1_router.register('titles', TitlesViewSet, 'Titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet, basename='Reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentsViewSet, basename='Comments'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
