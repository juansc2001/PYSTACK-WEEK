from django.db import models
from django.contrib.auth.models import User #aqui eu importo a tabela User para que eu possa fazer uma relação entre as tabelas com o ForeignKey
from datetime import timedelta #biblioteca timedelta cria intervalos de tempo
import secrets 

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

    token = models.CharField(max_length=16)


    def save(self, *args, **kwargs): 
    #a classe mentorados já possui um metodo save que foi herdado e quando criamos outro metodo com o nome igual, na hora usamos o metodo a prioridade é o da classe que estamos e nao o que foi herdado



        #se nao houver um token salve um
        if not self.token :
                
            self.token = self.gerar_token_unico()

            super().save(*args, **kwargs)#para usarmos o metodo da classe mae usamos o super() que nesse caso ira usar o metodo save() da classe Model 
            #agora oque esta acontecendo é que chamamos este metodo save nas views e nosso metodo vai chamar o metodo save() da classe mae que realmente salva os dados. Agora podemos acrescentar novas funções para o metodo save sem nos preocuparmos com funcionalidades anteriores.

    def gerar_token_unico(self):
         while True:#enquanto não for gerado um token unico o loop ira ocorrer
              tooken = secrets.token_urlsafe(8)#gera um token ou 16 caracteres de forma aleatoria
              if not Mentorados.objects.filter(token = tooken).exists() : #checa se o token que foi gerado ja é existente, se não existir retorna o valor da função o token
                   return tooken
                     



    def __str__(self):
        return f" mentorado: {self.nome} usuario: {self.usuario} {self.navegador}"
    


class disponibilidade_horario(models.Model):
    data_inicial = models.DateTimeField(null = True, blank=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    agendado = models.BooleanField(default=False)
    #nao ah necessidade de guardar no banco de dados a datafinal, pois sera sempre 50m depois da data inicial

    def data_final(self): #função que pega a data inicial e soma 50 minutos
        return self.data_inicial + timedelta(minutes=50)

        


