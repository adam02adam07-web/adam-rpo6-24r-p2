from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseForbidden

# --- НОВЫЕ ИМПОРТЫ ДЛЯ API ---
from rest_framework import generics
from .serializers import AdSerializer
# ------------------------------

from .models import Ad, Category, Favorite, Banner, Review # Добавил Review
from .forms import UserRegisterForm, AdForm


# --- REST API VIEWS (Задание №3) ---

class AdListCreateAPIView(generics.ListCreateAPIView):
    """API для получения списка (GET) и создания (POST) объявлений"""
    queryset = Ad.objects.filter(is_moderated=True).order_by('-is_top', '-created_at')
    serializer_class = AdSerializer

# --- АВТОРИЗАЦИЯ ---

def register_view(request):
    if request.user.is_authenticated: return redirect('ad_list')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated: return redirect('profile')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('ad_list')

# --- ПРОФИЛЬ ---

@login_required
def profile_view(request):
    my_ads = Ad.objects.filter(author=request.user).order_by('-created_at')
    favorites = Favorite.objects.filter(user=request.user).select_related('ad')
    return render(request, 'profile.html', {'my_ads': my_ads, 'favorites': favorites})

# --- ОБЪЯВЛЕНИЯ (КАТАЛОГ И ДЕТАЛИ) ---

def ad_list_view(request, slug=None):
    # ОБНОВЛЕНО: Сначала показываем ТОП объявления (-is_top)
    ads = Ad.objects.filter(is_moderated=True).order_by('-is_top', '-created_at')
    
    if slug: ads = ads.filter(category__slug=slug)

    # Поиск
    q = request.GET.get('q')
    if q: ads = ads.filter(Q(title__icontains=q) | Q(description__icontains=q))

    # Сортировка (сохраняем приоритет ТОП при любой сортировке)
    sort = request.GET.get('sort')
    if sort == 'cheap': ads = ads.order_by('-is_top', 'price')
    elif sort == 'expensive': ads = ads.order_by('-is_top', '-price')
    elif sort == 'free': ads = ads.filter(price=0).order_by('-is_top', '-created_at')

    # Пагинация
    page_obj = Paginator(ads, 8).get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'banners': Banner.objects.filter(is_active=True),
        'current_category': slug,
        'query_params': request.GET.copy().pop('page', True) and request.GET.urlencode()
    }
    return render(request, 'ad_list.html', context)

def ad_detail_view(request, uuid):
    ad = get_object_or_404(Ad, uuid=uuid)
    # Получаем отзывы для этого объявления (Задание №4)
    reviews = ad.reviews.all().order_by('-created_at')
    
    is_favorite = request.user.is_authenticated and Favorite.objects.filter(user=request.user, ad=ad).exists()
    return render(request, 'ad_detail.html', {
        'ad': ad, 
        'is_favorite': is_favorite,
        'reviews': reviews
    })

# --- CRUD ОБЪЯВЛЕНИЙ ---

@login_required
def ad_create_view(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES) 
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.is_moderated = False 
            ad.save()
            messages.success(request, 'Объявление отправлено на проверку.')
            return redirect('profile')
    else:
        form = AdForm()
    return render(request, 'ad_form.html', {'form': form})

@login_required
def ad_update_view(request, uuid):
    ad = get_object_or_404(Ad, uuid=uuid)
    if ad.author != request.user: return HttpResponseForbidden("Доступ запрещен.")

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление обновлено.')
            return redirect('ad_detail', uuid=ad.uuid)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ad_form.html', {'form': form})

@login_required
def ad_delete_view(request, uuid):
    ad = get_object_or_404(Ad, uuid=uuid)
    if ad.author != request.user: return HttpResponseForbidden("Доступ запрещен.")

    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Объявление удалено.')
        return redirect('profile')
    return render(request, 'ad_confirm_delete.html', {'ad': ad})

# --- ИЗБРАННОЕ ---

@login_required
def toggle_favorite(request, uuid):
    ad = get_object_or_404(Ad, uuid=uuid)
    fav, created = Favorite.objects.get_or_create(user=request.user, ad=ad)
    if not created: fav.delete()
    return redirect(request.META.get('HTTP_REFERER', 'ad_list'))

# --- ОТЗЫВЫ ---

@login_required
def add_review(request, uuid):
    ad = get_object_or_404(Ad, uuid=uuid)
    if request.method == 'POST' and request.user != ad.author:
        text = request.POST.get('text', '').strip()
        try:
            rating = int(request.POST.get('rating', 0))
        except (ValueError, TypeError):
            rating = 0
        if text and 1 <= rating <= 5:
            Review.objects.create(ad=ad, author=request.user, text=text, rating=rating)
            messages.success(request, 'Отзыв добавлен!')
        else:
            messages.error(request, 'Пожалуйста, заполните отзыв и выберите оценку.')
    return redirect('ad_detail', uuid=uuid)
