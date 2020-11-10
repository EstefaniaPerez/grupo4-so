import csv
from clases import Particion,Proceso
from tabulate import tabulate

class Simulador:
    particiones=list()
    procesos=list()

    def crearParticiones(self):
        so=Particion('so', 100000)
        par1=Particion('pa1',60000) 
        par2=Particion('pa2', 120000)
        par3=Particion('pa3',250000)
        self.particiones.append(par1)
        self.particiones.append(par2)
        self.particiones.append(par3)

    def ingresarProcesos(self):
        i=0
        with open("/Users/ESTEFANIA/Documents/GitHub/grupo4-so/archivo.csv") as archivo:
            entrada = csv.reader(archivo, skipinitialspace=True, strict=True)
            next(entrada, None) #ignora la cabecera
            for linea in entrada:
                if not (linea): #saltea lineas vacias
                    continue
                if(i<10): #maximo 10 procesos
                    linea.extend((None,None,None)) 
                    if(linea[1] is None) or (linea[2] is None) or (linea[3]is None): #si a un proceso le falta tamanio,TA, o TI da error
                        print('Error: a Proceso ', linea[0], 'le falta datos')
                    else:
                        if(int(linea[1])<=250000): #si el tamanio es menor o igual a la particion mas grande
                            self.procesos.append(Proceso(linea[0], linea[1], linea[2], linea[3]))
                            i=i+1 #las lineas que dan error no se cuentan o tendrian que contar??
                        else:
                            print('Error: Proceso ', linea[0], 'supera tamanio de particiones existentes')
                else:
                    print("Se supero maximo numero de procesos. Se leyeron los 10 primeros.")
                    break

        self.procesos.sort(key=lambda x: x.TA) #ordena por TA, como ordenar si TA de 2 procesos son iguales??
        archivo.close()
        #for i in self.procesos:
        #    print(i.idProceso, i.tamanio, i.TA, i.TI)

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

        
        



s=Simulador()
s.crearParticiones()
s.ingresarProcesos()
s.mostrarTablaParticiones()


    

        