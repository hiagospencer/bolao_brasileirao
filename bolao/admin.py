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


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Classificacao, ClassificacaoAdmin)
admin.site.register(Palpite, PalpiteAdmin)
