from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^fbuser', views.fbuser, name='fbuser'),
]