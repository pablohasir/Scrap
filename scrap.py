#Importamos las librerías necesarias
import csv
import requests
import sys
import os
from bs4 import BeautifulSoup

#Comprobamos que se pase el enlace como argumento
if len(sys.argv) < 2 :
	print ('Debes indicar el enlace del canal')
	sys.exit()

#Meto el enlace en una variable y le hago un curl para obtener el código fuente
url = sys.argv[1]
os.system(f"curl {url} > pagina.txt")

#Hola


#A continuación voy a abrir el archivo con el código fuente para hacer un bucle.
#Este bucle buscará la cadena "videoId": y sacará el contenido que tiene hasta
#llegar a ". Así consigo el id de los vídeos. Repite el proceso para todo el código

with open("pagina.txt", "r") as archivo:
    contenido = archivo.read()

    index = 0
    while True:
        # Busca la cadena "videoId": a partir de la posición index
        index = contenido.find('"videoId":', index)
        if index == -1:
            # Si no se encuentra más la cadena, salir del bucle
            break

        # Busca la siguiente aparición de " a partir de la posición index
        index_comilla = contenido.find('"', index + len('"videoId":') + 1)
        if index_comilla == -1:
            # Si no se encuentra la siguiente comilla, salir del bucle
            break

        # Guarda el texto entre las comillas en el archivo videoId.txt
        video_id = contenido[index + len('"videoId":')+1 : index_comilla]
        with open("videoId.txt", "a") as archivo_video_id:
            archivo_video_id.write(video_id + "\n")

        # Actualiza el índice para buscar la siguiente cadena "videoId":
        index = index_comilla

#Como se encuentra el mismo id varias veces lo ordeno e indico que se guarde
#solo una vez. A continuación le pongo lo que falta de enlace a cada id
os.system("sort -u videoId.txt > videoId1.txt")
os.system("sed -i 's/^/https:\/\/www.youtube.com\/watch?v=/' videoId1.txt")




# Meto en una variable el archivo con los enlaces y otro archivo de salida
input_file = "videoId1.txt"
output_file = "webScraping.csv"

#Voy a hacer un bucle para que haga un request de cada enlace y busque el título
with open(input_file, "r") as f_input, open(output_file, "w", newline="") as f_output:
    csv_writer = csv.writer(f_output)

    # Iterate over each line in the input file
    for line in f_input:

        # Make a request to the URL in the line
        url = line.strip()
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Aquí busca el contenido en la etiqueta <title>
        title = soup.find("title").get_text()

        # Ahora le pido que haga un csv con enlace, título 
        csv_writer.writerow([url, title])

#Elimino los otros archivos
os.system("rm pagina.txt videoId.txt videoId1.txt")