from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import *
from cliente.views import LoginRequiredMixin
from despesa.forms import DespesaModelForm

class DespesaFormView(LoginRequiredMixin, FormView):
	template_name = "despesa/cadastrar.html"
	form_class = DespesaModelForm
	success_url = reverse_lazy('cadastrar-despesa')

	def form_valid(self,form):
		despesa = form.save(commit = False)
		despesa.save()
		messages.success(self.request, u"Despesa cadastrada com sucesso!")
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self,form):
		messages.error(self.request, u"Por favor, preencha corretamente os campos")
		return self.render_to_response(self.get_context_data(form = form))
