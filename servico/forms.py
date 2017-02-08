from django import forms
from servico.models import *
from cliente.models import Cliente


class ServicoModelForm(forms.ModelForm):
	codigo = forms.CharField(
		label = 'Código do Serviço',
		widget = forms.TextInput(
			attrs = {
				'placeholder': 'Código do serviço',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)

	codigo_cliente = forms.ModelChoiceField(
		queryset = Cliente.objects.all(),
		label  = 'Código do Cliente',
		widget = forms.TextInput(
			attrs = {
				'placeholder': 'Código do cliente',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)

	valor_servico = forms.FloatField(
		label  = 'Valor do Serviço',
		widget = forms.NumberInput(
			attrs = {
				'placeholder':'Valor do Serviço',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)

	juros = forms.FloatField(
		label  = 'Juros Cobrado',
		widget = forms.NumberInput(
			attrs = {
				'placeholder':'Juros do Serviço',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)	

	numero_parcelas = forms.IntegerField(
		label  = 'Número de Parcelas',
		widget = forms.NumberInput(
			attrs = {
				'placeholder': 'Número de Parcelas',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)

	tipo_parcelamento = forms.ChoiceField(
		label = 'Tipo de Parcelamento', 
		choices=PARCELAS_CHOICES,
	)

	
	class Meta:
		model = Servico 
		fields = ('codigo','codigo_cliente','valor_servico','juros','numero_parcelas','tipo_parcelamento')



class ServicoUpdateModelForm(forms.ModelForm):
	valor_servico = forms.FloatField(
		label  = 'Valor do Serviço',
		widget = forms.NumberInput(
			attrs = {
				'placeholder':'Valor do Serviço',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)

	juros = forms.FloatField(
		label  = 'Juros Cobrado',
		widget = forms.NumberInput(
			attrs = {
				'placeholder':'Juros do Serviço',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)	

	numero_parcelas = forms.IntegerField(
		label  = 'Número de Parcelas',
		widget = forms.NumberInput(
			attrs = {
				'placeholder': 'Número de Parcelas',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)

	tipo_parcelamento = forms.ChoiceField(
		label = 'Tipo de Parcelamento', 
		choices=PARCELAS_CHOICES,
	)

	
	class Meta:
		model = Servico 
		fields = ('valor_servico','juros','numero_parcelas','tipo_parcelamento')




class PagamentoModelForm(forms.ModelForm):
	codigo_servico = forms.ModelChoiceField(
		queryset = Servico.objects.all(),
		label  = 'Código do Serviço',
		widget = forms.TextInput(
			attrs = {
				'placeholder': 'Código do Serviço',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)

	valor_pagamento = forms.FloatField(
		label = 'Valor do Pagamento',
		widget = forms.NumberInput(
			attrs = {
				'placeholder': 'Valor do Pagamento',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)

	class Meta:
		model = Pagamento 
		fields = ('codigo_servico', 'valor_pagamento')

class SaldoModelForm(forms.ModelForm):
	codigo_cliente = forms.ModelChoiceField(
		queryset = Cliente.objects.all(),
		label  = 'Código do Cliente',
		widget = forms.TextInput(
			attrs = {
				'placeholder': 'Código do cliente',
				'required': 'required',
				'class': 'form-control'
			}
		)
	)

	class Meta:
		model = Saldo
		fields = ('codigo_cliente',)