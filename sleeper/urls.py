from django.urls import path
from sleeper import views as sleeper_views

urlpatterns = [
    path('league/<str:league_id>/', sleeper_views.SleeperAPI.as_view(), name='sleeper-api'),
]
