
#__________________________________________________GALA I_________________________________________________


#___________________________________CLASE #6: ARBIRAJE ESTADISTICO________________________________________

#_____________________________________PARTE I: Tipos Estrategias De Trading_______________________________

#________________________________________ESTRATEGIAS DE MOMEMTUM__________________________________________



import time
import pandas as pd
import MetaTrader5 as mt5

nombre =501049257
clave='I@6yTfWk'
servidor = 'RoboForex-Pro'
path = r'C:\Program Files\RoboForex MT5 Terminal\terminal64.exe'
mt5.initialize(login=nombre,password=clave,server=servidor,path=path)