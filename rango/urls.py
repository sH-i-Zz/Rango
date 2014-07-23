from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^add_category/$', views.add_category , name = 'add_category'),
        url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),
        url(r'^category/(?P<category_name_url>\w+)/add_page/$', views.add_page, name='add_page'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.login_view, name='login'),
        url(r'^restricted/', views.restricted, name='restricted'),
        url(r'^logout/$', views.user_logout, name='logout'),
        )

urlpatterns += patterns(
    'django.contrib.auth.views',
    
    url(r'^login/$', 'login',
        {'template_name': 'login.html'},
        name='login'),
    
    url(r'^logout/$', 'logout',
        {'next_page': 'index'},
        name='logout'),  
)