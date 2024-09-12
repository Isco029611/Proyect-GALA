import pandas as pd 
import MetaTrader5 as mt5 


nombre=501049257
clave= "I@6yTfWk"
server= "RoboForex-Pro"
path = r'C:\Program Files\RoboForex MT5 Terminal\terminal64.exe'


#Se necesita version numpy version:  1.26, codigo: pip install numpy<2
mt5.initialize(login=nombre,password=clave,server=server,path=path)
rates= mt5.copy_rates_from_pos("TSLA",mt5.TIMEFRAME_H1,0,999)
tabla= pd.DataFrame(rates)
tabla['time'] = pd.to_datetime(tabla['time'], unit = 's')
#Si quiero ver datos del principio del dataframe, utilizo metodo: .head( cuantos datos quiero ver desde la posicion)
# Sintaxis: .head( aqui colocar cuantos datos quiero ver desde la posicion #0)
print (tabla.head(5))
#Si quiero ver datos del final del dataframe, utilizo metodo: .tail ()
# Sintaxis: .tail( aqui colocar cuantos datos quiero ver desde la posicion #-2, no muestra la ultima posicion)
print (tabla.tail(1))

#Si deseo traer una(s) columna(s) especifica, utilizo ["Colocar nombre de columna(s)"]

tabla[["close","open"]]


# si lo que deseo es traer solo datoz de una fila y una columna en especifico utilizaremos metodo .iloc[] o loc[]
#sintaxis: tabla["columa elegida"].iloc["filas elegidas"]
#Trayendo un solo dato; el primer dato de la columna open

tabla["open"].iloc[1:4]


#Trayendo varios datos: los primeros datos de las columnas high y low

tabla[["high","low"]].iloc[0:2]

#Fin primera Clase, Clase #3 del curso

#Bonus de primer repositorio

import pytz
from datetime import datetime

#Para traer informacion con zona horaria del pais en el que vivimos
timezone = pytz.timezone("America/Bogota")
#Con datetime le decimos fecha en la que queremos que se extraigan los datos
utc_from = datetime(2024, 8, 5, tzinfo=timezone)
#Aqui colocamos que producto queremos traer, y desde que momento hasta donde 
ticks = mt5.copy_ticks_from("TSLA", utc_from , 1000, mt5.COPY_TICKS_INFO)
print("Ticks received:",len(ticks))
#Lo volvemos un dataframe
ticks_frame = pd.DataFrame(ticks)
ticks_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')













