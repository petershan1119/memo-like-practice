import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .forms import PostForm
from .models import Memos

User = get_user_model()

def index(request):
    sort = request.GET.get('sort', '')
    if sort == 'likes':
        memos = Memos.objects.annotate(like_counts=Count('likes')).order_by('-like_counts', '-update_date')
        context = {
            'memos': memos,
        }
        return render(request, 'memos/index.html', context)
    elif sort == 'mypost':
        user = request.user
        memos = Memos.objects.filter(name_id=user).order_by('-update_date')
        context = {
            'memos': memos,
        }
        return render(request, 'memos/index.html', context)
    else:
        memos = Memos.objects.order_by('-update_date')
        context = {
            'memos': memos,
        }
        return render(request, 'memos/index.html', context)


def post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            # memo.name_id = User.objects.get(username=request.user.username)
            memo.generate()
            return redirect('index')
    else:
        form = PostForm()
        context = {
            'form': form,
        }
        return render(request, 'memos/form.html', context)


def modify(request, memokey):
    if request.method == 'POST':
        memo = Memos.objects.get(pk=memokey)
        form = PostForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        memo = Memos.objects.get(pk=memokey)
        form = PostForm(instance=memo)
        context = {
            'memo': memo,
            'form': form,
        }
        return render(request, 'memos/modify.html', context)