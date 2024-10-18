import threading
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
import pandas as pd

from .models import *
from .utils import *
from .api_brasileirao import get_api_data


def homepage(request):
    user = request.user
    usuarios = Classificacao.objects.filter(usuario__pagamento=True).order_by('-pontos', '-placar_exato', '-vitorias', '-empates')

    calcular_pontuacao(user)
    context = {'usuarios':usuarios}
    return render(request, 'index.html',context)



def palpites(request):
    user = request.user
    rodadas = Rodada.objects.filter(rodada_atual=29)
    time_casa = []
    time_visitante = []
    rodada_dict = []
    placar_casa = []
    placar_visitante = []


    # adicionando os times casa e time visitantes dentros das lista para depois salvar no banco de dados
    for rodada in rodadas:
        time_casa.append(rodada.time_casa)
        time_visitante.append(rodada.time_visitante)

    if request.method == "POST":
        dados = request.POST
        resultados_form = dict(dados)


        if resultados_form["resultado_casa"] and resultados_form["resultado_visitante"]:
            for resultado_visitante in resultados_form["resultado_visitante"]:
                placar_visitante.append(resultado_visitante)

            for resultado_casa in resultados_form["resultado_casa"]:
                placar_casa.append(resultado_casa)

            for rodada in resultados_form["rodada_atual"]:
                rodada_dict.append(rodada)


        resultado_tabela = {
                "time_casa": time_casa,
                "placar_casa": placar_casa,
                "placar_visitante": placar_visitante,
                "time_visitante": time_visitante,
                "rodada_atual": rodada_dict
        }

        df_tabela = pd.DataFrame(resultado_tabela)
            # Iterar sobre o DataFrame e criar instâncias do modelo Rodada1
            #criando o banco de dados
        for _, row in df_tabela.iterrows():
            jogos_rodada_criado  = Palpite.objects.create(
                time_casa=row['time_casa'],
                placar_casa=row['placar_casa'],
                placar_visitante=row['placar_visitante'],
                time_visitante=row['time_visitante'],
                usuario=user,
                rodada_atual=row['rodada_atual'],
                )


    # thread = threading.Thread(target=criar_rodadas_campeonato)
    # thread.start()
    context = {"rodadas":rodadas}
    return render(request,'palpites.html', context)


def regras(request):
    return render(request,'regras.html')


def perfil(request):
    user = request.user
    usuarios = Usuario.objects.filter(usuario=user)

    if request.method == 'POST':
        dados = request.POST.dict()

        try:
            img = request.FILES['img']
        except KeyError:
            img = 'imagens/perfil-null.png'

        for usuario in usuarios:
            usuario.imagem = img
            usuario.save()

    context = {"usuarios":usuarios}
    return render(request, 'perfil.html', context)


def login_bolao(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        nome = request.POST.get('usuario')
        senha = request.POST.get('senha')
        usuario = authenticate(request,username=nome,password=senha)
        if usuario:
            #fazer login
            login(request,usuario)
            return redirect('homepage')
        else:
            messages.error(request, 'usuário ou senha inválidos!')
            return redirect('login_bolao')
    return render(request,'autenticacao/login_bolao.html')



def cadastro(request):

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        whatsapp = request.POST.get('whatsapp')
        senha = request.POST.get('senha')
        confirme_senha = request.POST.get('confirme_senha')

        if Usuario.objects.filter(nome=nome).exists():
            messages.error(request, 'Já existe um usuário cadastrado com esse nome.')
            return redirect('cadastro')

        validacao_senha = validar_senha(senha, confirme_senha)

        if validacao_senha == False:
            messages.error(request, "Senha inválida. A senha deve ter pelo menos 8 caracteres, uma letra maiúscula e um número.")
            return redirect('cadastro')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
            return redirect('cadastro')

        if Usuario.objects.filter(whatsapp=whatsapp).exists():
            messages.error(request, 'Número do Whatsapp já cadastrado')
            return redirect('cadastro')

        if len(whatsapp) < 15:
            messages.error(request, 'Número inválido! Tente novamente.')
            return redirect('cadastro')

         # Criar o usuário do Django
        user = User.objects.create_user(username=nome, email=email, password=senha)

         # Criar o objeto Usuario e associar o campo 'usuario' com o usuário logado
        usuario = Usuario.objects.create(usuario=user,nome=nome,email=email, whatsapp=whatsapp)

         # Criar o objeto Classificacao e associar ao Usuario criado
        classificacao = Classificacao.objects.create(usuario=usuario)

        login(request, user)  # Faz o login automático após o cadastro


        return redirect('homepage')  # Redireciona para a página inicial

    return render(request,'autenticacao/cadastro.html')


def fazer_logout(request):
    logout(request)
    return redirect('login_bolao')
