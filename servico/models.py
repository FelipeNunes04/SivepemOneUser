from django.db import models
from cliente.models import *
from django.db.models import signals
from datetime import date

PARCELAS_CHOICES = (
	('Diario','Diario'),
	('Semanal','Semanal'),
	('Quizenal','Quizenal'),
	('Mensal','Mensal'),
)
lista_feriados = [[1,1],[2,11],[15,11],[25,12]]

class Servico(models.Model):
	codigo = models.CharField(max_length = 50, primary_key = True)
	codigo_cliente = models.ForeignKey(Cliente, related_name="codigo_cliente")
	valor_servico = models.FloatField()
	juros = models.FloatField()
	valor_total = models.FloatField()
	numero_parcelas = models.IntegerField()
	valor_parcela = models.FloatField()
	tipo_parcelamento = models.CharField( max_length = 25, choices = PARCELAS_CHOICES)
	data_servico = models.DateField("Data do serviço", auto_now_add = True)
	vencimento_parcela = models.DateField("Vencimento da Parcela", auto_now_add = True)
	vencimento_ultima_parcela = models.DateField(auto_now_add = True)
	pago = models.BooleanField(default = False)
	numero_parcelas_extra = models.IntegerField(default = 0) 
	valor_parcela_extra = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
	cont_feriados = models.IntegerField(default = 0) 

	def calcula_parcela(self):
		self.valor_total = self.valor_servico + self.valor_servico * (self.juros / 100)
		self.valor_parcela = self.valor_total / self.numero_parcelas
		self.pago = False
		self.valor_parcela_extra = 0
		self.numero_parcelas_extra = 0
		self.save()
	def primeira_pacela(self):		
		if self.tipo_parcelamento == "Diario":
			data_vencimento = self.vencimento_parcela.fromordinal(self.vencimento_parcela.toordinal()+2)
			dias = self.numero_parcelas - 1
		elif self.tipo_parcelamento == "Semanal":
			data_vencimento = self.vencimento_parcela.fromordinal(self.vencimento_parcela.toordinal()+8)
			dias = (self.numero_parcelas - 1) * 7
		elif self.tipo_parcelamento == "Quizenal":
			data_vencimento = self.vencimento_parcela.fromordinal(self.vencimento_parcela.toordinal()+16)
			dias = (self.numero_parcelas - 1) * 15
		else:
			data_vencimento = self.vencimento_parcela.fromordinal(self.vencimento_parcela.toordinal()+31)
			dias = (self.numero_parcelas - 1) * 30
		

		#Data de vencimento da ultima parcela recebe o numero de dias que serão contados
		data_vencimento_ultima = data_vencimento.fromordinal(data_vencimento.toordinal()+dias)

		cont = 0
		#Verifica se a data da primeira parcela é em algum feriado ou é domingo
		for i in range(len(lista_feriados)):
			while (data_vencimento.day==lista_feriados[i][0] and data_vencimento.month==lista_feriados[i][1]) or data_vencimento.weekday() == 6:
				data_vencimento = data_vencimento.fromordinal(data_vencimento.toordinal()+1)
				cont+=1

		#Verifica se o tipo de parcelamento é diário e retira os domingos e feriados da soma dos dias
		if self.tipo_parcelamento == "Diario":
			cont_dias = dias
			for d in range(dias):
				dia_parcela_qualquer = data_vencimento.fromordinal(data_vencimento.toordinal()+d)
				for i in range(len(lista_feriados)):
					if (dia_parcela_qualquer.day==lista_feriados[i][0] and dia_parcela_qualquer.month==lista_feriados[i][1]) or dia_parcela_qualquer.weekday() == 6:
				  		cont_dias+=1
				  		break
			print(cont_dias)
			#Atribui ao numero de dias o valor do mesmo sem domingos e feriados, e a data de vencimento da última parcela recebe a nova data de vencimento mais os dias
			dias = cont_dias
			data_vencimento_ultima = data_vencimento.fromordinal(data_vencimento.toordinal()+dias)
		
		#Verifica se a data da ultima parcela é em algum feriado ou é domingo
		for i in range(len(lista_feriados)):
			while (data_vencimento_ultima.day==lista_feriados[i][0] and data_vencimento_ultima.month==lista_feriados[i][1]) or data_vencimento_ultima.weekday() == 6:
				data_vencimento_ultima = data_vencimento_ultima.fromordinal(data_vencimento_ultima.toordinal()+1)

		
		self.cont_feriados = cont
		self.vencimento_ultima_parcela = data_vencimento_ultima
		self.vencimento_parcela = data_vencimento
		self.save()

	def calcula_vencimento(self):
		#Verifica qual o tipo da parcela
		if self.tipo_parcelamento == "Diario":
			self.vencimento_parcela = self.vencimento_parcela.fromordinal(self.vencimento_parcela.toordinal()+1)
		elif self.tipo_parcelamento == "Semanal":
			self.vencimento_parcela = self.vencimento_parcela.fromordinal(self.vencimento_parcela.toordinal()+7)
		elif self.tipo_parcelamento == "Quizenal":
			self.vencimento_parcela = self.vencimento_parcela.fromordinal(self.vencimento_parcela.toordinal()+15)
		else:
			self.vencimento_parcela = self.vencimento_parcela.fromordinal(self.vencimento_parcela.toordinal()+30)

		#verifica se no dia da parcela passada teve feriado
		if self.tipo_parcelamento != "Diario" and self.cont_feriados>0:
			self.vencimento_parcela = self.vencimento_parcela.fromordinal(self.vencimento_parcela.toordinal()-self.cont_feriados)
		
		cont = 0
		#Verifica se a data é em algum feriado ou é domingo
		for i in range(len(lista_feriados)):
			while (self.vencimento_parcela.day == lista_feriados[i][0] and self.vencimento_parcela.month == lista_feriados[i][1]) or self.vencimento_parcela.weekday() == 6:
				self.vencimento_parcela = self.vencimento_parcela.fromordinal(self.vencimento_parcela.toordinal()+1)		
				cont+=1
		
		self.cont_feriados = cont
		self.save()

	def cliente_devendo(self):
		cliente = Cliente.objects.get(codigo = self.codigo_cliente)
		cliente.devendo = True
		cliente.save()

	def servico_pago(self):
		self.pago = True
		cliente = Cliente.objects.get(codigo = self.codigo_cliente)
		cliente.pagar()
		self.save()
		cliente.save()

	def __str__(self):
		return self.codigo

class Pagamento(models.Model):
	codigo_servico = models.ForeignKey(Servico, related_name = "codigo_servico")
	valor_pagamento = models.FloatField()
	data_pagamento = models.DateField("Data do pagamento", auto_now_add = True)

	def calculos(self):
		servico = Servico.objects.get(codigo = self.codigo_servico)
		if servico.numero_parcelas > 0:
			servico.valor_total -= self.valor_pagamento
			servico.numero_parcelas -= 1
			if self.valor_pagamento < servico.valor_parcela:
				v_parcela_extra = servico.valor_parcela - self.valor_pagamento
				num_parcela_extra = 0
				parcela_extra = ParcelaExtra(
					numero_parcela_extra = servico.numero_parcelas_extra,
				 	valor_parcela_extra = v_parcela_extra,
				 	servico = self.codigo_servico,
				 )
				parcela_extra.save()
				for p in ParcelaExtra.objects.filter(servico = servico.codigo):
					num_parcela_extra += 1
				servico.numero_parcelas_extra = num_parcela_extra
				servico.valor_parcela_extra = v_parcela_extra
			servico.save()

		elif servico.numero_parcelas_extra > 0 and servico.numero_parcelas == 0:
			iden = servico.numero_parcelas_extra - 1
			parcela_extra = ParcelaExtra.objects.get(numero_parcela_extra = iden, servico = self.codigo_servico)
			servico.valor_total -= self.valor_pagamento
			if self.valor_pagamento < parcela_extra.valor_parcela_extra:
				parcela_extra.valor_parcela_extra -= self.valor_pagamento
				servico.valor_parcela_extra = parcela_extra.valor_parcela_extra
				parcela_extra.save()
			else:
				parcela_extra.delete()
				servico.numero_parcelas_extra -= 1
				if servico.numero_parcelas_extra > 0:
					iden = servico.numero_parcelas_extra - 1
					parcela_extra = ParcelaExtra.objects.get(numero_parcela_extra = iden, servico = self.codigo_servico)
					servico.valor_parcela_extra = parcela_extra.valor_parcela_extra
				else:
					servico.valor_parcela_extra = 0
		if servico.numero_parcelas_extra == 0 and servico.numero_parcelas == 0:
			servico.servico_pago()
		servico.save()
			

		
class ParcelaExtra(models.Model):
	numero_parcela_extra = models.IntegerField()
	valor_parcela_extra = models.DecimalField(max_digits = 10, decimal_places = 2)
	servico = models.CharField(max_length = 50)

	def __str__(self):
		return self.valor_parcela_extra

class Saldo(models.Model):
	codigo = models.IntegerField(primary_key = True, default = 1)
	codigo_cliente = models.ForeignKey(Cliente)

