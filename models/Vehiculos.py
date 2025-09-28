import math
from datetime import datetime

class Vehiculo:
    def __init__(self, placa, ingreso=None):
        self.placa = placa
        self.ingreso = ingreso or datetime.now()
        self.salida = None
        self.cobro = 0

    def calcular_cobro(self, tarifa):
        self.salida = datetime.now()
        horas = (self.salida - self.ingreso).total_seconds() / 3600
        self.cobro = math.ceil(horas) * tarifa
        return self.cobro


class Carro(Vehiculo):
    tarifa = 3000  # pesos por hora

    def calcular_cobro(self):
        return super().calcular_cobro(Carro.tarifa)


class Moto(Vehiculo):
    tarifa = 1000  # pesos por hora

    def calcular_cobro(self):
        return super().calcular_cobro(Moto.tarifa)
