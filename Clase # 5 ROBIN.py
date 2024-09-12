
#___________________________________________________________CLASE #5________________________________________________________________

#_________________________________________CREACION DE ROBOT METODO MARTINGALA_______________________________________________________

# IMPORTANTE: Toda estrategia de trading debe contar con dos cosas: Condiciones de entrada y condiciones de salida


#*****************************************************************************************************************************************|
#SE RECOMIENDA ESCRIBIR EL PSEUDOCODIGO EN UN DIAGRAMA DE FLUJOS QUE AYUDE A ENTENDER QUE NECESITAMOS Y COMO SE DEBE ESTRUCTURAR EL CODIGO|
#*****************************************************************************************************************************************|

#LINK DEL PSEUDOCODIGO PARA ENTENDER QUE REALIZA EL ROBOT: https://uautonomaedu-my.sharepoint.com/:u:/r/personal/francisco_salcedo_uac_edu_co/_layouts/15/Doc.aspx?sourcedoc=%7BA9E3FC13-7EBC-4B04-A041-CBA69A8E069C%7D&file=Drawing.vsdx&action=edit&mobileredirect=true&DefaultItemOpen=1&login_hint=francisco.salcedo%40uac.edu.co&ct=1725034170678&wdOrigin=OFFICECOM-WEB.START.EDGEWORTH&cid=2a2f1c0b-76b0-4cd3-8259-34c7a79c303a&wdPreviousSessionSrc=HarmonyWeb&wdPreviousSession=93f9d12f-1ac2-4478-9ad7-6abd04e69a64&or=PrevEdit 

#________________________________________________________PRACTICA___________________________________________________________
import time
import pandas as pd
import MetaTrader5 as mt5

nombre =501049257
clave='I@6yTfWk'
servidor = 'RoboForex-Pro'
path = r'C:\Program Files\RoboForex MT5 Terminal\terminal64.exe'
mt5.initialize(login=nombre,password=clave,server=servidor,path=path)

#1. Abrimos nuestra cuenta de mt5
#2. Debemos tener tres funciones, estas funciones tienen la logica basica de la estrategia que vamos a seguir
#3. funcion extraer datos: Esta funcion trae los datos de un simbolo especifico en un marco de tiempo especifico
#4. Funcion enviar operacion: esta funcion automatiza el envio de ordenes al broker
#5. Funcion calcular operaciones abiertas: esta funcion se encarga de medir cuantas posiciones hemos abierto en un simbolo
#5b. Esto permite saber donde y de que volumen debemos colocar la siguiente operacion de recompra. O si apenas vamos a comenzar la estrategia

#_____________________________________________CODIGO PARA MOVER LA ESTRATEGIA_______________________________________________________


def extraer_datos(simbolo,num_periodos,timeframe):
    rates= mt5.copy_rates_from_pos(simbolo,timeframe,0,num_periodos)
    tabla= pd.DataFrame(rates)
    tabla['time'] = pd.to_datetime(tabla['time'], unit = 's')
    return tabla


def enviar_operaciones(simbolo, tipo_operacion, take_profit, stop_loss,volumen):
    diccionario_martingala={
    "action":mt5.TRADE_ACTION_PENDING,
    "symbol":simbolo,
    "price": mt5.symbol_info_tick(simbolo).ask, 
    "type": tipo_operacion,
    "tp": take_profit,
    "sl": stop_loss,
    "volume": volumen,
    "coment": "Martingala",
    "type filling":mt5.ORDER_FILLING_FOK
    }
    mt5.order_send(diccionario_martingala)
    
def calcular_operaciones_abiertas():
     try:
        operaciones_abiertas= mt5.positions_get()
        df_positions= pd.DataFrame(list(operaciones_abiertas), columns =operaciones_abiertas[0]._asdict().keys())
        df_positions["time"]=pd.to_datetime(df_positions["time"], unit='s')
     except:
        df_positions= pd.DataFrame()
     return df_positions

#_______________________________________________EJECUCCION DEL CODIGO_____________________________________________________

#Paso 1: Seleccionar un simbolo 
#Paso 2: Ejecutar la funcion extraer_datos 
#Paso 3: Calcular la media y la desviacion estandar
#Paso 4: Solicitar el precio actual al que se encuentra el simbolo
#Paso 5: Calcular el rango para Limite Superior - Limite Inferior (fila 14 y 15 de este codigo)
#Paso 6: Hacer un analisis de la direccion del precio (algo personal) (opcional)
#Paso 7: Ejecutar la funcion calcular_oepraciones_abiertas, validar si ya hay operaciones abiertas antes de ejecutar empezar.
#Paso 8: Con un len, ver la longitud de la variable, lo que permite ver cuantas operaciones abiertas hay.
#Paso 9: Con un condicional el programa sabe si aun no tenemos posiciones abiertas en el simbolo
#Paso 10: De ser asi, con ayuda de los limites se define si vamos a short o long.
#Paso 11: Calculamos nuestro TP y nuestro SL para colocarlo en la funcion enviar_operaciones y abrir nuestra primera posicion de ser necesario
#Paso 13: Si tenemos una o mas posiciones abiertas entonces:
#Paso 14: Lo primero que debemos es crear un nuevo dataframe que solo tenga la informacion que traiga el ultimo dato
#Paso 15: Tomamos el valor del volumen, el profit que lleva la ultima posicion y el type que define si es short o long del anterior dataframe
#Paso 16: Recalculamos el sp y el tp que va a tener dicha nueva posicion.
#Paso 17: Abrimos una nueva posicion pero con el volumen multiplciado por dos veces, agregando el nuevo sp y tp re calculado anteriormente 
#NOTA: Para mejorar la gestion del riesgo, robin no va a calcular nuevos sp, siempre sera un con un sp calculado al principio de la ejecuccion
while True: 
   df_simbolo = extraer_datos("AUDUSD",360,mt5.TIMEFRAME_H1)
   media_movil= df_simbolo["close"].rolling(12).mean().iloc[-1]
   desviacion_estandar= df_simbolo["close"].rolling(12).std().iloc[-1]
   precio_actual= df_simbolo["close"].iloc[-1]
   limite_superior= media_movil + 1*desviacion_estandar
   limite_inferior= media_movil - 1*desviacion_estandar

   posicion_abierta= calcular_operaciones_abiertas()
   num_posicion_abierta= len(calcular_operaciones_abiertas())

   if num_posicion_abierta==0:
      if precio_actual >= limite_superior:
         tp= mt5.symbol_info_tick("AUDUSD").ask - 0.4
         sl= mt5.symbol_info_tick("AUDUSD").ask + 0.2
         enviar_operaciones("AUDUSD",mt5.ORDER_TYPE_SELL_LIMIT,tp,sl,0.1)
      elif precio_actual <= limite_inferior:
         tp= mt5.symbol_info_tick("AUDUSD").bid + 0.4
         sl= mt5.symbol_info_tick("AUDUSD").bid - 0.2
         enviar_operaciones("AUDUSD",mt5.ORDER_TYPE_BUY_LIMIT,tp,sl,0.1)

   elif num_posicion_abierta>0:
      df_sentido_operacion= posicion_abierta.tail(1)
      sentido_operacion= df_sentido_operacion["type"].item()
      posible_profit=df_sentido_operacion["profit"].item()
      volumen_lotes= df_sentido_operacion["volume"].item()
     
      if (posible_profit<0) and (precio_actual > limite_superior):
         tp= mt5.symbol_info_tick("AUDUSD").ask -1.5
         enviar_operaciones("AUDUSD",mt5.ORDER_TYPE_SELL_LIMIT,tp,sl,volumen_lotes*2)
      elif (posible_profit<0 )and (precio_actual < limite_inferior):
         tp= mt5.symbol_info_tick("AUDUSD").bid +1.5
         enviar_operaciones("AUDUSD",mt5.ORDER_TYPE_BUY_LIMIT,tp,sl,volumen_lotes*2)
   
   time.sleep(60)
       


