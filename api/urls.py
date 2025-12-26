from django.urls import path
from . import views
from .views import health

urlpatterns = [
    path('health/', health, name='api_health'),

    path('subjects/', views.subjects_api),
    path('units/<int:subject_id>/', views.units_api),
    path('topics/<int:unit_id>/', views.topics_api),
]
