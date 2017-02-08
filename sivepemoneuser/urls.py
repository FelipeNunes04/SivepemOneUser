from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from cliente.views import *


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cliente/', include('cliente.urls')),
    url(r'^servico/', include('servico.urls')),
    url(r'^despesa/', include('despesa.urls')),
    url(r'^caixa/', include('caixa.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),

    url(r'^$', Home.as_view(), name='home'),

    url(r'^usuario/login/$','django.contrib.auth.views.login',{'template_name':'autenticacao/login.html'},name='login'),
    url(r'^usuario/logout/$','django.contrib.auth.views.logout',{'template_name':'autenticacao/logout.html'},name='logout'),
]
