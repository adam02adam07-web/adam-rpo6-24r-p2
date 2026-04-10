from django.urls import path
from . import views
from .views import AdListCreateAPIView

urlpatterns = [
    path('api/ads/', AdListCreateAPIView.as_view(), name='api_ads'),
    path('', views.ad_list_view, name='ad_list'),
    path('category/<slug:slug>/', views.ad_list_view, name='category_list'),

    path('ad/new/', views.ad_create_view, name='ad_create'),
    path('ad/<uuid:uuid>/', views.ad_detail_view, name='ad_detail'),
    path('ad/<uuid:uuid>/edit/', views.ad_update_view, name='ad_update'),
    path('ad/<uuid:uuid>/delete/', views.ad_delete_view, name='ad_delete'),
    path('ad/<uuid:uuid>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('ad/<uuid:uuid>/review/', views.add_review, name='add_review'),

    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
