from django.forms import TextInput, Select, DateInput
from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter
from .models import Post, Author, Category


class PostFilter(FilterSet):
    # type_news = ChoiceFilter(
    #     label='Тип публикации',
    #     choices=TYPES,
    #     empty_label='любой',
    #     widget=Select(attrs={'class': 'form-control'})
    # )

    categories = ModelChoiceFilter(
        label='Категория',
        empty_label='без категории',
        queryset=Category.objects.all(),
        widget=Select(attrs={'class': 'form-control'})
    )

    date_time = DateFilter(
        lookup_expr='date__gte',
        widget=DateInput(attrs={'type': 'date'}),
        label='позже указываемой даты'
    )

    title = CharFilter(
        lookup_expr='icontains',
        label='Название публикации',
        widget=TextInput(
            attrs={'type': 'text',
                   'class': 'form-control',
                   'placeholder': 'Название содержит...',
                   }
        )
    )

    author = ModelChoiceFilter(
        label='Автор',
        empty_label='Все авторы',
        queryset=Author.objects.all(),
        widget=Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'date_time',
            'categories',
            # 'type_news'
        ]