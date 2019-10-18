from django.views.generic import (ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView,
                                  CreateView,
                                  TemplateView)

from .models import Post, CustomUser

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import render, get_object_or_404

from django.db.models import Q


class AboutView(TemplateView):
    template_name = "blog/about.html"


class SearchView(ListView):
    model = Post
    context_object_name = 'tags'
    template_name = 'blog/search.html'

    def get_queryset(self):
        return Post.tags.all()


class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/results.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('query')
        tags = self.request.GET.getlist('tags')

        # Different options in case any of the search fields is left in blank

        if query and tags:
            object_list = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__in=tags)).distinct()
            return object_list

        elif query:
            object_list = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)).distinct()
            return object_list

        elif tags:
            object_list = Post.objects.filter(tags__name__in=tags).distinct()
            return object_list

        else:
            return Post.objects.all().distinct()


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(
            CustomUser, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
