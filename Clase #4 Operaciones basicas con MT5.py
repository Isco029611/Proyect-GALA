import pandas as pd
import MetaTrader5 as mt5

#Primero: Descargar Libreria de pandas y MetaTrader5 
#Verificar que Numpy este siendo compatible si no, colocar comando Pip Install Numpy<2 Para que descarge una version anterior a la 2.0
#Se ingresa credenciales de la cuenta.

nombre =501049257
clave='I@6yTfWk'
servidor = 'RoboForex-Pro'
path = r'C:\Program Files\RoboForex MT5 Terminal\terminal64.exe'
mt5.initialize(login=nombre,password=clave,server=servidor,path=path)

#CLASE #4 Operaciones con mt5 

#____________________________________CLASE #4________________TEORIA________________________________________


#Teoria: LOS TIPOS DE OPERACION QUE EXISTEN SON:
#1. Operaciones de mercado 
#2. Operaciones pendientes
#3. Modificaciones de operaciones

#SU MQLS ES EL SIGUIENTE:
#1. TRADE_ACTION_DEAL (ABRE UNA POSICION INSTANTANEA, COMPRA A MERCADO)
#2. TRADE_ACTION_PENDING (SOLICITA ABRIR UNA POSICION CON ORDEN LIMITE)
#3. TRADE_ACTION_MODIFY (MODIFICA LA LA ORDEN DE APERTURA DE POSICION)
#4. TRADE_ACTION_SLTP (COLOCA UN STOP LOSS/TAKE PROFIT)
#5. TRADE_ACTION_REMOVE (PERMITE ELIMINAR LAS ORDENES NO EJECUTADAS AL MOMENTO)
#6. TRADE_ACTION_CLOSE_BY (PERMITE CERRAR LA POSICIONES ABIERTAS)

#TEORIA: TIPOS DE ORDENES
#1. Compra
#2. Venta
#3. Buy limit
#4. Sell limit
#5. Buy stop
#6. Sell stop

#SU MQLS ES EL SIGUIENTE
#1. ORDER_TYPE_BUY (Colocar posicion en long/ Cierra posicion en short)
#2. ORDER_TYPE_SELL (Colocar una posicion en short/ Cierra una posicion en long)
#3. ORDER_TYPE_BUY_LIMIT (Colocar posicion en long limit/ Cierra posicion en short)
#4. ORDER_TYPE_SELL_LIMIT (Colocar una posicion en short limit/ Cierra una posicion en long)
#5. ORDER_TYPE_BUY_STOP (Colocar posicion en long al superar cierto precio/ Cierra posicion en short)
#6. ORDER_TYPE_SELL_STOP (Colocar posicion en long al superar cierto precio/ Cierra posicion en short)

#TEORIA: POLITICA DE EJECUCCION DE ORDEN / ORDER FILLING:

#1. La orden de apertura se ejecutara si solo si se consigue el 100% del importe: "ORDER_FILLING_FOK"
#2. Para que la orden de apertura se ejecute con un importe parcial: "ORDER_FILLING_IOC"

# _____________________________________________PRACTICA__#1________ ABRIR UNA POSICION_________________________________

#Para lanzar una orden de trading algoritmico y abrir - cerrar una posicion. El mercado debe estar abierto.

#1. Crear un diccionario o una funcion con un diccionario.
#2. Colocamos si queremos ejecutar una orden a market, limite, modificarla,  coloca un sl/tp, eliminar las ordenes o cerrar posiciones
#3. Colocar que elemento (accion o comodity) queremos negociar.
#4. Colocamos el lotaje que queremos negociar.
#4. Colocamos si queremos que la orden se pueda ejecutar parcialmente o si solo se ejecutara si se completa el lotaje al 100%
#5. Debemos fijarnos que en Algo Trading, dentro de MT5 tenga el simbolo play verde,si esta un cuadrado rojo hacer clic.

dic_basico_apertura= {
     "action":mt5.TRADE_ACTION_DEAL,
     "type": mt5.ORDER_TYPE_SELL,
     "symbol":"TSLA",
     "volume": 0.05,
     "type_filling":mt5.ORDER_FILLING_FOK
     } 
mt5.order_send(dic_basico_apertura)


# _________________________________________PRACTICA__#2_______ABRIR VARIAS POSICIONES________________________________

#Para abrir varias posiciones y lanzar varias ordenes market o limit en simultaneo, utilizamos un ciclo for
#En este caso solo se abriran ordenes del simbolo que indiquemos en el diccionario

#1. Creamos un diccionario con las mismas keys y values.
#2. Colocamos un ciclo for con un rango deseado

for i in range(0,3):
     dic_basico_loop={
          "action":mt5.TRADE_ACTION_DEAL,
         "symbol":"GOOGL",
          "volume": 0.05,
          "type": mt5.ORDER_TYPE_BUY,
          "magic":20240701,
          "comment":(f"posicion:{i+1}"),
          "type_filling":mt5.ORDER_FILLING_FOK
          }  
     mt5.order_send(dic_basico_loop)

#_____________________________________PRACTICA__#3_______ABRIR VARIAS POSICIONES EN VARIOS SIMBOLOS__________________________________

#Para abrir varias posiciones y lanzar varias ordenes market o limit en simultaneo.
#Y que tambien sean en varios simbolos especifico debemos realizar lo siguiente:
# Para este ejemplo escogere 2 o mas simbolos para abrir posiciones y en cada simbolo abrire un numero x de posiciones en long a market 

#1. Creamos una lista/tupla con los simbolos que estamos interesados negociar
#2. Creamos un ciclo for con un rango el cual definiria cuantas posiciones/ordenes vamos a abrir para cada simbolo
#3. Creamos un ciclo for que se encagara de pasar al siguiente simbolo y ejecutar la creacion de la orden en dicho simbolo elegido.
#4. Creamos un diccionario con las mismas keys y values.
#5. Importante la indentacion de la funcion orden_send, juega un papel importante para que el codigo haga lo que uno desea 

lista_simbolos=["TSLA","AAPL"]
for symbol in lista_simbolos:
     for j in range(0,3):
          dic_basico_loop_symbols={
               "action":mt5.TRADE_ACTION_DEAL,
               "symbol":symbol,
               "volume": 0.05,
               "type": mt5.ORDER_TYPE_BUY,
               "comment":(f"LOOP:{symbol}{j}"),
               "type_filling":mt5.ORDER_FILLING_FOK
               }  
          mt5.order_send(dic_basico_loop_symbols)


#________________________________________PRACTICA__#3.1_____________________________________________

#
#Para realizar la apertura en long o en short dependiende de una o varias variables.


lista_simbolos=["NVDA","MSFT","TSLA","GOOGL"]
for symbol in lista_simbolos:
     for i in range(0,2):
          if symbol == "TSLA":
               type_operation= mt5.ORDER_TYPE_SELL
          else:
               type_operation= mt5.ORDER_TYPE_BUY
          dic_SELL_BUY_loop_symbols={
               "action":mt5.TRADE_ACTION_DEAL,
               "symbol":symbol,
               "volume": 0.05,
               "comment":(f"{symbol} {i+1}"),
               "type": type_operation,
               "type_filling":mt5.ORDER_FILLING_FOK
               }
          mt5.order_send(dic_SELL_BUY_loop_symbols)

 
#________________________________PRACTICA__#4_CIERRE DE TODAS LAS POSICIONES___________________________________________

#Para cerrar las posicones debemos entonces:
#1. Creamos una variable, la cual va a traer los datos de todas las posiciones que tengamos abiertas en nuestra cuenta de MT5
posiciones_abiertas= mt5.positions_get()

#2. tomamos la lista y la volvemos un Dataframe, agregamos la parte columns para que tome los valores que envia MT5
#2B. NOTA: Si no agregamos la parte de columns, entonces el dataframe no me va a mostrar el nombre de cada columna solo lo va a enumerar desde 0 hasta x
df_posiciones_abiertas= pd.DataFrame(list(posiciones_abiertas), columns = posiciones_abiertas[0]._asdict().keys())

#3. Tomamos la columna ticket del dataframe creado anteriormente (df_posciones_abiertas) y lo volvemos una lista, y lo guardamos en una variable
operaciones_ticket= df_posiciones_abiertas["ticket"].tolist()

#4. Creamos un lop que va a recorrer dicha lista recien creada y que va guardar el valor en una variable llamada "posicion"
for posicion in operaciones_ticket: 

#5. Creamos una variable, la cual se va a encargar de guardar true o false
#5.B Para saber si es true o false python va a comparar el valor de la columna del dataframe(df_posiciones_abiertas) vs el valor posicion 
#5.C Esto es para saber si se esta viendo la misma posicion abierta 
     df_operacion= df_posiciones_abiertas[df_posiciones_abiertas["ticket"]==posicion]

#6 Creamos varias variables, que traigan, simbolo, volumen y el sentido de posicion (long o short) 
#6.B Esta se va a encargar de recolectar el numero 0 y 1, donde 0 signficia posicion en long y 1 posicion en short.
     posicion_abierta= df_operacion["type"].iloc[0] 
     simbolo_posicion_abierta= df_operacion["symbol"].iloc[0]
     volumen_posicion_abierta= df_operacion["volume"].iloc[0]
     if posicion_abierta==0:
          cerrar_posicion= mt5.ORDER_TYPE_SELL
     else: 
          cerrar_posicion= mt5.ORDER_TYPE_BUY
     
     dic_cierre_posicion={
          "action":mt5.TRADE_ACTION_DEAL,
          "symbol":simbolo_posicion_abierta,
          "volume": volumen_posicion_abierta,
          "position": posicion,
          "type": cerrar_posicion,
          "type_filling":mt5.ORDER_FILLING_FOK
          }
     mt5.order_send(dic_cierre_posicion)

#________________________________________PRACTICA__#5__CERRAR OPERACIONES UNICAMENTE EN PROFIT__________________________________________


#Para que el codigo solo nos cierre las posiciones que estan en ganancia
#Se utiliza la misma columna de codigo y solo se debe cambiar:
#Debemos colocar un condicional que se active si el profit es positivo y dentro colocaremos la funcion "orden_send"
#Para cerrar las posiciones en perdida se hara lo mismo colocando que el profit es menor a 0

posiciones_abiertas= mt5.positions_get()
df_posiciones_abiertas= pd.DataFrame(list(posiciones_abiertas), columns = posiciones_abiertas[0]._asdict().keys())
operaciones_ticket= df_posiciones_abiertas["ticket"].tolist()
for posicion in operaciones_ticket: 
     df_operacion= df_posiciones_abiertas[df_posiciones_abiertas["ticket"]==posicion]
     posicion_abierta= df_operacion["type"].iloc[0] 
     simbolo_posicion_abierta= df_operacion["symbol"].iloc[0]
     volumen_posicion_abierta= df_operacion["volume"].iloc[0]
     posicion_profit= df_operacion["profit"].iloc[0]

     if posicion_abierta==0:
          cerrar_posicion= mt5.ORDER_TYPE_SELL
     else:
          cerrar_posicion= mt5.ORDER_TYPE_BUY
     
     dic_cierre_posicion={
          "action":mt5.TRADE_ACTION_DEAL,
          "symbol":simbolo_posicion_abierta,
          "volume": volumen_posicion_abierta,
          "position": posicion,
          "type": cerrar_posicion,
          "type_filling":mt5.ORDER_FILLING_FOK
          }
     if posicion_profit>0:
          mt5.order_send(dic_cierre_posicion)
     else: 
          print ("Operacion en perdida")

#__________________________________________________ORDENES LIMITES________________________________________________________

#________________________________________________PRACTICA #1___________________________________________________

#1. Para crear una orden limite, se debe tener un diccionario, con keys y values parecidos a una orden a mercado.
#2. Se debe colocar una key adicional que es price. En el value se debe colocar el codigo necesario donde se solicita el precio del simbolo a mt5
#3. Existe el ask y el bid. para colocar el precio de entrada, se puede dejar solo el codigo o se puede sumar o restar un monto deseado para la entrada. 
#4. El valor ask, es el valor donde los vendedores estan dispuestas a vender sus acciones
#5. El valor bid, es el valor donde los compradores estan dispuestas a comprar las acciones 
#6. Se debe cambiar el value de action y type. Cabe destacar que se puede abrir una posicion limit o stop, sea buy o sell. 


dic_orden_limite= {
     "action":mt5.TRADE_ACTION_PENDING,
     "symbol":"NVDA",
     "price": mt5.symbol_info_tick("NVDA").ask - 0.002,
     "volume": 0.05,
     "type": mt5.ORDER_TYPE_BUY_LIMIT,
     "type_filling":mt5.ORDER_FILLING_FOK
     } 
mt5.order_send(dic_orden_limite)

#NOTA: Se puede mezclar ciclos, y condicionales, para abrir posiciones en diferentes simbolos, y en diferentes sentidos del mercado.
#NOTA 2: Se puede cerrar posiciones con lo aprendido en la clase anterior.

#_________________________________________PRACTICA #2  ______CERRAR ORDENES NO EJECUTADA__________________________________________ 

#1. Recordemos que las ordenes que se colocan y el precio no las toca son posiciones sin abrir, las condiciones del mercado pueden cambiar
#2. Por eso, primero: debemos obtener los datos de las ordenes sin ejecutar aun. En la clase #4 Vimos como obtener los datos pero de las posiciones
#3. Convertirmos esta informacion en un dataframe. pero antes de eso, debemos convertirlo en una lista.
#4. sacar la informacion especifca de la columna ticket en forma de lista
#5. Debemos crear un pequeño diccionario que va a tener dos keys una que sera el ticket de la orden sin ejecutar y la indicacion de que remueva dicha orden.
#6. Para hacer mas automatico el proceso se crea un bucle que recorre la lista de tickets.

obtener_ordenes= mt5.orders_get()
df_ordenes= pd.DataFrame(list(obtener_ordenes), columns =obtener_ordenes[0]._asdict().keys())
ticket_deordenes=df_ordenes["ticket"].tolist()

for orden in ticket_deordenes:
     solicitud_cierre={
          "order": orden,
          "action": mt5.TRADE_ACTION_REMOVE,
          }
     resultado =mt5.order_send(solicitud_cierre)

#______________________________________PRACTICA #3  ______COLOCAR SP/TP A LAS ORDENES__________________________________________ 

#1. Se debe crear un diccionario con una estructura basica como la que trabajamos para orden limites o ha mercado 
#2.Para colocar un sp/tp se debe colocar dos keys adicionales.
#3. Se puede trabajar con los ciclos y sentencias, y adicionalmente pueden ser posiciones que se abrieron a mercado o ha limite.

dic_orden_sptp ={
     "action":mt5.TRADE_ACTION_PENDING,
     "symbol":"NVDA",
     "price": mt5.symbol_info_tick("NVDA").ask - 0.3,
     "volume": 1.0,
     "tp": mt5.symbol_info_tick("NVDA").ask + 2.1,
     "sl": mt5.symbol_info_tick("NVDA").ask - 1.1,
     "type": mt5.ORDER_TYPE_BUY_LIMIT,
     "type_filling":mt5.ORDER_FILLING_FOK
     } 
mt5.order_send(dic_orden_sptp)



#___________________________FIN DE LAS OPERACIONES BASICAS CON PYTHON_________________________________________

#________________________________________________Fin de la clase #4____________________________________________________
     