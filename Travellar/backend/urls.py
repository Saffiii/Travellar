from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^fbuser', views.fbuser, name='fbuser'),
    url(r'^googleplaces', views.googleplaces, name='googleplaces'),
    url(r'^recommend', views.recommend, name='recommend'),
    url(r'^als', views.recommendals, name='recommendals'),
]