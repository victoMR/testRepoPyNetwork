import os
import subprocess
import requests
import time
import sys

def ejecutar_ping(sitio):
    try:
        # Ejecuta el comando de ping
        resultado = subprocess.check_output(["ping", sitio])

        # Decodifica la salida (puede variar según la codificación de tu sistema)
        resultado_decodificado = resultado.decode("cp1252")

        # Muestra los resultados
        print(resultado_decodificado)
    except subprocess.CalledProcessError:
        print(f"No se pudo hacer ping a {sitio}. Verifica el nombre del dominio o la conexión.")

def prueba_velocidad_descarga(url):
    try:
        inicio = time.time()
        response = requests.get(url)
        fin = time.time()
        tiempo_transcurrido = fin - inicio
        velocidad_descarga_mbps = len(response.content) * 8 / tiempo_transcurrido / 1e+6
        return velocidad_descarga_mbps
    except requests.RequestException:
        print("Error al descargar el archivo. Verifica la conexión o la URL.")

def animacion_espera():
    for _ in range(5):
        sys.stdout.write("\rRealizando prueba de velocidad de internet. Por favor, espera...")
        sys.stdout.flush()
        time.sleep(1)
        sys.stdout.write("\r" + " " * 60 + "\r")

if __name__ == "__main__":
    print("Menú"
          "\n1: Comparar dos números"
          "\n2: Sumar dos números"
          "\n3: Abrir navegador"
          "\n4: Opciones de red")

    option1 = input("¿Qué opción deseas? Presiona el número correspondiente: ")

    if option1 == "1":
        number1 = input("Ingresa el primer número a comparar: ")
        number2 = input("Ingresa el segundo número para comparar: ")

        if number1 == number2:
            print("Son iguales. Puedes proseguir.")
        else:
            print("No son iguales.")
    elif option1 == "2":
        number1 = float(input("Ingresa el primer número: "))
        number2 = float(input("Ingresa el segundo número: "))
        res = number1 + number2
        print(res)
    elif option1 == "3":
        sitio = input("¿Qué página deseas visitar? (solo el nombre, no la URL): ")
        url = f"https://{sitio}"
        option2 = input("¿Qué tipo de dominio es (.com, .net, etc.)?: ")
        domain = url + "." + option2
        os.system(f"start msedge.exe --inprivate {domain}")
        print("Abriendo Microsoft Edge en modo privado...")
    elif option1 == "4":
        print("\n1: Reiniciar todas las interfaces de red"
              "\n2: Hacer ping a un sitio web"
              "\n3: Limpiar la caché DNS"
              "\n4: Realizar prueba de velocidad de internet")
        menu = input("¿Qué deseas hacer? Presiona el número correspondiente: ")

        if menu == "1":
            os.system(f"powershell.exe Restart-NetAdapter -All")
        elif menu == "2":
            sitio = input("¿Qué sitio deseas hacer ping? (solo el nombre, no la URL): ")
            option2 = input("¿Qué tipo de dominio es (.com, .net, etc.)?: ")
            domain = sitio + "." + option2
            animacion_espera()
            ejecutar_ping(domain)
        elif menu == "3":
            os.system("ipconfig /flushdns")
            print("Caché DNS limpiada correctamente.")
        elif menu == "4":
            url_prueba = "http://ipv4.download.thinkbroadband.com/512MB.zip"  # URL de un archivo grande (puedes cambiarlo)
            animacion_espera()
            velocidad_descarga = prueba_velocidad_descarga(url_prueba)
            print(f"Velocidad de descarga: {velocidad_descarga:.2f} Mbps")
        else:
            print("Opción no válida. Inténtalo nuevamente.")
    else:
        print("Opción no válida. Inténtalo nuevamente.")
