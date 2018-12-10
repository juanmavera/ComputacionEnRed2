import numpy as np

from pymongo import MongoClient


class MongoHandler():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.CompuP1

    def InsertNew(self, New):

        entrada = {
            'Clics': New[0],
            'Meneos': New[1],
            'Noticia': New[2],
            'Fecha': New[3],
            'Hora': New[4]
        }

        self.db.noticias.update_one({'Noticia': New[2]}, {'$set': entrada}, upsert=True) # si no hay match con la noticia la inserta

    def LeerNoticias(self):
        Clics = []
        Meneos = []
        Noticias = []
        Fechas = []
        Horas = []
        for New in self.db.noticias.find():
            Clics.append(int(float(New['Clics'])))
            Meneos.append(int(float(New['Meneos'])))
            Noticias.append(New['Noticia'])
            Fechas.append(New['Fecha'])
            Horas.append(New['Hora'])

        return Clics, Meneos, Noticias, Fechas, Horas