from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Posts
from .forms import PostForm

# Create your views here.
class PostView(View):
    def get(self, request):
        posts = Posts.objects.all()
        context = {
            'title': 'Blog',
            'posts': posts,
        }
        return render(request, 'posts/post_list.html', context)
    

class PostDetail(View):
    def get(self, request, post_id):
        post = Posts.objects.get(pk=post_id)
        context = {
            'post': post
        }
        return render(request, 'posts/post_detail.html', context)


class PostWrite(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        context = {
            'form': form
        }
        return render(request, 'posts/post_write.html', context)
    
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post.save()
            return redirect('blog:list')
            # return redirect('/blog/detail/' + str(post.id))
        print(form)
        form.add_error(None, '폼이 유효하지 않습니다.')
        context = {
            'form': form
        }
        return render(request, 'posts/post_write.html')
