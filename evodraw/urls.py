
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('ilike/', views.ilike, name="ilike"),
    path('collections/', views.user_collections, name="user_collections"),

  #  path('dashboard/<slug:pop>/', views.dashboard, name="dashboard"),
  #  path('id/<str:individual>', views.details, name="details"),
  #  path('<slug:pop>/next', views.next, name="next"),
  #  path('<slug:pop>/new', views.new, name="new"),
]