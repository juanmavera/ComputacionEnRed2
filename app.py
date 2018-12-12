from flask import Flask, render_template, request, redirect
from DataObtainer import *
from MongoHandler import *
from BeebotteHandler import *

import threading
import time
import numpy as np

app = Flask(__name__)

usedDB = True


def InitPeriodicDataObtainer():
    Data = DataObtainer()
    page = Data.get_web()
    Noticia = Data.get_web_data(page)

    mongoDB = MongoHandler()
    mongoDB.InsertNew(Noticia)

    bbtDB = BeebotteHandler()
    bbtDB.InsertNew(Noticia)

    threading.Timer(120, InitPeriodicDataObtainer).start()


def CalculaMedia(Mongo=True):
    if Mongo:
        mongoDB = MongoHandler()
        Clics, Meneos, Noticias, _, _ = mongoDB.LeerNoticias()

    else:
        bbtDB = BeebotteHandler()
        Clics, Meneos, Noticias, _, _ = bbtDB.LeerNoticias()

    mediaClics = np.mean(Clics)
    mediaMeneos = np.mean(Meneos)

    print('\nNoticias\n--------\n')
    for noticia in Noticias:
        print(noticia)

    print('\n\nEstadisticas\n------------\n')
    print('Numero medio de clics obtenidos: %.2f\n'
          'Numero medio de meneos obtenidos: %.2f\n'
          'Numero de noticias: %d\n'
          % (mediaClics, mediaMeneos, len(Noticias)))

    return mediaClics, mediaMeneos, len(Noticias)


def NoticiasUmbral(umbral, Mongo=True):
    if Mongo:
        mongoDB = MongoHandler()
        Clics, Meneos, Noticias, Fechas, Horas = mongoDB.LeerNoticias()

    else:
        bbtDB = BeebotteHandler()
        Clics, Meneos, Noticias, Fechas, Horas = bbtDB.LeerNoticias()

    zipNoticias = list(zip(Clics, Meneos, Noticias, Horas, Fechas))

    Clic = []
    Meneo = []
    Noticia = []
    Hora = []
    Fecha = []

    for noticia in zipNoticias:
        print(noticia)
        if int(noticia[0]) > int(umbral):
            print(noticia)
            Clic.append(noticia[0])
            Meneo.append(noticia[1])
            Noticia.append(noticia[2])
            Hora.append(noticia[3])
            Fecha.append(noticia[4])

    return Clic, Meneo, Noticia, Hora, Fecha

@app.route('/', methods=['GET','POST'])
def index():
    global usedDB
    uri_grafica = "https://beebotte.com/dash/b2228cc0-e059-11e8-a9e5-9db85b2d1393?shareid=shareid_CO5OcpPIrqxkuoip"

    if request.method == 'POST':
        boton = request.form['boton']
        if boton == 'Media':
            mediaClics, mediaMeneos, nNoticias = CalculaMedia(Mongo=usedDB)

            if usedDB:
                BD = 'Mongo DB'
            else:
                BD = 'BeeBotte DB'

            usedDB = not usedDB

            mongoDB = MongoHandler()
            Clics, Meneos, Noticias, Fechas, Horas = mongoDB.LeerNoticias()

            cadena = "Media de Clicks: %.2f || Media Meneos: %.2f || Noticias analizadas: %d || Base de datos utilizada: %s\n" % (mediaClics, mediaMeneos, nNoticias, BD)

            return render_template('index.html', summaryNews=cadena, clics=Clics[-10:], meneos=Meneos[-10:], noticias=Noticias[-10:], fechas=Fechas[-10:], horas=Horas[-10:])

        elif boton == 'Umbral':
            valorUmbral = request.form['UmbralText']

            Clics, Meneos, Noticias, Fechas, Horas = NoticiasUmbral(umbral=valorUmbral, Mongo=True)

            return render_template('index.html', clics=Clics[-10:], meneos=Meneos[-10:], noticias=Noticias[-10:], fechas=Fechas[-10:], horas=Horas[-10:])

        elif boton == 'Grafica':
            return redirect(uri_grafica)

    else:
        mongoDB = MongoHandler()
        Clics, Meneos, Noticias, Fechas, Horas = mongoDB.LeerNoticias()

        return render_template('index.html', clics=Clics[-10:], meneos=Meneos[-10:], noticias=Noticias[-10:], fechas=Fechas[-10:], horas=Horas[-10:])

@app.route('/loc')
def location():
    return'<p> UAH </p>'


if __name__ == '__main__':

    InitPeriodicDataObtainer()

    app.debug = True
    app.run(host='0.0.0.0', port=80)
