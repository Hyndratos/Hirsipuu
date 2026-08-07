from peli import Peli

class Sovellus:
    """ Ohjelman pää objecti joka joka hoitaa pelin luonnin """
    def __init__(self):
        self.Peli = None

    def uusi_peli(self):
        self.Peli = Peli(
            sanatPolku="/home/client/Documents/GitHub/Hirsipuu/src/sanat.txt", 
            arvausMaara=6
        )
        self.Peli.aloitus()


def main():
    sovellus = Sovellus()
    sovellus.uusi_peli()

main()