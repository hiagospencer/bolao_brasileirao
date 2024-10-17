from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.CharField(max_length=200, null=True, blank=True, unique=True)
    whatsapp = models.CharField(max_length=200, null=True, blank=True, unique=True)
    pagamento = models.BooleanField(default=False)
    imagem = models.ImageField(upload_to='imagens', default='imagens/perfil-null.png')

    def __str__(self):
        return f"Nome: {self.usuario}"



class Classificacao(models.Model):
    usuario = models.OneToOneField(Usuario, null=True, blank=True, on_delete=models.CASCADE)
    pontos = models.IntegerField(default=0)
    placar_exato = models.IntegerField(default=0)
    vitorias = models.IntegerField(default=0)
    empates = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.usuario} - {self.pontos}"


class Palpite(models.Model):
    usuario = models.OneToOneField(Usuario, null=True, blank=True, on_delete=models.CASCADE)
    rodada_atual = models.IntegerField(default=1)
    time_casa = models.CharField(max_length=50)
    placar_casa = models.IntegerField(default=0)
    time_visitante = models.CharField(max_length=50)
    placar_visitante = models.IntegerField(default=0)
    vencedor = models.CharField(max_length=50)
    finalizado = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.time_casa} x {self.time_visitante}"
