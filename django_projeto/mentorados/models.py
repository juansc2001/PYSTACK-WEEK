from django.db import models
from django.contrib.auth.models import User #aqui eu importo a tabela User para que eu possa fazer uma relação entre as tabelas com o ForeignKey

# Create your models here.
class navigator(models.Model):#navigator sao pessoas que trabalhao junto ao mentor
    nome = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,)

    def __str__(self):
        return f" navagator: {self.nome} mentor: {self.usuario}"

class Mentorados(models.Model):
    escolhas = (
    ('estagio1', '10-100'),
    ('estagio2', '100-1000'),
    )
    
    nome = models.CharField( max_length= 200)
    data_de_criação = models.DateField(auto_now_add= True) #auto_now_add= True automaticamente salva com a data que o objeto foi criado.
    foto = models.ImageField( upload_to='fotos', null=True, blank= True)  #upload_to='' indica em qual pasta o django vai salvar as imagens
    estagio = models.CharField(choices= escolhas) #choices='' faz com que o usuario possa apenas colocar determinados tipos de opções no banco de dados

    #mentor
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, ) # o primeiro parametro esta relacioando a tabela aos User, ou seja, cada User vai ser responsavel por um objeto ou tabela do mentorados.
    # on_delete=models.CASCADE indica que quando um usuario relacionado a tabela for excluido ou deletado do banco de dados, todas as tabelas que estao relacionadas a esse usuario serao deletadas
    navegador = models.ForeignKey(navigator, null=True, blank= True, on_delete= models.CASCADE )

    def __str__(self):
        return f" mentorado: {self.nome} usuario: {self.usuario} {self.navegador}"


