import threading
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
import pandas as pd

from .models import *
from .utils import *
from .api_brasileirao import get_api_data


def homepage(request):
    if request.user.is_authenticated:
        user = request.user
        usuarios = Classificacao.objects.filter(usuario__pagamento=True).order_by('-pontos', '-placar_exato', '-vitorias', '-empates')

        # thread = threading.Thread(target=calcular_pontuacao(user))
        # thread.start()


        context = {'usuarios':usuarios}
        return render(request, 'index.html',context)
    else:
        user = request.user
        usuarios = Classificacao.objects.filter(usuario__pagamento=True).order_by('-pontos', '-placar_exato', '-vitorias', '-empates')

        context = {'usuarios':usuarios}
        return render(request, 'index.html',context)


def palpites(request):

    if request.user.is_authenticated:
        user = request.user
        time_casa = []
        time_visitante = []
        rodada_dict = []
        placar_casa = []
        placar_visitante = []
        img_casa = []
        img_visitante = []
        verificacao_partida, criado = Verificacao.objects.get_or_create(user=user)
        rodadas = Rodada.objects.filter(rodada_atual=verificacao_partida.partida_atual )
        # calcular_pontuacao(user)

        if verificacao_partida.partida_atual == verificacao_partida.partida_final:
            verificacao_partida.verificado = True
            verificacao_partida.save()

        # adicionando os times casa e time visitantes dentros das lista para depois salvar no banco de dados
        for rodada in rodadas:
            time_casa.append(rodada.time_casa)
            time_visitante.append(rodada.time_visitante)
            img_casa.append(rodada.imagem_casa)
            img_visitante.append(rodada.imagem_fora)

        if request.method == "POST":
            # data = get_api_data(verificacao_partida.partida_atual)
            dados = request.POST
            resultados_form = dict(dados)


            # #salvando os emblemas dos times no banco de dados
            # for jogo in data["matches"]:
            #     img_casa.append(jogo['homeTeam']['crest'])
            #     img_visitante.append(jogo['awayTeam']['crest'])



            #salvando os resultados dos times e rodadas no banco de dados
            if resultados_form["resultado_casa"] and resultados_form["resultado_visitante"]:
                for resultado_visitante in resultados_form["resultado_visitante"]:
                    placar_visitante.append(resultado_visitante)

                for resultado_casa in resultados_form["resultado_casa"]:
                    placar_casa.append(resultado_casa)

                for rodada in resultados_form["rodada_atual"]:
                    rodada_dict.append(rodada)


            resultado_tabela = {
                    "time_casa": time_casa,
                    "img_casa": img_casa,
                    "placar_casa": placar_casa,
                    "placar_visitante": placar_visitante,
                    "time_visitante": time_visitante,
                    "img_visitante": img_visitante,
                    "rodada_atual": rodada_dict
            }

            print(resultado_tabela['time_casa'])
            print(resultado_tabela['img_casa'])

            df_tabela = pd.DataFrame(resultado_tabela)


                # Iterar sobre o DataFrame e criar instâncias do modelo Rodada1
                #criando o banco de dados
            for _, row in df_tabela.iterrows():
                jogos_rodada_criado  = Palpite.objects.create(
                    time_casa=row['time_casa'],
                    imagem_casa=row['img_casa'],
                    placar_casa=row['placar_casa'],
                    placar_visitante=row['placar_visitante'],
                    time_visitante=row['time_visitante'],
                    imagem_fora=row['img_visitante'],
                    usuario=user,
                    rodada_atual=row['rodada_atual'],
                    )

            verificacao_partida.partida_atual += 1
            verificacao_partida.save()
            return redirect('palpites')

        context = {"rodadas":rodadas, 'verificacao_partida':verificacao_partida.verificado}
        return render(request,'palpites.html', context)
    else:
        return redirect('login_bolao')


def meus_palpites(request):
    if request.user.is_authenticated:
        user = request.user
        rodadas = Palpite.objects.filter(usuario=user)
        #pagination
        paginator = Paginator(rodadas, 10)
        page_obj = request.GET.get('page')
        posts = paginator.get_page(page_obj)

        context = {'posts':posts, 'rodadas':rodadas}
        return render(request,'meus_palpites.html', context)
    else:
        return redirect('login_bolao')

def regras(request):
    return render(request,'regras.html')

@user_passes_test(lambda u: u.is_superuser)
def configuracoes(request):
    user = request.user


    if request.method == 'POST':
        rodada_inicial = request.POST.get('rodada_inicial')
        rodada_final = request.POST.get('rodada_final')
        rodada_original = request.POST.get('rodada_original')
        apagar_rodada = request.POST.get('apagar_rodada')
        criar_rodadas = request.POST.get('criar_rodadas')
        resetar_pontuacao = request.POST.get('resetar_pontuacao')
        bloquear_partidas = request.POST.get('bloquear_partidas')
        desbloquear_partidas = request.POST.get('desbloquear_partidas')
        zerar_palpites = request.POST.get('zerar_palpites')
        atualizar_classificacao = request.POST.get('atualizar_classificacao')

        if zerar_palpites:
            thread = threading.Thread(target=zerar_palpites_usuarios(zerar_palpites))
            thread.start()

        if atualizar_classificacao:
            thread = threading.Thread(target=calcular_pontuacao_usuario())
            thread.start()

        if rodada_original:
            thread = threading.Thread(target=salvar_rodada_original(rodada_original))
            thread.start()

        if apagar_rodada:
            RodadaOriginal.objects.filter(rodada_atual=apagar_rodada).delete()

        if resetar_pontuacao:
            thread = threading.Thread(target=resetar_pontuacao_usuarios())
            thread.start()

        if bloquear_partidas:
            bloquear = Verificacao.objects.all()
            for partida in bloquear:
                partida.verificado = True
                partida.save()

        if desbloquear_partidas:
            bloquear = Verificacao.objects.all()
            for partida in bloquear:
                partida.verificado = False
                partida.save()

        if criar_rodadas:
            if Rodada.objects.exists():
                messages.error(request, 'Rodadas campeonato já foram criadas!')
                return redirect('configuracoes')
            else:
                thread = threading.Thread(target=criar_rodadas_campeonato())
                thread.start()
                print("Rodadas Criadas com sucesso!")

        else:
            print("Checkbox desativo")


        # verificando se tem rodadas no inputs e salvando no banco de dados
        if rodada_inicial and rodada_final:
            if int(rodada_inicial) >= int(rodada_final) or int(rodada_final) > 39:
                messages.error(request, 'A rodada inicial não pode ser maior ou igual que a rodada final. Rodada final não poede ser maior que 38')
                return redirect('configuracoes')
            else:
                setar_rodadaAtual_rodadaFinal(rodada_inicial, rodada_final)
                print('Rodadas setadas!')
        else:
            messages.error(request, 'Campos rodadas vazios!')
            return redirect('configuracoes')

    return render(request,'configuracoes.html')


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

        if senha != confirme_senha:
            messages.error(request, "Senha inválida. senhas são diferentes")
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
