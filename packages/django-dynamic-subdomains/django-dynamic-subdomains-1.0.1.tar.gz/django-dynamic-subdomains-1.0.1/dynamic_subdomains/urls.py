from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^redirect/(?P<host>.+)$', views.redirect_,
        name='redirect'),
)
