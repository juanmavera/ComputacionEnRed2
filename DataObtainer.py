import numpy as np
import re

from urllib import urlopen
from time import strftime


class DataObtainer():
    def __init__(self):
        self.web = 'https://www.meneame.net/'

    def get_web(self):
        page = urlopen(self.web).read()

        return page

    def get_clics(self, page):

        patronClics = re.compile('<div class="clics">(.*?)</div>')
        listaClics = patronClics.findall(page)
        listaClics = listaClics[5:]
        Clics = np.zeros(np.array(listaClics).shape[0])

        for index, lista in enumerate(listaClics):
            aux = str(lista).split(' ')
            Clics[index] = int(aux[2])

        return Clics

    def get_meneos(self, page):

        patronMeneos = re.compile('<div class="votes"> <a (.*?)>(.*?)</a> meneos </div>')
        listaMeneos = patronMeneos.findall(page)
        Meneos = np.zeros(np.array(listaMeneos).shape[0])

        for index, lista in enumerate(listaMeneos):
            Meneos[index] = int(lista[1])

        return Meneos

    def get_news(self, page):
        patronNews = re.compile('<h2> <a href=(.*?) > (.*?) </a>(.*?)</h2>')
        listaNews = patronNews.findall(page)
        News = np.array(listaNews)[:, 1]

        return News

    def get_date(self):
        date = strftime("%d/%B/%Y")
        time = strftime("%H:%M:%S")

        return date, time

    def get_web_data(self, page):

        # Obteninendo Clics
        Clicks = self.get_clics(page)

        # Obteniendo Meneos
        Meneos = self.get_meneos(page)

        # Obteniendo Titulos
        News = self.get_news(page)

        # Obteniendo Hora
        date, time = self.get_date()

        # Solo se devuelven los datos de la primera noticia encontrada
        return Clicks[0], Meneos[0], News[0], date, time
