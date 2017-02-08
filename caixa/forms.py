from django import forms
from caixa.models import Caixa


class CaixaModelForm(forms.ModelForm):
	dinheiroCaixa = forms.FloatField(
		label  = 'Valor a ser Lançado no Caixa',
		widget = forms.NumberInput(
			attrs = {
				'placeholder':'Valor a ser Lançado no Caixa',
				'class': 'form-control'
			}
		)
	)

	
	class Meta:
		model = Caixa
		fields = ('dinheiroCaixa',)

