from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('login', views.home, name=''),
    path('', views.index, name=''),
    path('regis_page', views.registration, name=''),
    path('regis.html', views.index, name=''),
    path('home', views.home, name=''),
    path('login_page', views.login_page, name=''),
    path('home.html', views.home, name=''),
    path('fetch_info',views.fetch_info, name='fetch_info'),
    path('add',views.secondPartNew, name='display_info'),
    path('check',views.fetch_info, name=''),
    path('download/',views.download, name = 'download'),
    #path('data.csv',views.downfile, name = 'down'),
    path('allow.html',views.allow, name=''),	
    path('insert',views.insert, name=''),
    path('logout.html',views.logout, name=''),	
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
]
