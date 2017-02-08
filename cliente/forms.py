# -*- coding: utf-8 -*-

from django import forms
from localflavor.br.forms import *
from .models import *

class ClienteModelForm(forms.ModelForm):
	nome = forms.CharField(
		label = "Nome",
		widget = forms.TextInput(
			attrs = {
				'placeholder': 'Nome do Cliente',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)
	codigo = forms.CharField(
		label = "Código",
		widget = forms.TextInput(
			attrs = {
				'placeholder': 'Código',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)
	cpf = forms.ImageField(
		label = "CPF",
		required = True
	)
	telefone = BRPhoneNumberField(
		label = "Telefone",
		widget = forms.TextInput(
			attrs = {
				'placeholder': 'Telefone',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)
	endereco = forms.CharField(
		label = "Endereço",
		widget = forms.TextInput(
			attrs = {
				'placeholder': 'Endereço',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)
	limite = forms.FloatField(
		label = "Limite",
		widget = forms.NumberInput(
			attrs = {
				'placeholder': 'Valor Limite para serviços',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)
	class Meta:
		model = Cliente
		fields = ('nome', 'codigo', 'cpf', 'telefone','endereco','limite')



class ClienteUpdateModelForm(forms.ModelForm):
	nome = forms.CharField(
		label = "Nome",
		widget = forms.TextInput(
			attrs = {
				'placeholder': 'Nome do Cliente',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)
	cpf = forms.ImageField(
		label = "CPF",
		required = True
	)
	telefone = BRPhoneNumberField(
		label = "Telefone",
		widget = forms.TextInput(
			attrs = {
				'placeholder': 'Telefone',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)
	endereco = forms.CharField(
		label = "Endereço",
		widget = forms.TextInput(
			attrs = {
				'placeholder': 'Endereço',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)
	limite = forms.FloatField(
		label = "Limite",
		widget = forms.NumberInput(
			attrs = {
				'placeholder': 'Valor Limite para serviços',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)
	class Meta:
		model = Cliente
		fields = ('nome', 'cpf', 'telefone','endereco','limite')
