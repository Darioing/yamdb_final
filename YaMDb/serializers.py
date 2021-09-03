from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор модели категорий"""

    class Meta:
        exclude = ['id']
        model = Category


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор модели жанров"""

    class Meta:
        exclude = ['id']
        model = Genre


class BaseTitlesSerializer(serializers.ModelSerializer):
    """Базовый сериализатор модели произведений"""

    class Meta:
        fields = '__all__'
        model = Title


class TitlesSerializer(BaseTitlesSerializer):
    """Сериализатор модели произведений для метода POST и PATCH"""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )


class TitlesDetailSerializer(BaseTitlesSerializer):
    """Сериализатор модели произведений для метода GET и DELETE"""

    rating = serializers.IntegerField()
    category = CategoriesSerializer()
    genre = GenresSerializer(many=True)


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date', ]
        model = Review

    def validate(self, value):
        if self.context['request'].method == 'POST':
            title_id = self.context['view'].kwargs['title_id']
            user = self.context['request'].user
            review_check = Review.objects.filter(
                title_id=title_id, author=user
            ).exists()
            if review_check:
                raise serializers.ValidationError(
                    'This user has already added review for this title'
                )
        return value


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ['id', 'text', 'author', 'pub_date', ]
        model = Comment
