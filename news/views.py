
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import PostForm
from .models import Post, Category, UserCategory
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .filters import PostFilter
from django.shortcuts import redirect


# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'post_list.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'


class PostSearch(PostList):
    template_name = 'search.html'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    initial = {'type_news': 'NE'}


class ArticleCreate(PostCreate):
    initial = {'type_news': 'AR'}


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    ordering = 'id'
    template_name = 'category_list.html'
    context_object_name = 'category_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sub = []
        for cat_user in UserCategory.objects.all().filter(user=self.request.user):
            sub.append(cat_user.category)

        context['user_subscriber'] = sub
        return context

    def subscribe_user(request, pk, **kwargs):
        UserCategory.objects.create(user=request.user, category=Category.objects.get(id=pk))
        return redirect('/category/')

    def unsubscribe_user(request, pk, **kwargs):
        cat = UserCategory.objects.get(user=request.user, category=Category.objects.get(id=pk))
        cat.delete()
        return redirect('/category/')
