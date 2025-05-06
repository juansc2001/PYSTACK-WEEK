from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from .models import Mentorados, navigator
from django.contrib import messages
from django.contrib.messages import constants
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
    return HttpResponse("pagina de abrir horarios")
