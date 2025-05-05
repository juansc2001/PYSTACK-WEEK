from django.shortcuts import render, redirect
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
            print(request.user)#informa usuario que esta logado no momento
            usuario_logado = request.user
            print(usuario_logado)

            opcoes_estagio = Mentorados.escolhas
            navegators_do_user = navigator.objects.filter(usuario = usuario_logado)
            mentorados_do_mentor = Mentorados.objects.filter(usuario = usuario_logado)
            return render(request, 'mentorados.html', {'estagios': opcoes_estagio, 'navegators': navegators_do_user, 'mentorados' : mentorados_do_mentor})
        
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
