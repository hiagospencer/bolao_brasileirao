from django.urls import path
from .views import *

urlpatterns = [

    path('', homepage, name='homepage'),
    path('palpites', palpites, name='palpites'),
    path('meus-palpites', meus_palpites, name='meus_palpites'),
    path('regras', regras, name='regras'),
    path('perfil', perfil, name='perfil'),

    path('login', login_bolao, name='login_bolao'),
    path('cadastro', cadastro, name='cadastro'),
    path('logout', fazer_logout, name='logout'),
]
