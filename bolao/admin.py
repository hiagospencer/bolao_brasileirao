from django.contrib import admin

from .models import *

class UsuarioAdmin(admin.ModelAdmin):
    model = Usuario
    list_display = ["usuario", "email", "whatsapp", "pagamento"]
    search_fields = ["usuario"]

class ClassificacaoAdmin(admin.ModelAdmin):
    model = Usuario
    list_display = ["usuario", "pontos"]
    search_fields = ["usuario"]


class PalpiteAdmin(admin.ModelAdmin):
    model = Palpite
    list_display = ["usuario","rodada_atual","time_casa", "placar_casa", "placar_visitante",  "time_visitante", "vencedor", "finalizado"]
    list_filter = ["usuario", "rodada_atual"]
    list_per_page = 10
    search_fields = ("usuario", "rodada_atual")

class RodadaOriginalAdmin(admin.ModelAdmin):
    model = RodadaOriginal
    list_display = ["rodada_atual","time_casa", "placar_casa", "placar_visitante",  "time_visitante", "vencedor", "finalizado"]
    list_filter = ["rodada_atual"]
    list_per_page = 10
    search_fields = ("usuario", "rodada_atual")


class RodadaAdmin(admin.ModelAdmin):
    model = Palpite
    list_display = ["rodada_atual","time_casa", "placar_casa", "placar_visitante",  "time_visitante"]
    list_filter = ["rodada_atual"]
    list_per_page = 10
    search_fields = ("rodada_atual",)




admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Classificacao, ClassificacaoAdmin)
admin.site.register(Palpite, PalpiteAdmin)
admin.site.register(RodadaOriginal, RodadaOriginalAdmin)
admin.site.register(Rodada, RodadaAdmin)
admin.site.register(Verificacao)
admin.site.register(BloquearPartida)
