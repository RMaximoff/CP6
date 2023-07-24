from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, TemplateView, DeleteView

from apps.blog.forms import BlogForm
from apps.blog.models import Blog


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class PostCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_detail')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class PostUpdateView(UpdateView):
    model = Blog
    form_class = BlogForm

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.object.slug})


class PostView(DetailView):
    model = Blog
    slug_url_kwarg = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.count_views += 1
        self.object.save()
        return context


class PostDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')



