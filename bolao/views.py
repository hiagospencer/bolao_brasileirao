

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import *
from .utils import validar_senha, utc_para_brasil
from .api_brasileirao import get_api_data


def homepage(request):
    usuarios = Classificacao.objects.filter(usuario__pagamento=True).order_by('-pontos', '-placar_exato', '-vitorias', '-empates')

    context = {'usuarios':usuarios}
    return render(request, 'index.html',context)



def palpites(request):
    data = get_api_data(31)
    context = {'jogos': data["matches"]}
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
