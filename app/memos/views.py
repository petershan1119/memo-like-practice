import json

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import Memos


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