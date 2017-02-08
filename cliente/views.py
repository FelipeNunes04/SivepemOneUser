from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.views.generic.edit import *
from django.views.generic.list import *
from django.views.generic import *
from cliente.models import *
from cliente.forms import *
import os

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class Home(LoginRequiredMixin, TemplateView):
	template_name = u'index.html'

class ClienteFormView(LoginRequiredMixin, FormView):
	template_name = u'cliente/cadastrar.html'
	form_class = ClienteModelForm
	success_url = reverse_lazy('cadastrar-cliente')

	def form_valid(self,form):
		cliente = form.save(commit = False)
		cliente.save()
		messages.success(self.request, u"Cliente cadastrado com sucesso!")
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self,form):
		messages.error(self.request, u"Por favor, preencha corretamente os campos")
		return self.render_to_response(self.get_context_data(form = form))

class ClienteListView(LoginRequiredMixin, ListView):
	template_name = u'cliente/listar.html'

	def get_queryset(self):
		cliente = Cliente.objects.all().order_by('nome')
		return cliente

class ClienteDetailView(LoginRequiredMixin, DetailView):
	template_name = u'cliente/detalhe.html'
	model = Cliente

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
	template_name = u'cliente/editar.html'
	model = Cliente
	form_class = ClienteUpdateModelForm
	success_url = reverse_lazy('listar-cliente')

	def form_valid(self,form):
		cliente = form.save(commit = False)
		cliente.save()
		messages.success(self.request, u"Cliente atualizado com sucesso!")
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self,form):
		messages.error(self.request, u"Por favor, preencha corretamente os campos")
		return self.render_to_response(self.get_context_data(form = form))

@login_required
def cliente_delete(request, pk):
	cliente = Cliente.objects.get(codigo = pk)
	os.unlink("/home/felipe/sivepemoneuser"+cliente.cpf.url)
	cliente.delete()
	return redirect('listar-cliente')