from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'jobs', views.JobViewSet, basename='job')
router.register(r'runs', views.ScraperRunViewSet, basename='scraperrun')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/stats/', views.stats_api, name='stats-api'),
    path('', views.dashboard, name='dashboard'),
]
