from django.urls import path
from django.contrib.auth import views
from .views import *

urlpatterns = [

    path('', homepage, name='homepage'),
    path('palpites', palpites, name='palpites'),
    path('meus-palpites', meus_palpites, name='meus_palpites'),
    path('regras', regras, name='regras'),
    path('configuracoes', configuracoes, name='configuracoes'),
    path('perfil', perfil, name='perfil'),

    path('login', login_bolao, name='login_bolao'),
    path('cadastro', cadastro, name='cadastro'),
    path('logout', fazer_logout, name='logout'),

    # reset senha
    path("password_change/", views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
