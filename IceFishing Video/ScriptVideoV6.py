from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
from datetime import datetime, timedelta
import traceback
import random
import os

salir = False


frases = ["suerte a todos", "good luck", "I am nervious", "Yess", "Noo", "I am going to win hehe", "I am the number oneee", "yep", "nop"]

link = "https://www.playdoit.mx/favourite-games/evolution-ice-fishing/real"


    
contador = 0
print("-"*60)
print()
print("[+] Iniciando el bot...\n")
print("[!] Para salir, haz click en la terminal y pulsa CTRL + C")
print()
print("-"*60)
print()


while True:


    if contador >= 15:
        print("[!] Se ha cumplido el número máximo de reintentos")
        input()
        break

    try:
            
        with sync_playwright() as p:

            

            browser = p.chromium.launch(headless=False, channel='chrome') # Primero iniciamos un navegador en modo headless, porque necesitamos un elemento que solo aparece si la ventana gráfica esta operativa

            context1 = browser.new_context()

            page = context1.new_page()


            page.goto(link, timeout=60000)

        

            page.get_by_placeholder('Email o Usuario').fill('maxgarciadsd@gmail.com')
            
            page.get_by_placeholder('Contraseña').fill('Playdoit1!')

            time.sleep(1)

            page.click("//button[contains(@class,'login__button')]") # Botón para logearnos


            try:
                page.click("//div[@class='modalContentWrapper']//button") # Es un cuadro de diálogo que debemos cerrar
            except:
                pass



            

            src_frame = page.frame_locator("//iframe[@class='game__content']").locator('//iframe').get_attribute('src') # Aquí se encuentra el link que necesitamos para que el vídeo se inicie correctamente


            storage= context1.storage_state()


    except Exception as e:

        print("-"*60)
        print()
        print("[!] Se ha producido un error:\n")
        traceback.print_exc()
        print()
        print("[+] Reintentando de nuevo...")
        print("-"*60)
        print()

        time.sleep(5)
        continue
    except KeyboardInterrupt:
        print("[!] Saliendo...")
        time.sleep(3)
        break


               
            

    try:
        with sync_playwright() as p2: # Iniciamos una nueva sesión porque queremos iniciar el navegador en modo headless

            browser2 = p2.chromium.launch(headless=True, channel='chrome')

            context2 = browser2.new_context(locale='es-MX', record_video_dir="videos/", 
                                    record_video_size={"width": 1920, "height": 1080},  
                                    viewport={"width": 1920, "height": 1080},
                                    storage_state=storage
                                    )


            page2 = context2.new_page()
            page2.goto(src_frame)

        
            try:
                primero = page2.frame_locator('//iframe').locator("span", has_text="Con tecnología de").nth(1)

                texto_primero = primero.text_content() # Si encontramos este elemento significa que el video ha cargado correctamente (en ocasiones falla)

            except PlaywrightTimeoutError:

                hoy = datetime.now().replace(second=0, microsecond=0)

   
                page2.close()

                context2.close()

                browser2.close()

                archivos = os.listdir('videos')


                for archivo in archivos: # Si el video no de IceFishing no ha cargado correctamente, eliminamos el último video pues no nos interesa

                    ruta = os.path.join('videos', archivo)

                    modificacion_epoch = os.path.getmtime(ruta)

                    ultima_modi = datetime.fromtimestamp(modificacion_epoch).replace(second=0, microsecond=0)

                    if hoy == ultima_modi:
                        os.remove(ruta)




                contador = contador + 1
    
            else:


                if contador != 0:
                    contador = 0

                


                inicio = datetime.now()


                escribir_chat = datetime.now()


                iframe = page2.frame_locator('//iframe') # Para poder dar click a unos determinados botones, tenemos que acceder a un iframe

                boton_volumen = iframe.locator('button[data-role="volume-button"]')

                boton_volumen.click(timeout=180000)

                
        
                while True:

                    
            
                    
                    if (datetime.now() - inicio) > timedelta(hours=1): # Si se cumple 1 hora de grabación, salimos del bucle

        
                        break


                    if (datetime.now() - escribir_chat) > timedelta(minutes=15): # Debemos escribir en el chat cada 15 minutos para que el casino no nos expulse por inactividad


                        input_chat = iframe.locator('input[data-role="quick-chat-input"]').fill(random.choice(frases))

                        boton_enviar = iframe.locator("button[data-role='message-input__button']")
                        
                        boton_enviar.click()
                

                        escribir_chat = datetime.now()

                    try:
                        boton = iframe.locator('div[data-role="button-container-item"] > button[data-role="button"]') # El boton para cerrar el mensaje que indica que no dispongo del saldo suficiente

                        boton.click()

                    except:
                        pass

                    page2.wait_for_timeout(200000)
                    iframe = page2.frame_locator('//iframe')

    except KeyboardInterrupt:
        print("[!] Saliendo...")
        time.sleep(3)
        break

                                      
    except Exception as e:

        print("-"*60)
        print()
        print("[!] Se ha producido un error:\n")
        traceback.print_exc()
        print()
        print("[+] Reintentando de nuevo...")
        print("-"*60)
        print()

    
        time.sleep(5)


