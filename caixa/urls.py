from django.conf.urls import  url
from caixa.views import *


urlpatterns = [
    url(r'^caixa/extrato/$', total_arrecadado, name = 'extrato'),
    url(r'^caixa/cadastrar/$',CaixaFormView.as_view(), name = 'lancar-dinheiro'),

]