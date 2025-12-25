import requests
from datetime import datetime, timezone, timedelta
import time
import traceback
import json

utc_mexico = timezone(timedelta(hours=-6))
utc_ar = timezone(timedelta(hours=-3))
utc_ru = timezone(timedelta(hours=+3))


headers = {
    'accept': '*/*',
    'accept-language': 'es-ES,es;q=0.9,en;q=0.8',
    'origin': 'https://casinoscores.com',
    'priority': 'u=1, i',
    'referer': 'https://casinoscores.com/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
}


params = {
    'page': 0,
    'size': 16,
    'sort': 'data.settledAt,desc',
    'duration': 10,
    'isMatched': 'false',
    'wheelResults': 'LilBlues,BigOranges,HugeReds,Leaf1,Leaf2'

}

def telegram(mensaje, imagen):




    CHANNEL_ID = -1002480092493 # cliente
    # CHANNEL_ID = -1003454194717 #YO

    TOKEN = "8312889768:AAGtL6AYKolSoADt3L5c3NeNECKid8RrRew" # cliente
    # TOKEN = "5516289003:AAEvLBGEvFsKHpZKBb20YCLRmenCkmzXlg8" # yo
    URL = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'

    files = {'photo': open(f'{imagen}.png', 'rb')}


    contenido = {'inline_keyboard': [

        [{'text': 'JUGAR', 'url': "https://beacons.ai/juegosonline"}],
            [{'text': 'APRENDE A JUGAR', 'url': "https://t.me/betvibes25/83"}],
            [{'text': 'CÓMO RECARGAR', 'url': "https://t.me/betvibes25/91"}],
        ]
    }
    
    da = {
        'chat_id': CHANNEL_ID,
        'caption': mensaje,
        'parse_mode': 'HTML',
        'reply_markup': json.dumps(contenido)
    } 

    

    requests.post(URL, data=da, files=files)




with requests.Session() as session:

    session.headers = headers
    session.params = params

    print("(+) Iniciando", flush=True)



    almacen = []
    while True:

        try:
            response = session.get(
                'https://api.casinoscores.com/svc-evolution-game-events/api/icefishing',
            )


            if response.status_code != 200:
                print(f"Error en el status code, status {response.status_code}", flush=True)
                time.sleep(10)
                continue


            
            objeto = response.json()


            for resultado in objeto:

                ganancia = resultado['totalAmount']


                fecha = resultado['data']['settledAt']

                if fecha in almacen:
                    break

                fecha_utc = datetime.fromisoformat(fecha).astimezone(timezone.utc)
                
                

                # fecha_utc_8 = fecha_utc.astimezone(utc_minus_8)
                
                hora_mexico = fecha_utc.astimezone(utc_mexico).strftime('%H:%M %p')
                hora_ru = fecha_utc.astimezone(utc_ru).strftime('%H:%M %p')
                hora_ar = fecha_utc.astimezone(utc_ar).strftime('%H:%M %p')

                
                multiplicador= resultado['data']['result']['wheelResult']['maxMultiplier'] # El cliente necesita que este valor sea mayor o igual a 100

                apostadores = resultado['bettorsCount']

                tipo_pez = resultado['data']['result']['wheelResult']['wheelSector']

        
                # if multiplicador >= 100 and multiplicador <=250:

                #     if tipo_pez == "LilBlues":
                #         pez = 'Pez AZUL 🔵'
                #         imagen = 'azul'

                #     elif tipo_pez == "BigOranges":
                #         pez = 'Pez NARANJA 🟠'
                #         imagen = 'naranja'
                #     elif tipo_pez == "HugeReds":
                #         pez = 'Pez Rojo 🔴'
                #         imagen = 'rojo'
       

                #     multiplicador = str(multiplicador) + "X"

                #     mensaje = (f"SUPER <b>{pez}</b> de <b>{multiplicador}</b>\n\n"
                #             f"➡️ <b>Apostadores:</b> {apostadores}\n\n"
                #             f"➡️ <b>Ganancia:</b> {ganancia} $\n\n"
                #             f"➡️ <b>Fecha:</b> {fecha_final}\n\n"
                #             "🔎 <a href='https://telegra.ph/Bot-Ice-Fishing-12-01'><b>Información</b> acerca del <b>bot</b></a>"
                #             )


                #     telegram(mensaje=mensaje, imagen=imagen)
                
                fecha_final = fecha_utc.strftime('%d/%m/%Y') 
                
                if multiplicador > 250:
                    multiplicador = str(multiplicador) + "X"

                    imagen = 'otro'

                    mensaje = (f"⭐ SUPER PEZ de <b>{multiplicador}</b>\n\n"
                               f"🇲🇽 {hora_mexico} 🇦🇷 {hora_ar} 🇷🇺 {hora_ru}\n\n"
                            f"➡️ <b>Jugadores:</b> {apostadores}\n\n"
                            f"➡️ <b>Ganancia:</b> {ganancia} $\n\n"
                            f"➡️ <b>Fecha:</b> {fecha_final}\n\n"
                            "🔎 <a href='https://telegra.ph/Bot-Ice-Fishing-12-01'><b>Información</b> acerca del <b>bot</b></a>"
                            )
                    
             

                    telegram(mensaje=mensaje, imagen=imagen)


            almacen.clear()
            for resultado in objeto:
                fecha = resultado['data']['settledAt']

                almacen.append(fecha)


            time.sleep(60)

        except Exception as e:
            mensaje= traceback.format_exc()
            
            print(mensaje, flush=True)

            time.sleep(10)



# print(objeto['data']['result']['wheelResult'])
