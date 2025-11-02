import datetime
import pickle as pkl
import os

qnt_mesas = [[] for _ in range(10)]  # 10 mesas

class Veiculo:
    def __init__(self, placa: str, dono: 'Cliente'):
        self.__placa = placa
        self.dono = dono
    
    def __str__(self):
        return f"Placa: {self.__placa}\nDono: {self.dono}"


class Cliente:
    def __init__(self, v, n):
        self.__nome = n
        self.veiculo = v
    
    def __str__(self):
        return f"Nome: {self.__nome}\nVeículo: \n{self.veiculo}"


class Reserva_Mesa:
    def __init__(self, cliente: 'Cliente', entrada: datetime.datetime, saida: datetime.datetime, mesa: int):
        self.cliente = cliente
        self.horario_de_entrada = entrada
        self.horario_de_saida = saida
        self.numero_mesa = mesa
        self.tem_veiculo = 1 if self.cliente.veiculo is not None else 0
        self.path = 'app/models/mesas.pkl'
        self.mesas = []
    
    def reservar_mesa(self):
        try:
            if os.path.exists(self.path):
                with open(self.path, 'rb') as a:
                    self.mesas = pkl.load(a)
            else:
                self.mesas = qnt_mesas
        except:
            self.mesas = qnt_mesas
        
        if self.numero_mesa > len(self.mesas) or self.numero_mesa <= 0:
            raise Exception("Mesa inválida.")
        
        # Checar conflitos de horário
        for i in range(0, len(self.mesas[self.numero_mesa - 1]), 2):
            if (self.horario_de_entrada < self.mesas[self.numero_mesa - 1][i + 1] and
                self.horario_de_saida > self.mesas[self.numero_mesa - 1][i]):
                raise Exception("Conflito de horário para esta mesa.")
        
        self.mesas[self.numero_mesa - 1].append(self.horario_de_entrada)
        self.mesas[self.numero_mesa - 1].append(self.horario_de_saida)
        
        with open(self.path, 'wb') as a:
            pkl.dump(self.mesas, a)
        
        return True

    def __str__(self):
        return f"Reserva na mesa: {self.numero_mesa}. Início: {self.horario_de_entrada} | Saída: {self.horario_de_saida}"