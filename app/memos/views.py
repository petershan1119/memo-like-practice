try:
    from django.utils import simplejson as json
except ImportError:
    import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .forms import PostForm, UserForm
from .models import Memos

User = get_user_model()


@login_required
@require_POST
def like(request):
    if request.method == "POST":
        user = request.user
        memo_id = request.POST.get('pk', None)
        memo = Memos.objects.get(pk=memo_id)

        if memo.likes.filter(id=user.id).exists():
            memo.likes.remove(user)
            message = '좋아요 취소'
        else:
            memo.likes.add(user)
            message = "좋아요!"
    context = {
        'likes_count': memo.total_likes,
        'message': message,
    }
    return HttpResponse(json.dumps(context), content_type='application/json')


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


def delete(request, memokey):
    memo = Memos.objects.get(pk=memokey)
    memo.delete()
    return redirect('index')


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('index')
        else:
            return HttpResponse('사용자 이미 존재')
    else:
        form = UserForm()
        context = {
            'form': form,
        }
        return render(request, 'memos/adduser.html', context)