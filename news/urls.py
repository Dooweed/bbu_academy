from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("<str:article_url>/", views.article_view, name="article"),
    path("", views.news_list_view, name="news"),
]
