from django.shortcuts import render
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

posts=[
   {
        'title':'The Waste Land',
        'author':'T.S.Eliot',
        'content':'An excellent master piece',
        'date_posted':'1978'
   },
   {    
        'title':'This Be The Verse',
        'author':'Philip Larkin',
        'content':'A great poet in  England',
        'date_posted':'1876'
   } 
]



def home(request):
    ctx={'posts':Post.objects.all()}
    return render(request, 'blog/home.html', ctx)


class PostListView(ListView):
     model = Post
     template_name = 'blog/home.html'
     context_object_name = 'posts'
     ordering = ['-date_posted']


class PostDetailView(DetailView):
     model = Post
      

class PostCreateView(LoginRequiredMixin, CreateView):
     model = Post
     fields = ['title', 'content']

     def form_valid(self, form):
          form.instance.author = self.request.user
          return super().form_valid(form)   


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
     model = Post
     fields = ['title', 'content']

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
     success_url = '/'

     def test_func(self):
          post = self.get_object()
          if self.request.user == post.author:
               return True
          return False         


def about(request):
    return render(request, 'blog/about.html', {'title':'About'})