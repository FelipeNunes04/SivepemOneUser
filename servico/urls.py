from django.conf.urls import  url
from servico.views import *


urlpatterns = [
    url(r'^servico/cadastrar/$',ServicoFormView.as_view(), name = 'cadastrar-servico'),
    url(r'^servico/listar/$',ServicoListView.as_view(), name = 'listar-servico'),
    url(r'^servico/listar/pago/$',ServicoPagoListView.as_view(), name = 'listar-servico-pago'),
    url(r'^servico/(?P<pk>\d+)/$',SevicoDetailView.as_view(), name = "detalhe-servico"),

	url(r'^servico/(?P<pk>[\w-]+)/atualizar$',ServicoUpdateView.as_view(), name = 'update-servico'),
    url(r'^servico/(?P<pk>[\w-]+)/deletar/$', servico_delete, name = 'delete-servico'),

    url(r'^saldo/cadastrar/$',SaldoFormView.as_view(), name = 'cadastrar-saldo'),
    url(r'^saldo/listar/$',SaldoListView.as_view(), name = 'listar-saldo'),

     url(r'^pagamento/cadastrar/$',PagamentoFormView.as_view(), name = 'cadastrar-pagamento'),

]