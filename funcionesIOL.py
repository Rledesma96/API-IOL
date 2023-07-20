import requests
import json
import pandas as pd
from typing import Union
from datetime import datetime
import config


# =============================================================================
# Generacion del Token para realizar las consultas
# =============================================================================
def token():
    url = "https://api.invertironline.com/token"
    data = {
            'username':config.username,
            'password': config.password,
            'grant_type':'password'
            }
    access = json.loads(requests.post(url=url, data=data).text)['access_token']
    refresh = json.loads(requests.post(url=url, data=data).text)['refresh_token']
    return access

# =============================================================================
# Acceso a los datos de mi cuenta
# =============================================================================

def datos_perfil():
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/datos-perfil"
    r = requests.get(url=url, headers=headers)
    
    return r.json()


def estado_cuenta():
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/estadocuenta"
    r = requests.get(url=url, headers=headers)
    if r.status_code==200:
        data = r.json()
        if "message" in data and data['message'] == "En estos momentos estamos trabajando en la actualización de la información solicitada.":
            return "API Caida"
        else:
            return data
    else:
        return r

def portafolio(pais:str="argentina"):
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/portafolio"
    data = {'pais':pais}
    r = requests.get(url=url, headers=headers, data=data)
    if r.status_code==200:
        data = r.json()
        if "message" in data and data['message'] == "En estos momentos estamos trabajando en la actualización de la información solicitada.":
            return "API Caida"
        else:
            return data
        
def consulta_operaciones(estado:str,desde:str,hasta:str,pais:str):
    #Valores permitidos
    estado_correcto = ['todas', 'pendientes','terminadas','canceladas']
    if estado not in estado_correcto:
        return "El valor especificado en Estado no es un parametro valido"
    
    pais_correcto = 'argentina'
    if pais != pais_correcto:
        return "El valor especificado en Pais no es un parametro valido, por el momento solo se permite argentina"    
    
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/operaciones"
    desde = datetime.strptime(desde, "%Y-%m-%d")
    hasta = datetime.strptime(hasta, "%Y-%m-%d")
    data = {'filtro.estado': estado,
            'filtro.fechaDesde': desde,
            'filtro.fechaHasta': hasta,
            'filtro.pais': pais
            }
    
    r = requests.get(url=url, headers=headers, data=data)
    if r.status_code==200:
        data = r.json()
        if "message" in data and data['message'] == "En estos momentos estamos trabajando en la actualización de la información solicitada.":
            return "API Caida"
        else:
            return data

# =============================================================================
# Obtencion de Datos de mercado
# =============================================================================

def cotizacion(simbolo:str, simple = False):
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/bCBA/Titulos/"+str(simbolo)+\
        "/CotizacionDetalle"
    data = {'mercado':'bCBA',
            'simbolo':simbolo}
    r = requests.get(url=url,data=data, headers=headers).text
    if simple == False:
        print(r)
    else:
        dicc = {}
        respuesta = json.loads(r)
        dicc['simbolo'] = respuesta['simbolo']
        dicc['ultimoPrecio'] = respuesta['ultimoPrecio']
        dicc['maximo'] = respuesta['maximo']
        dicc['minimo'] = respuesta['minimo']
        dicc['cierreAnterior'] = respuesta['cierreAnterior']
        dicc['volumenNominal'] = respuesta['volumenNominal']
        dicc['cantidadOperaciones'] = respuesta['cantidadOperaciones']
        try:
            dicc['Bid'] = respuesta['puntas'][0]['precioCompra']
        except IndexError:
            dicc['Bid'] = None
        try:
            dicc['Ask'] = respuesta['puntas'][0]['precioVenta']
        except IndexError:
            dicc['Ask'] = None
        dicc['date'] = str(datetime.datetime.now())
        asa = json.dumps(dicc)
        return asa

    
def mep(simbolo:str = None):
    bonos_locales = ['AL29','AL30','AL35','AE38','AL41']
    bonos_exterior = ['GD29','GD30','GD35','GD38','GD41','GD46']
    headers = {'Authorization': 'Bearer ' + token()}
    mep = {}
    
    if simbolo in bonos_locales +  bonos_exterior:
        url = "https://api.invertironline.com/api/v2/Cotizaciones/MEP/"+str(simbolo)
        data = {'simbolo':simbolo}
        r = requests.get(url=url, data=data, headers=headers).json()
        return r
    
    elif simbolo == "todos":
        for i in bonos_locales:
            url = "https://api.invertironline.com/api/v2/Cotizaciones/MEP/"+str(i)
            data = {'simbolo':i}
            r = requests.get(url=url,data=data, headers=headers).json()
            mep[i] = r
        for j in bonos_exterior:
            url = "https://api.invertironline.com/api/v2/Cotizaciones/MEP/"+str(j)
            data = {'simbolo':j}
            r = requests.get(url=url,data=data, headers=headers).json()
            mep[j] = r
            
        return mep
    
    elif isinstance(simbolo, int):
        return {"error":"El Simbolo debe ser en letras, no en números"}
    
    elif isinstance(simbolo, float):
        return {"error":"El Simbolo debe ser en letras, no en números"}
    
    return {"error":"El simbolo ingresado no tiene MEP"}


def cotizacion_historica(mercado:str, simbolo:str,desde:str,hasta:str):
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/"+\
        str(mercado)+"/Titulos/"+str(simbolo)+"/Cotizacion/seriehistorica/"+\
            str(desde) + str(hasta)+"ajustada"
    r = requests.get(url=url, headers=headers)
    return r

def comprar_stock(
                  simbolo: str,
                  cantidad: int,
                  precio: float,
                  plazo: str,
                  validez:str,
                  mercado:str  = "bCBA"):
    
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/Operar/Comprar"
    data = {'mercado':"bCBA",
            'simbolo': simbolo,
            'cantidad': cantidad,
            'precio': precio,
            'plazo': plazo, #t0, t1 o t2
            'validez':validez, #fecha en formato texto ejemplo: 2023-05-23
            }
    
    if (cantidad*precio) > estado_cuenta().json()['cuentas'][0]['disponible']:
        print ("No tenes saldo suficiente en la cuenta")
    else:
        comprar = requests.post(url, headers=headers, data=data)
        return comprar.text
    
def vender_stock(simbolo:str,
                cantidad:int,
                precio:float,
                plazo:str,
                validez:str):
    
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/Operar/Comprar"
    data = {'mercado':"bCBA",
            'simbolo': simbolo,
            'cantidad': cantidad,
            'precio': precio,
            'plazo': plazo,
            'validez':validez,
            }
    
    # Comprobar si el activo está en cartera
    en_cartera = []
    for i in json.loads(portafolio())['activos']:
        en_cartera.append(i['titulo']['simbolo'])
    posicion = en_cartera.index(simbolo)
    
    if simbolo not in en_cartera:
        print("No podes vender un activo que no tenes en el portafolio")
    
    elif cantidad > (json.loads(portafolio())['activos'][posicion]['cantidad']):
        print("No podes vender mas cantidad de activo que disponible en cartera")
        
        
    # Si para ese control, ejecutamos la funcion
    else:
        vender = requests.post(url, headers=headers, data=data)
        print(vender.text)

#comprar_stock("BOLT", 1, 15,"t0","2023-12-31")

#print(consulta_operaciones("todas","2018-01-01","2018-06-30","argentina"))
print(token())