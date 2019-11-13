from django.views.generic import (ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView,
                                  CreateView,
                                  TemplateView)

from .models import Post, CustomUser
from .forms import PostForm
from comments.models import Comment
from comments.forms import CommentForm

from .utils import lecture_time

from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import render, get_object_or_404

from django.db.models import Q

from django.contrib.messages.views import SuccessMessageMixin

from django.http import HttpResponseRedirect
from django.urls import reverse


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


class TagPostListView(ListView):
    model = Post
    template_name = 'blog/tag_post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        tag = self.kwargs.get('tag')
        return Post.objects.filter(tags__name__in=[tag]).order_by('-date')


# class PostDetailView(DetailView):
#     model = Post
#     context_object_name = 'post'
#     slug_url_kwarg = 'slug'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         context['comments'] = post.comments.all()
#         return context

def PostDetailView(request, slug):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    user = get_object_or_404(CustomUser, username=request.user)
    comments = post.comments.filter(parent=None)

    word_count = lecture_time(post.content)
    new_comment = None
    parent_obj = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            try:
                parent_id = int(request.POST.get("parent_id"))
            except:
                parent_id = None

            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists():
                    parent_obj = parent_qs.first()

            post.comments.create(author=user,
                                 content=new_comment,
                                 parent=parent_obj)

            return HttpResponseRedirect(reverse('post_detail', args=[post.slug]))

    else:
        comment_form = CommentForm()

    context = {"post": post,
               "comments": comments,
               "new_comment": new_comment,
               "comment_form": comment_form,
               "word_count": word_count}

    return render(request, template_name, context)


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/post_form.html'
    # model = Post
    # fields = ['title', 'content', 'tags']
    success_message = "Post created successfully, please check it below."

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'tags']
    success_message = 'Post updated successfully, please check it below.'

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
