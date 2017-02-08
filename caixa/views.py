from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import *
from cliente.views import LoginRequiredMixin
from caixa.forms import CaixaModelForm
from servico.models import Pagamento,Servico
from despesa.models import Despesa
from caixa.models import Caixa
from datetime import date


class CaixaFormView(LoginRequiredMixin, FormView):
	template_name = u'caixa/cadastrar.html'
	form_class = CaixaModelForm
	success_url = reverse_lazy('lancar-dinheiro')

	def form_valid(self,form):
		caixa = form.save(commit = False)
		caixa.save()
		messages.success(self.request, u"Dinheiro lançado com sucesso!")
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self,form):
		messages.error(self.request, u"Por favor, preencha corretamente os campos")
		return self.render_to_response(self.get_context_data(form = form))


@login_required
def total_arrecadado(request):
	pagamento = Pagamento.objects.filter(data_pagamento = date.today())
	servico = Servico.objects.filter(data_servico = date.today())
	caixa = Caixa.objects.filter(data = date.today())
	despesa = Despesa.objects.filter(data_despesa = date.today())

	#Calcula o valor arrecadado no dia
	valor_arrecadado = 0
	for p in pagamento:
		valor_arrecadado += p.valor_pagamento
	#Calcula o valor emprestado no dia
	valor_emprestado = 0
	for s in servico:
		valor_emprestado += s.valor_servico
	#Calcula o valor das despesas no dia
	valor_despesas_gasolina = 0
	valor_despesas_comida = 0
	valor_despesas_outros = 0
	valor_despesas = 0
	for d in despesa:
		valor_despesas_gasolina += d.gasolina
		valor_despesas_comida += d.comida
		valor_despesas_outros += d.outros
		valor_despesas = valor_despesas_gasolina + valor_despesas_comida + valor_despesas_outros
	#Calcula o valor lançado no caixa durante dia
	valor_lancado_caixa = 0
	for c in caixa:
		valor_lancado_caixa += c.dinheiroCaixa
	#Calcula o valor atual em caixa
	valor_arrecadado = float(valor_arrecadado)
	valor_atual_caixa = (valor_lancado_caixa + valor_arrecadado) - (valor_emprestado + valor_despesas)
	
	return render(request, 'caixa/extrato.html', {"valor_arrecadado" : valor_arrecadado, "valor_emprestado":valor_emprestado,
	"valor_despesas":valor_despesas, "valor_lancado_caixa":valor_lancado_caixa,"valor_atual_caixa":valor_atual_caixa,
	"valor_despesas_gasolina":valor_despesas_gasolina, "valor_despesas_comida":valor_despesas_comida,"valor_despesas_outros":valor_despesas_outros,
	})
