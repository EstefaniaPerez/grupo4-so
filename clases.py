class Proceso:
    def __init__(self, idProceso, tamanio, TA, TI):
        self.idProceso=idProceso
        self.tamanio=tamanio
        self.TA=TA
        self.TI=TI

class Particion:
    def __init__(self, idParticion, tamanio):
        self.idParticion=idParticion
        self.tamanio=tamanio
        self.dirInicio=hex(id(self))
        self.fragmentacion=0
        self.proceso=None

class Procesador:
    def __init__(self, unProceso):
        self.proceso=unProceso
        self.ocupado=False
        self.tiempoRestante=0




