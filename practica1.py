#!/usr/bin/python3

import webapp
import urllib.parse
import requests
import os.path

real_urls = {}
shortened_urls = {}

id = len(real_urls)

formulario = """
 <form action="" method="POST">
  URL:<br>
  <input type="text" name="url" value="http://www.youtube.com"><br>
  <input type="submit" value="Enviar">
</form>
"""


def read_file():
    if os.path.isfile("urls.txt"):
        # print("FILE EXIST!!!")
        file = open("urls.txt", "r")
        for line in file:
            # print(line)
            id_num, url_name = line.split(",")
            # print("numero: |" + id_num + "| url: |" + url_name[:-1] + "|")
            real_urls[int(id_num)] = url_name[:-1]
            shortened_urls[url_name[:-1]] = int(id_num)
        file.close()
        # print("AÑADIDO TODO EL FICHERO: ")
        # print(real_urls)
        # print(shortened_urls)
    else:
        print("FILE DOESN`T EXIST!!!")
        file = open("urls.txt", "w")


def save_in_file(id, url):
    # print("ENTRO A ESCRIBIR AL FILE!!!")
    file = open("urls.txt", "a")
    line = str(id) + "," + url + "\n"
    file.write(line)
    file.close()


def create_list():
    url_list = ""
    for key, val in real_urls.items():
        # print("KEY:" + str(key) + " VALUE: " + val)
        url_list += "<br><a href=" + str(key) + ">" + str(key) + "</a>" + ": "
        url_list += "<a href=" + val + ">" + str(val) + "</a><br/>"
    return url_list


class contentApp(webapp.webApp):
    def parse(self, request):
        return (request.split()[0], request.split()[1], request)

    def process(self, parsedRequest):
        metodo, recurso, peticion = parsedRequest
        try:
            num = recurso.split('/')[1]
            # print("NUM: " + num)
            if num != "":
                int(num)
            if recurso == "/":
                if metodo == "GET":
                    url_list = create_list()
                    return ("200 OK", "<html><h1>URL Shortener</h1>" +
                            formulario + "Lista URLs: " + url_list + "</html>")
                elif metodo == "POST":
                    cuerpo = peticion.split('\r\n\r\n', 1)[1]
                    # print(metodo)
                    # print(recurso)
                    # print(cuerpo)
                    url = urllib.parse.unquote_plus(cuerpo.split('=')[1])
                    if url == "":
                        # print("URL vacia")
                        return ("404 Not found", "<html>Error: URL incorrecta!</html>")
                    if not (url.startswith('http://') or url.startswith('https://')):
                        url = "http://" + url
                    if url in shortened_urls:
                        respuesta = "<a href=" + str(shortened_urls[url]) + ">" + str(shortened_urls[url]) + "</a>" + ": "
                        respuesta += "<a href=" + url + ">" + url + "</a>"
                        return ("200 OK", "<html>RESP: " + respuesta + "</html>")
                    else:
                        id = len(real_urls)
                        real_urls[id] = url
                        shortened_urls[url] = id
                        save_in_file(id, url)
                        try:
                            # print(real_urls)
                            # print(shortened_urls)
                            # print(recurso)
                            respuesta = "<a href=" + str(id) + ">" + str(id) + "</a>" + ": "
                            respuesta += "<a href=" + real_urls[id] + ">" + str(real_urls[id]) + "</a>"
                            return ("200 OK", "<html>RESP: " + respuesta + "</html>")
                        except KeyError:
                            url_list = create_list()
                            return ("404 Not found", "<html><h1>URL Shortener</h1>\r\n<h2>Not found!</h2>" +
                                    formulario + "Lista URLs: " + url_list + "</html>")
            elif int(num) in real_urls:
                # print("EXISTE: " + real_urls[int(num)])
                return ("302 Found\r\nLocation: " + real_urls[int(num)], "")
            else:
                # print("NINGUN CASO")
                url_list = create_list()
                return ("404 Not found", "<html><h1>URL Shortener</h1>\r\n<h2>Not found!</h2>" +
                        formulario + "Lista URLs: " + url_list + "</html>")
        except ValueError:
            # print("ERRRORRR!")
            url_list = create_list()
            return ("404 Not found", "<html><h1>URL Shortener</h1>\r\n<h2>Not found!</h2>" +
                    formulario + "Lista URLs: " + url_list + "</html>")


if __name__ == "__main__":
    read_file()
    testWebApp = contentApp("localhost", 1234)
