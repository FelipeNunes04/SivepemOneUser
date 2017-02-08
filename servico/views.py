from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic.edit import *
from django.views.generic.list import *
from django.views.generic import *
from servico.models import *
from cliente.models import *
from servico.forms import * 
from cliente.views import LoginRequiredMixin
from datetime import date,datetime


class ServicoFormView(LoginRequiredMixin, FormView):
	template_name = u'servico/cadastrar.html'
	form_class = ServicoModelForm
	success_url = reverse_lazy('cadastrar-servico')

	def form_valid(self,form):
		servico = form.save(commit = False)
		cliente = Cliente.objects.get(codigo = servico.codigo_cliente)
		if not cliente.devendo:
			if servico.numero_parcelas < 1:
				messages.error(self.request, u"O número de parcelas deve ser maior que ZERO!")
				return self.render_to_response(self.get_context_data(form = form))
			elif cliente.limite >= servico.valor_servico:
				''' Realiza calculos da parcela e adiciona um dia a data de vencimento da parcela. '''
				id = servico.codigo;
				servico.calcula_parcela()
				servico.cliente_devendo()
				servico.primeira_pacela()
				servico.save()
				messages.success(self.request, u"Serviço cadastrado com sucesso!")
				return HttpResponseRedirect(self.get_success_url())
			else:
				messages.error(self.request, u"O valor do serviço é maior do que o limite do Cliente!")
				return self.render_to_response(self.get_context_data(form = form))
		else:
			messages.error(self.request, u"Cliente com serviço em aberto!")
			return self.render_to_response(self.get_context_data(form = form))

	def form_invalid(self,form):
		messages.error(self.request, u"Por favor, preencha corretamente os campos")
		return self.render_to_response(self.get_context_data(form = form))

class ServicoListView(LoginRequiredMixin, ListView):
	template_name = u'servico/listar.html'

	def get_queryset(self):
		servico = Servico.objects.filter(pago = False)
		return servico

class ServicoPagoListView(LoginRequiredMixin, ListView):
	template_name = u'servico/listar_pago.html'

	def get_queryset(self):
		servico = Servico.objects.filter(pago = True)
		return servico

class SevicoDetailView(LoginRequiredMixin, DetailView):
	template_name = u'servico/detalhe.html'
	model = Servico

class ServicoUpdateView(LoginRequiredMixin, UpdateView):
	template_name = u'servico/editar.html'
	model = Servico
	form_class = ServicoModelForm
	success_url = reverse_lazy('listar-servico')

	def form_valid(self,form):
		servico = form.save(commit = False)
		cliente = Cliente.objects.get(codigo = servico.codigo_cliente)
		parcela_extra = ParcelaExtra.objects.filter(servico = servico.codigo)
		if servico.numero_parcelas < 1:
			messages.error(self.request, u"O número de parcelas deve ser maior que ZERO!")
			return self.render_to_response(self.get_context_data(form = form))
		elif cliente.limite >= servico.valor_servico:
			servico.cliente_devendo()
			parcela_extra.delete()
			servico.calcula_parcela()
			servico.save()
			messages.success(self.request, u"Serviço Atualizado com sucesso!")
			return HttpResponseRedirect(self.get_success_url())
		else:
			messages.error(self.request, u"O valor do serviço é maior do que o limite do Cliente!")
			return self.render_to_response(self.get_context_data(form = form))

	def form_invalid(self,form):
		messages.error(self.request, u"Por favor, preencha corretamente os campos")
		return self.render_to_response(self.get_context_data(form = form))

@login_required
def servico_delete(request, pk):
	servico = Servico.objects.get(codigo = pk)
	cliente = Cliente.objects.get(codigo = servico.codigo_cliente)
	parcela_extra = ParcelaExtra.objects.filter(servico = servico.codigo)
	cliente.pagar()
	parcela_extra.delete()
	servico.delete()
	return redirect('listar-servico')

class PagamentoFormView(LoginRequiredMixin, FormView):
	template_name = u'pagamento/cadastrar.html'
	form_class = PagamentoModelForm
	success_url = reverse_lazy('cadastrar-pagamento')

	def form_valid(self,form):
		pagamento = form.save(commit = False)
		servico = Servico.objects.get(codigo = pagamento.codigo_servico)
		if servico.pago:
			messages.error(self.request, u"Esse serviço já está pago!")
			return self.render_to_response(self.get_context_data(form = form))
		elif pagamento.valor_pagamento > servico.valor_parcela:
			messages.error(self.request, u"O valor do pagamento não pode ser maior que o valor da parcela!")
			return self.render_to_response(self.get_context_data(form = form))
		elif servico.numero_parcelas == 0 and pagamento.valor_pagamento > servico.valor_parcela_extra:
			messages.error(self.request, u"O valor do pagamento não pode ser maior que o valor da parcela!")
			return self.render_to_response(self.get_context_data(form = form))
		else:
			servico.calcula_vencimento()
			servico.save()
			pagamento.calculos()
			pagamento.save()
			messages.success(self.request, u"Pagamento realizado com sucesso!")
			return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self,form):
		messages.error(self.request, u"Por favor, preencha corretamente os campos")
		return self.render_to_response(self.get_context_data(form = form))

class SaldoFormView(LoginRequiredMixin, FormView):
	template_name = u'saldo/cadastrar.html'
	form_class = SaldoModelForm
	success_url = reverse_lazy('listar-saldo')

	def form_valid(self,form):
		saldo = Saldo.objects.all()
		saldo.delete()
		saldo = form.save(commit = False)
		saldo.save()
		messages.success(self.request, u"Estes são os serviços deste Cliente.")
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self,form):
		messages.error(self.request, u"Por favor, digite o código de um cliente existente.")
		return self.render_to_response(self.get_context_data(form = form))


class SaldoListView(LoginRequiredMixin, ListView):
	template_name = u'saldo/listar.html'

	def get_queryset(self):
		saldo = Saldo.objects.get(codigo = 1)
		servico = Servico.objects.filter(codigo_cliente = saldo.codigo_cliente)
		return servico

