import datetime
import pickle as pkl
qnt_mesas=[]
for i in range(10):
    qnt_mesas.append([])

class Veiculo():
    def __init__(self,placa:str,dono:'Cliente'):
        self.__placa=placa
        self.dono=dono
    
    def __str__(self):
        return f"Placa: {self.__placa}\nDono: {self.dono}"

class Cliente():
    def __init__(self,v,n):
        self.__nome=n
        self.veiculo=v
    
    def __str__(self):
        return f"Nome: {self.__nome}\nVeículo: \n{self.veiculo}"

class Reserva_Mesa():
    def __init__(self,cliente:'Cliente',entrada:datetime,saida:datetime,mesa:int):
        self.cliente=cliente
        self.horario_de_entrada=entrada
        self.horario_de_saida=saida
        self.numero_mesa=mesa
        self.tem_veiculo=1 if self.cliente.veiculo is not None else 0
        self.path='mesas'
        self.mesas=[]
        self.abertura=datetime.datetime.strptime('11','%H')
        self.fechamento=datetime.datetime.strptime('23','%H')
    
    def reservar_mesa(self):
        try:
            with open(self.path,'rb') as a:
                self.mesas=pkl.load(a)
        except:
            print("Sem mesas reservadas.")
            self.mesas=qnt_mesas
        try:
            self.mesas[self.numero_mesa]
        except:
            print("Mesa não reservada ainda.")
        if self.horario_de_entrada-self.horario_de_saida>=datetime.timedelta(0) or int(self.horario_de_entrada.hour)<=int(self.abertura.hour) or int(self.horario_de_saida.hour)>=int(self.fechamento.hour):
            print("Arrume o horário")
            return -1
        try:
            for i in range(0,len(self.mesas[self.numero_mesa-1]),2):
                if self.horario_de_saida>=self.mesas[self.numero_mesa-1][i] and self.horario_de_saida<=self.mesas[self.numero_mesa-1][i+1]:
                    raise Exception("Não pode reservar essa mesa nesse dia e horário.")
                if self.horario_de_entrada>=self.mesas[self.numero_mesa-1][i] and self.horario_de_entrada<=self.mesas[self.numero_mesa-1][i+1]:
                    raise Exception("Não pode reservar essa mesa nesse dia e horário.")
        except Exception as e:
            print(e)
            return 0

        self.mesas[self.numero_mesa-1].append(self.horario_de_entrada)
        self.mesas[self.numero_mesa-1].append(self.horario_de_saida)
        with open(self.path,'wb') as a:
            pkl.dump(self.mesas,a)
        print(self.mesas)

    def __str__(self):
        return f"Reserva na mesa: {self.numero_mesa}.\nInicio: {self.horario_de_entrada}\nSaída: {self.horario_de_saida}"