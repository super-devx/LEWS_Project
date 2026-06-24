from django.urls import path
from django.conf.urls import url
from . import views
from . import cross_correlation_views
urlpatterns = [
    path('login', views.monitoring_page, name=''),
    path('', views.index, name='landing'),
    path('regis_page', views.registration, name=''),
    path('regis.html', views.login_form, name='login_form'),
    path('home', views.monitoring_page, name='home'),
    path('analysis', views.home, name='analysis'),
    path('monitoring', views.monitoring_page, name='monitoring'),
    path('login_page', views.login_page, name=''),
    path('home.html', views.monitoring_page, name=''),
    path('signin', views.login_form, name='signin'),
    path('register', views.register_form, name='register_form'),
    path('fetch_info',views.fetch_info, name='fetch_info'),
    path('add',views.secondPartNew, name='display_info'),
    path('check',views.fetch_info, name=''),
    path('download/',views.download, name = 'download'),
    #path('data.csv',views.downfile, name = 'down'),
    path('allow.html',views.allow, name=''),
    path('insert',views.insert, name=''),
    path('logout.html',views.logout, name='logout_legacy'),
    # New pages
    path('profile', views.profile_view, name='profile'),
    path('profile/update', views.update_profile, name='update_profile'),
    path('about', views.about, name='about'),
    path('mission', views.mission, name='mission'),
    path('contact', views.contact, name='contact'),
    path('coming-soon', views.coming_soon, name='coming_soon'),
    path('team', views.team, name='team'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('api/tenants/register', views.api_register_tenant, name='api_register_tenant'),
    path('cross-correlation/', cross_correlation_views.cross_correlation_page, name='cross_correlation'),
    path('cross-correlation/analyze/', cross_correlation_views.cross_correlation_analyze, name='cross_correlation_analyze'),
]
