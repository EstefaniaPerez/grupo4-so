from clases import Particion,Proceso
from tabulate import tabulate

class Simulador:
    particiones=list()
    procesos=list()

    def crearParticion(self):
        #hago asi nomas las particiones y procesos para probar que ande best-fit
        par1=Particion('pa1',60000,1) #como se haria para tener la dirInicio? porque en C estaba malloc para reservar memoria
        par2=Particion('pa2', 120000,1000)
        par3=Particion('pa3',250000, 3455)
        self.particiones.append(par1)
        self.particiones.append(par2)
        self.particiones.append(par3)

    def crearProceso(self):
        p1=Proceso('p1',60001,0,4)
        p2=Proceso('p2',120001,0,3)
        p3=Proceso('p3',26423,2,5)
        p4=Proceso('p4',1902,3,4)
        self.procesos.append(p1)
        self.procesos.append(p2)
        self.procesos.append(p3)
        self.asignarParticion(p1)
        self.asignarParticion(p3)
        self.desasignarParticion(p1)
        #self.asignarParticion(p2)
        self.asignarParticion(p1)
        self.asignarParticion(p4)

    def asignarParticion(self, unProceso):
        #se asigna particion de memoria utilizando tecnica best-fit
        i=0
        while(i<len(self.particiones)): #considerando que la lista de particiones esta ordenada de menor a mayor tamaño
            frag=self.particiones[i].tamanio-unProceso.tamanio
            if(frag>=0 and self.particiones[i].proceso is None): #particion de tamaño mayor o igual al proceso y sin proceso asignado
                self.particiones[i].proceso=unProceso
                self.particiones[i].fragmentacion=frag
                i=9999
            else:
                i=i+1
    
    def desasignarParticion(self, unProceso):
        i=0
        while(i<len(self.particiones)):
            if(unProceso==self.particiones[i].proceso ):
                self.particiones[i].proceso=None
                self.particiones[i].fragmentacion=0
                i=9999
            else:
                i=i+1

    def mostrarTablaParticiones(self):
        aux=Proceso('-',0,0,0)
        for i in range(len(self.particiones)):
            if(self.particiones[i].proceso is None):
                self.particiones[i].proceso=aux
        tabla=[ ['ID Particion', 'Dir Inicio Particion', 'Tamaño Particion', 'ID Proceso', 'Fragmentacion Interna'],
                [self.particiones[0].idParticion, self.particiones[0].dirInicio, self.particiones[0].tamanio, self.particiones[0].proceso.idProceso, self.particiones[0].fragmentacion],
                [self.particiones[1].idParticion, self.particiones[1].dirInicio, self.particiones[1].tamanio, self.particiones[1].proceso.idProceso, self.particiones[1].fragmentacion],
                [self.particiones[2].idParticion, self.particiones[2].dirInicio, self.particiones[2].tamanio, self.particiones[2].proceso.idProceso, self.particiones[2].fragmentacion]]
        print(tabulate(tabla, headers='firstrow', tablefmt='fancy_grid',stralign='center'))

        
        



s =Simulador()
s.crearParticion()
s.crearProceso()
s.mostrarTablaParticiones()


    

        