from django.conf.urls import  url
from cliente.views import *


urlpatterns = [
    url(r'^cliente/cadastrar/$',ClienteFormView.as_view(), name = 'cadastrar-cliente'),
    url(r'^cliente/listar/$',ClienteListView.as_view(), name = 'listar-cliente'),
    url(r'^cliente/(?P<pk>\d+)/$',ClienteDetailView.as_view(), name = "detalhe-cliente"),

	url(r'^cliente/(?P<pk>[\w-]+)/atualizar$',ClienteUpdateView.as_view(), name = 'update-cliente'),
    url(r'^cliente/(?P<pk>[\w-]+)/deletar/$',cliente_delete, name = 'delete-cliente'),

]