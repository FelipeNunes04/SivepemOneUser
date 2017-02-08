from django.conf.urls import  url
from despesa.views import DespesaFormView


urlpatterns = [
    url(r'^despesa/cadastrar/$',DespesaFormView.as_view(), name = 'cadastrar-despesa'),
]