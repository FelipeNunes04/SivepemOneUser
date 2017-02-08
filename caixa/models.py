from django.db import models

class Caixa(models.Model):
	data = models.DateField(auto_now_add = True)
	dinheiroCaixa = models.FloatField()
	
		