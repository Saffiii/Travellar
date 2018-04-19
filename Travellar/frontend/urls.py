from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^recommendations$', views.recommendations, name='recommendations'),
    url(r'^flights', views.flights, name='flights'),
    url(r'^hotel', views.hotel, name='hotel'),
    url(r'^rental', views.rental, name='rental'),
]
