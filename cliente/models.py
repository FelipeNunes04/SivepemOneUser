from django.db import models

class Cliente(models.Model):
	codigo = models.CharField("Código",max_length = 20,  primary_key=True)
	nome = models.CharField(max_length = 50)
	cpf = models.ImageField(upload_to = 'cpfs')
	telefone = models.CharField(max_length = 20)
	endereco = models.CharField(max_length = 70)
	limite = models.FloatField()
	devendo = models.BooleanField(default = False)

	def pagar(self):
		self.devendo = False
		self.save()

	def __str__(self):
		return self.codigo