from beebotte import *

class BeebotteHandler():
    def __init__(self):
        self.api_key = 'QNMGqaXUTizwYJC7ly4rCswl'
        self.secret_key = 'hUVA4I7F76tIWIYW4qpx3jZRPdrxt7Sg'
        self.client = BBT(self.api_key, self.secret_key)
        self.channel = 'CompuP1'

    def InsertNew(self, New):

        self.client.write(self.channel, 'Clics', New[0])
        self.client.write(self.channel, 'Meneos', New[1])
        self.client.write(self.channel, 'Noticia', New[2])
        self.client.write(self.channel, 'Fecha', New[3])
        self.client.write(self.channel, 'Hora', New[4])


    def LeerNoticias(self):
        Clicsparcial = []
        Clics = []

        Meneosparcial = []
        Meneos = []

        Noticiasparcial = []
        Noticias = []

        Fechasparcial = []
        Fechas = []

        Horasparcial = []
        Horas = []

        TotalClics = self.client.read(self.channel, 'Clics', 1000)
        for clic in TotalClics:
            Clicsparcial.append(clic['data'])

        TotalMeneos = self.client.read(self.channel, 'Meneos', 1000)
        for meneo in TotalMeneos:
            Meneosparcial.append(meneo['data'])

        TotalNoticias = self.client.read(self.channel, 'Noticia', 1000)
        for noticia in TotalNoticias:
            Noticiasparcial.append(noticia['data'])

        TotalFechas = self.client.read(self.channel, 'Fecha', 1000)
        for fecha in TotalFechas:
            Fechasparcial.append(fecha['data'])

        TotalHoras = self.client.read(self.channel, 'Hora', 1000)
        for hora in TotalHoras:
            Horasparcial.append(hora['data'])

        Noticia = zip(Clicsparcial, Meneosparcial, Noticiasparcial, Fechasparcial, Horasparcial, Fechasparcial)

        for index, noticia in enumerate(Noticia):

            if index == 0:
                NewAnt = noticia[2]

            if NewAnt != noticia[2]:

                Clics.append(noticia[0])
                Meneos.append(noticia[1])
                Noticias.append(noticia[2])
                Fechas.append(noticia[3])
                Horas.append(noticia[4])
                NewAnt = noticia[2]

            if index == len(Noticias)-1:
                Clics.append(noticia[0])
                Meneos.append(noticia[1])
                Noticias.append(noticia[2])
                Fechas.append(noticia[3])
                Horas.append(noticia[4])
                NewAnt = noticia[2]

        return Clics, Meneos, Noticias, Fechas, Horas
