class Proceso:
    def __init__(self, idProceso, tamanio, TA, TI):
        self.idProceso=idProceso
        self.tamanio=tamanio
        self.TA=TA
        self.TI=TI

class Particion:
    def __init__(self, idParticion, tamanio, dirInicio):
        self.idParticion=idParticion
        self.tamanio=tamanio
        self.dirInicio=dirInicio
        self.fragmentacion=0
        self.proceso=None


