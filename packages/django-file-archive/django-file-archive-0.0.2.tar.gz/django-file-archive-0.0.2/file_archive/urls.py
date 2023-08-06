from django.conf.urls import url

from . import views


urlpatterns = [
    url( r'^(?P<slug>[\w\-]+)$', views.redirect_to_file, name='file_archive' ),
]
