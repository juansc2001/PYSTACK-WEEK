from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from .models import Mentorados, navigator, disponibilidade_horario
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta
# Create your views here.

def mentorados(request):
    if  not request.user.is_authenticated:
        print('usuario nao esta logado')
        redirect('/usuarios/loguin')
    else:
        if request.method == "GET":
            usuario_logado = request.user
            print(usuario_logado)#informa usuario que esta logado no momento

            opcoes_estagio = Mentorados.escolhas
            navegators_do_user = navigator.objects.filter(usuario = usuario_logado)
            mentorados_do_mentor = Mentorados.objects.filter(usuario = usuario_logado)

            estagios_flat = []
            for i in opcoes_estagio:
                estagios_flat.append(i[1])
            print(estagios_flat)

            qtd_estagios = []
            for i, j in opcoes_estagio:
                quta_mentorados= Mentorados.objects.filter(estagio = i).filter(usuario = usuario_logado)
                qtd_estagios.append(quta_mentorados.count())
                print('-'*5)
            print(estagios_flat)
            print(qtd_estagios)

            return render(request, 'mentorados.html', {'estagios': opcoes_estagio, 'navegators': navegators_do_user, 'mentorados' : mentorados_do_mentor, 'estagio_flat': estagios_flat, 'qtd_estagios': qtd_estagios})
        
        elif request.method == 'POST':
            naame = request.POST.get('nome')
            foto_arquivo = request.FILES.get('foto')#request.files sempre que for acessar arqui
            estagio = request.POST.get('estagio')
            navegator_id = request.POST.get('navigator')
            navegador_obj = navigator.objects.get(id=navegator_id)

            mentorado = Mentorados(
                nome = naame,
                foto = foto_arquivo,
                estagio = estagio,
                navegador = navegador_obj, #nós ligamos a tabela navegator com foreignkey atravez do id da tabela
                usuario = request.user, #o mentor é o usuario que esta logado na aplicação
            )

            mentorado.save()#salva os dados da tabela no banco de dados 
            messages.add_message(request, constants.SUCCESS, 'mentorados cadastrados com sucesso')
            return redirect('/mentorados/')
        



def abrirhorarios(request):
    if request.method == "GET":
        return render(request, 'reunioes.html')
    elif request.method == "POST":
        data_string = request.POST.get('data')#coleta a data do formulario e guarda como uma string
        data = datetime.strptime(data_string, '%Y-%m-%dT%H:%M')#como nao é possivel fazer calculos com string função datetimestrptime faz uma conversao de string para datetime type 

        print(f"usuario: {request.user}")
        disponibilidades = disponibilidade_horario(
            data_inicial = data,
            mentor = request.user,
        )

        horarios_disponiveis = disponibilidade_horario.objects.filter(mentor = request.user).filter(
            #__gte signifca se é maior ou igual, ou seja, quando eu quero identificar se algo é maior ou igual eu utilizo __gte, se for apenas maior(>) usariamos __gt
            data_inicial__gte = data - timedelta( minutes=50 ),
            #__lte lessthan ou menor ou igual(>=)
            data_inicial__lte = data + timedelta( minutes = 50)
        )

        if horarios_disponiveis.exists():
            messages.add_message(request, constants.ERROR, 'Voce ja possui uma reuniao em aberto')
            return redirect('marcar_reunioes')

        disponibilidades.save()

        
        return HttpResponse(data)
    
