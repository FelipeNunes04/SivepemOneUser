from django.db import models

class Despesa(models.Model):
	gasolina = models.FloatField()
	comida = models.FloatField()
	outros = models.FloatField()
	data_despesa = models.DateField(auto_now_add = True)
