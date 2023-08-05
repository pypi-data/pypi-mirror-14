import os

from django.conf.urls import include, patterns, url
from kagiso_search import views

urlpatterns = patterns(
    '',
    url(r'^search/', views.search, name='search'),   
)
