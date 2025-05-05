from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate #recebe as credencias do usuario e identifica se os dados ja existem no banco de dados
from django.contrib.auth import login #inicia uma seção, (ele nao explicou muito)

from django.contrib.messages import constants
from django.contrib import messages
# Create your views here.

def cadastro(request):
    if request.method == 'GET' :
        return render(request, 'cadastro.html')
    
    
    elif request.method == 'POST' :
        usuario = request.POST.get('username')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirmar_senha')

        if senha != confirma_senha:
            messages.add_message(request, constants.ERROR, 'senha e confirmar senha deve ser iguais')
            return redirect( '/usuarios/cadastro/' )
        if len(senha) <= 6 :
            messages.add_message(request, constants.ERROR, 'a senha deve ter mais de 6 digitos')
            return redirect('/usuarios/cadastro/')


        users = User.objects.filter(username = usuario)#vai buscar se o valor usuario existe na tabela usuarios, se houver, vai guardar o valor em users
        print(users.exists()) # a função exists retorna se existe algum dado dentro da variavel e returna um valor boolleano 

        if users.exists() == True :
            messages.add_message(request, constants.ERROR, 'ja existe um usuario com este user name')
            return redirect('/usuarios/cadastro/')

        User.objects.create_user(#essa função sempre precisa de obrigatoriamente dois dados user e password
            #tanto a variavel usuario quando password precisao ter o mesmo nome caso contrario vai dar erro
            username = usuario,
            password = senha
        )
        return redirect('/usuarios/loguin/')
    



def loguin(request):

    if request.method == 'GET' :
        return render(request, 'loguin.html')
    
    elif request.method == 'POST':
        
        usuario = request.POST.get('username')
        senha = request.POST.get('senha')

        #autentica o usuario, ou seja, verifica se o usuario e a senha existem no banco de dados na tabela users
        user = authenticate(request, username=usuario, password=senha)#<< O metodo authenticate verifica a existencia dos dados do banco de dados, se existir ele retorna o nome do usuario, se nao existir ele retorna none
        print(user)

        if user != None:
            print(f'{user} logou')
            login(request, user)
            return redirect('/mentorados/')
        elif user == None:
            print(f'usuario nao existe, {user}')
            messages.add_message(request, constants.ERROR, 'usuario nao encontrado.')
            return redirect('/usuarios/loguin/')
