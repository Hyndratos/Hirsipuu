from peli import Peli

class Sovellus:
    """ Ohjelman pää objecti joka joka hoitaa pelin luonnin """
    def __init__(self):
        self.Peli = None

    def uusi_peli(self):
        self.Peli = Peli(
            sanatPolku="src/sanat.txt", 
            arvausMaara=6
        )
        self.Peli.aloitus()

    def alotusruutu(self):
        while True:
            self.piirrä_alotusruutu()

            try:
                komento = int(input("Valitse komento: "))
            except ValueError:
                print("Anna numero.")
                continue
            except KeyboardInterrupt:
                print("\nPeli lopetetaan.")
                break

            if self.suorita_komento(komento):
                print("\nPeli lopetetaan.")
                break

    def piirrä_alotusruutu(self):
        print("\n--- HIRSIPUU ---")
        print("1: Alota Uusi Peli")
        print("2: Lopeta Peli")

    def suorita_komento(self, komento) -> bool:
        match komento:
            case 1:
                self.uusi_peli()
                return False
            case 2:
                return True
            case _:
                print("Virheellinen komento.")
                return False

def main():
    sovellus = Sovellus()
    sovellus.alotusruutu()

main()