import csv
from clases import Particion, Proceso, Procesador
from tabulate import tabulate

class Simulador:
    particiones=list()
    colaNuevos=list()
    colaListos=list()
    procesador=Procesador(None)
    t=-1

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
                            self.colaNuevos.append(Proceso(linea[0], int(linea[1]), int(linea[2]), int(linea[3])))
                            i=i+1 #las lineas que dan error no se cuentan o tendrian que contar??
                        else:
                            print('Error: Proceso ', linea[0], 'supera tamanio de particiones existentes')
                else:
                    print("Se supero maximo numero de procesos. Se leyeron los 10 primeros.")
                    break

        self.colaNuevos.sort(key=lambda x: x.TA) #ordena por TA--> planificador a largo plazo
        archivo.close()
        

    def asignarParticion(self, unProceso):
        #se asigna particion de memoria utilizando tecnica best-fit
        i=0
        while(i<len(self.particiones)): #considerando que la lista de particiones esta ordenada de menor a mayor tamaño
            frag=self.particiones[i].tamanio-unProceso.tamanio
            if(frag>=0 and self.particiones[i].proceso is None): #particion de tamaño mayor o igual al proceso y sin proceso asignado
                self.particiones[i].proceso=unProceso
                self.particiones[i].fragmentacion=frag
                return True
            else:
                i=i+1
        return False  #si recorrio todas las particiones y ninguna puede alojar al proceso, devuelve f
    
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
        print("Tabla de Particiones")
        for i in range(len(self.particiones)):
            if(self.particiones[i].proceso is None):
                self.particiones[i].proceso=aux
        tabla=[ ['ID Particion', 'Dir Inicio Particion', 'Tamaño Particion', 'ID Proceso', 'Fragmentacion Interna'],
                [self.particiones[0].idParticion, self.particiones[0].dirInicio, self.particiones[0].tamanio, self.particiones[0].proceso.idProceso, self.particiones[0].fragmentacion],
                [self.particiones[1].idParticion, self.particiones[1].dirInicio, self.particiones[1].tamanio, self.particiones[1].proceso.idProceso, self.particiones[1].fragmentacion],
                [self.particiones[2].idParticion, self.particiones[2].dirInicio, self.particiones[2].tamanio, self.particiones[2].proceso.idProceso, self.particiones[2].fragmentacion]]
        print(tabulate(tabla, headers='firstrow', tablefmt='fancy_grid',stralign='center'))

    def salida(self):
        print("\n---------------------------------------------------------------")
        print("\nEstado del Procesador:")
        print("     Proceso ejecutandose en tiempo=",self.t, ": ", self.procesador.proceso.idProceso ,"\n")
        self.mostrarTablaParticiones()
        print("\nEstado de la Cola de Listos:")
        for i in self.colaListos:
          print("   Proceso:", i.idProceso, ". Tamanio:", i.tamanio, ". Tiempo de Arribo:", i.TA,  ". Tiempo de Irrupcion:", i.TI)
        print("\n---------------------------------------------------------------")


    
    def ordenarColaListos(self):
        i=0
        #print("\n t:", self.t,". proceso:", self.colaNuevos[i].idProceso,"\n")
        while (self.colaNuevos and i<len(self.colaNuevos)) : #mientras haya procesos con TA <= t actual en colaNuevos
            if(self.colaNuevos[i].TA<=self.t and self.asignarParticion(self.colaNuevos[i])) : #si a ese proceso se le puede asignar alguna particion
                self.colaListos.append(self.colaNuevos[i])
                self.colaNuevos.pop(i) 
            else:
                i=i+1
        self.colaListos.sort(key=lambda x: x.TI) #ordena por TI a la cola de listos


    def planificar(self):
        while (self.colaNuevos or self.colaListos): #hacer mientras haya procesos nuevos o listos
            self.t=self.t+1
            

            if(self.procesador.ocupado): #si hay algun proceso ejecutandose, se decrementa su tiempo restante en cpu
                self.procesador.tiempoRestante=self.procesador.tiempoRestante-1
                if(self.procesador.tiempoRestante==0): #si se termino tiempo I de proceso se lo saca del procesador
                    self.procesador.ocupado=False
                    self.desasignarParticion(self.procesador.proceso)
                    self.procesador.proceso=None

            self.ordenarColaListos()  #en cada tiempo t actual ordena la cola de listos

            if (not self.procesador.ocupado and self.colaListos):  
                #si el procesador no esta ocupado y hay procesos listos, ejecuta el siguiente con menor TI en cola de listos
                self.procesador.ocupado=True
                self.procesador.proceso=self.colaListos[0] 
                self.procesador.tiempoRestante=self.colaListos[0].TI
                self.colaListos.pop(0)
                self.salida()  #Las presentaciones de salida deberán realizarse cada vez que llega un nuevo proceso-->se refiere a cada que ingresa un proceso a CPU?
        
            
        

        



s=Simulador()
s.crearParticiones()
s.ingresarProcesos()
s.planificar()


    

        