from django import forms
from despesa.models import Despesa


class DespesaModelForm(forms.ModelForm):
	gasolina = forms.FloatField(
		label  = 'Valor gasto com Gasolina',
		widget = forms.NumberInput(
			attrs = {
				'placeholder':'Valor gasto com Gasolina',
				'class': 'form-control'
			}
		)
	)

	comida = forms.FloatField(
		label  = 'Valor gasto com Comida',
		widget = forms.NumberInput(
			attrs = {
				'placeholder':'Valor gasto com Comida',
				'class': 'form-control'
			}
		)
	)

	outros = forms.FloatField(
		label  = 'Valor gasto com outras coisas',
		widget = forms.NumberInput(
			attrs = {
				'placeholder':'Valor gasto outras coisas',
				'class': 'form-control'
			}
		)
	)

	
	class Meta:
		model = Despesa
		fields = ('gasolina','comida','outros')

