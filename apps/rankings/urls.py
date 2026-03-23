"""URLs de rankings."""

from django.urls import path

from . import views

app_name = 'rankings'

urlpatterns = [
    path('', views.RankingListView.as_view(), name='list'),
    path('me/', views.MiRankingView.as_view(), name='me'),
]
