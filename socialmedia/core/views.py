from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import json
from django.http import HttpResponseForbidden

from .models import *
from .forms import *


@login_required
def home(request):
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    posts = Post.objects.filter(user__in=following_users).order_by('-created_at')
    
    users = User.objects.filter(is_superuser=False)
    suggestions = User.objects.exclude(id__in=following_users)\
                              .exclude(id=request.user.id)\
                              .filter(is_superuser=False)[:5]

    return render(request, 'core/home.html', {
        'posts': posts,
        'users': users,
        'suggestions': suggestions,
    })

from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        image = request.FILES['image']
        caption = request.POST['caption']
        Post.objects.create(user=request.user, image=image, caption=caption)
        return redirect('home')
    return render(request, 'core/create_post.html')

@require_POST
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    return JsonResponse({'likes_count': post.likes.count(), 'liked': liked})
    

@require_POST
@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    text = request.POST.get('comment')
    if text:
        Comment.objects.create(post=post, user=request.user, text=text)
    comments_html = render_to_string("core/partials/comments.html", {'post': post})
    return JsonResponse({'comments_html': comments_html})



login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profile_user).order_by('-created_at')

    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'profile': profile_user.profile,
        'is_following': is_following,
    }

    return render(request, 'core/profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        bio = request.POST.get('bio', '').strip()
        profile_pic = request.FILES.get('profile_pic')

        if not first_name:
            return render(request, 'core/edit_profile.html', {'error': 'First name required'})

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        profile.bio = bio
        if profile_pic:
            profile.profile_pic = profile_pic
        profile.save()

        return redirect('profile', username=user.username)

    return render(request, 'core/edit_profile.html')


@login_required
def delete_post(request, post_id):
    if request.user.is_superuser:
        post = get_object_or_404(Post, id=post_id)
        post.delete()
    return redirect('home')

@login_required
def delete_comment(request, comment_id):
    if request.user.is_superuser:
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
    return redirect('home')

@login_required
def delete_user(request, user_id):
    if request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)
        user.delete()
    return redirect('home')



def search_users(request):
    query = request.GET.get('q')
    users = User.objects.filter(username__icontains=query) if query else []
    return render(request, 'core/search_results.html', {'users': users})

def view_profile(request, username):
    profile_user = User.objects.get(username=username)
    posts = Post.objects.filter(user=profile_user).order_by('-created_at')

    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    return render(request, 'core/profile.html', {
        'profile_user': profile_user,
        'profile': profile_user.profile,
        'posts': posts,
        'is_following': is_following,
    })

def load_posts(request):
    page = request.GET.get('page')
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 3)

    try:
        posts_page = paginator.page(page)
    except:
        return HttpResponse("")

    html = ""
    for post in posts_page:
        html += render_to_string("core/partials/post_card.html", {'post': post, 'request': request})
    return HttpResponse(html)

@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)

    if request.user == target_user:
        return redirect('profile', username=username)

    follow_relation, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )

    if not created:
        follow_relation.delete()  

    return redirect('profile', username=target_user.username)

@csrf_exempt
@login_required
def follow_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")

        target_user = User.objects.get(id=user_id)
        Follow.objects.get_or_create(follower=request.user, following=target_user)

        return JsonResponse({'status': 'followed'})
    return JsonResponse({'status': 'error'})






