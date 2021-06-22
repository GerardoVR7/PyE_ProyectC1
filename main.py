import statistics as st
import tkinter
from pandas.core.frame import DataFrame
from scipy import stats
import scipy
import xlrd 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter 
import numpy as np
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import math



window = tkinter.Tk()
window.geometry("250x200")
label = tkinter.Label(window, text="Visualizador de Graficas").pack(side=TOP)
def ventana2():
    window2 = tkinter.Tk()
    window2.geometry("750x700")
    def mostrarDatosContinuos():
        table1 = Text(window2)
        table1.insert(INSERT,DFgeneral.to_string())
        table1.pack()
        table1.place(x=30, y=140,height=195, width=650)

    def mostrarDatosDiscretos():
        calculos.createDataDiscreet(arrayHoras_Ejercicio)
        table1 = Text(window2)
        table1.insert(INSERT,DF_Discretos.to_string())
        table1.pack()
        table1.place(x=30, y=350,height=140, width=300)

    def mostrarDatosCualitativos():
        table1 = Text(window2)
        table1.insert(INSERT,DF_Estatus.to_string())
        print(DF_Estatus)
        table1.pack()
        table1.place(x=30, y=500,height=100, width=300)
    
    Button(window2, text="Generar graficas", command= archivo.generateGraficPie). pack(side=TOP)
    Button(window2, text="Mostrar tabla de datos continuos", command= lambda: mostrarDatosContinuos() ).pack(side=TOP)
    Button(window2, text="Mostrar tabla de datos discretos", command= lambda: mostrarDatosDiscretos() ).pack(side=TOP)
    Button(window2, text="Mostrar tabla de datos cualitativos", command= lambda: mostrarDatosCualitativos() ).pack(side=TOP)



def close_window(window):
    window.destroy()

class graphicFile:
    
    buscado = ""

    def openFile(self):
        global df
        global arrayPeso
        global arrayHoras_Ejercicio
        global arrayIMC
        
        arrayHoras_Ejercicio = None
        arrayPeso = None
        arrayIMC = None
        df = None
        file = filedialog.askopenfilename(title = "abrir", initialdir=r"C:\\", filetypes=(("Archivos CSV" , "*.csv") , ("Archivos de texto", "*.txt")))
        self.buscado = file
        print(self.buscado)
        
        df= pd.read_csv(self.buscado)
        arrayPeso = np.array(df['Peso_Kg'].sort_values())
        arrayHoras_Ejercicio = np.array(df['Dias_de_Ejercicio'].sort_values())
        arrayIMC = np.array(df['IMC'].sort_values())
        calculos.createQualitativeData(arrayIMC)
        calculos.createClass(arrayPeso)
        print(arrayIMC)
        


    def generateGraficPie(self):
        
        plt.plot(DFgeneral['Marca de clase'], DFgeneral['Frec Absoluta'])
        plt.title('Grafica de poligono')
        plt.xlabel('Marca de clase')
        plt.ylabel('Frecuencia')
        plt.show()
        
        df.groupby ("Edad") ["Dias_de_Ejercicio"].mean().plot(kind='bar',legend='Reverse' )
        plt.title('Grafica de barras')
        plt.ylabel('Dias de ejercicio')
        plt.show()

        DF_Estatus.Cantidad.groupby(DF_Estatus.Estatus).sum().plot(kind='pie' , cmap= 'Paired', autopct='%1.1f%%')  
        plt.axis('equal')
        plt.show()

class Calculos:

    rangoMayor = 0
    rangoMenor = 0
    rango = 0
    numClass = 0.0
    widthClass = 0
    classMark = 0
    frecAbs = 1
    freRel = 0
    auxMayor = 0

    list_numClass = []
    list_limtMayor = []
    list_limtMenor = []
    list_widthClass = []
    list_classMark = []
    list_frecAbs = []
    list_freRel = []
    list_rango = []


    

    def createClass(self , array):

        self.rangoMayor = df['Peso_Kg'].max()
        self.rangoMenor = df['Peso_Kg'].min()
        print(self.rangoMenor)
        print(self.rangoMayor)
        self.rango = self.rangoMayor - self.rangoMenor
        self.numClass = math.ceil(1 + (3.3 * math.log10(len(array))))
        print( len(array))
        print(self.numClass)
        self.widthClass = (round(self.rango / self.numClass))
        limiteMenor = self.rangoMenor
        print(self.widthClass)

        self.list_limtMenor.append("")
        self.list_limtMayor.append("")
        self.list_classMark.append(limiteMenor)
        self.list_frecAbs.append(0)
        self.list_freRel.append(0)


        for i in range(self.numClass):

            limiteMayor = limiteMenor + self.widthClass
            self.auxMayor = limiteMayor
            self.list_limtMenor.append(limiteMenor)
            self.list_limtMayor.append(limiteMayor)
            marca = 0.0
            marca = (limiteMenor + limiteMayor)/2
            self.list_classMark.append(marca)
            for y in range(len(array)):
                arraytotal = array[y]
                #self.frecAbs = df.loc[(df.Peso_Kg >= limiteMenor) & (df.Peso_Kg <= limiteMayor)  ].agg(frecuency= ("Peso_Kg" , "count"))
                if (arraytotal > limiteMenor and arraytotal <= limiteMayor): 
                    self.frecAbs = self.frecAbs + 1
                    self.freRel = (self.frecAbs * 100) /len(array)

            self.list_frecAbs.append(self.frecAbs)

            self.list_freRel.append(round(self.freRel,2))
            self.frecAbs = 0
            self.freRel = 0 

            limiteMenor = limiteMayor
        self.list_classMark.append(self.auxMayor)
        self.list_frecAbs.append(0)

        Lim_Menor=pd.DataFrame(self.list_limtMenor,columns=['Lim Menor'])
        Lim_Mayor=pd.DataFrame(self.list_limtMayor,columns=['Lim Mayor'])
        Marca_clases=pd.DataFrame(self.list_classMark,columns=['Marca de clase'])
        frecuencia_Absoluta=pd.DataFrame(self.list_frecAbs,columns=['Frec Absoluta'])
        frecuencia_Relativa=pd.DataFrame(self.list_freRel,columns=['Frec Relativa'])

        global DFgeneral
        DFgeneral = None
        DFgeneral=pd.concat([Lim_Menor,Lim_Mayor,Marca_clases,frecuencia_Absoluta,frecuencia_Relativa],axis=1)

    lis_encabezados = ["Media Geometrica:", "Media Aritmetica:", "Media truncada:" , "Mediana:", "Moda:", "Varianza:" , "Desviacion:"]
    list_datosDiscretos = []

    def createDataDiscreet(self,array):
        sesgo = ""
        #statistics
        #print('Media geometrica:' ,st.geometric_mean(array))
        print('Media geometrica:' , array.prod()**(1.0/len(array)))
        media_geometrica = array.prod()**(1.0/len(array))
        self.list_datosDiscretos.append(media_geometrica)
        print('Media aritmetica:' , array.mean())
        media_aritmetica = array.mean()
        self.list_datosDiscretos.append(media_aritmetica)
        #scipy
        print('Media truncada:' ,stats.trim_mean(array, .10))
        media_truncada = stats.trim_mean(array, .10)
        self.list_datosDiscretos.append(media_truncada)
        #statistic
        print('Mediana:' ,st.median(array))
        mediana =st.median(array)
        self.list_datosDiscretos.append(mediana)
        print('Moda:' , st.mode(array))
        moda = st.mode(array)
        self.list_datosDiscretos.append(moda)
        print("Varianza:" , array.var())
        variaza = array.var()
        self.list_datosDiscretos.append(variaza)
        print("Desviacion:" , array.std())
        desviacion = array.std()
        self.list_datosDiscretos.append(desviacion)

        encabezados = pd.DataFrame(self.lis_encabezados, columns=['Calculos'])
        datosD = pd.DataFrame(self.list_datosDiscretos, columns=['Datos'])
        
        global DF_Discretos
        DF_Discretos = None
        DF_Discretos = pd.concat([encabezados,datosD], axis=1)
        print(DF_Discretos)

        if (media_aritmetica > mediana > moda):
            sesgo = "Sesgado a la izquierda"
        elif(media_aritmetica == mediana == moda):
            sesgo = "Sesgado simetrico"
        elif(moda < mediana < media_aritmetica):
            sesgo = "Sesgado a la derecha"
        print("Sesgo:" , sesgo)

    limBP = 18.5
    #medida de bajo peso en el rango del IMC
    limPN = 24.9
    #medida de peso normal en el rango del IMC
    limSP = 29.9
    #medida de sobre peso en el rango del IMC
    list_estatus = ["Anemia", "Peso normal", "Sobrepeso", "Obesidad"]
    list_cantidad = []

    def createQualitativeData(self, array):
        self.limInfPeso = df['IMC'].min()
        estatusAnemia = 0
        estatusPesoN = 0
        estatusSobrepeso =0
        estatusObesidad = 0
        for i in range(len(array)):

            dato = array[i]

            if(dato < self.limBP):
                estatusAnemia = estatusAnemia + 1
            elif (dato >= self.limBP and dato <= self.limPN):
                estatusPesoN = estatusPesoN + 1
            elif( dato >= self.limPN and dato <= self.limSP):
                estatusSobrepeso = estatusSobrepeso + 1
            elif (dato > self.limSP):
                estatusObesidad = estatusObesidad + 1
        
        self.list_cantidad.append(estatusAnemia)
        self.list_cantidad.append(estatusPesoN)
        self.list_cantidad.append(estatusSobrepeso)
        self.list_cantidad.append(estatusObesidad)
        totalEstatus = pd.DataFrame(self.list_estatus, columns=['Estatus'])
        cantidad = pd.DataFrame(self.list_cantidad, columns=['Cantidad'])

        global DF_Estatus
        DF_Estatus = None
        DF_Estatus = pd.concat([totalEstatus,cantidad], axis=1)


calculos = Calculos()
archivo = graphicFile()

Button(window, text="Seleccionar archivo" ,command=lambda:[archivo.openFile(),ventana2(),close_window(window)]).pack()
window.mainloop()