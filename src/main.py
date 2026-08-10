import os
from peli import Peli
from colors import Color


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
            if self.Peli == None:
                self.cls()
            self.piirrä_alotusruutu()

            try:
                komento = int(input("Valitse komento: "))
            except ValueError:
                print("Anna numero.\n")
                continue
            except KeyboardInterrupt:
                self.cls()
                print("\nPeli lopetettu.")
                break

            if self.suorita_komento(komento):
                self.cls()
                print("\nPeli lopetettu.")
                break

    def piirrä_alotusruutu(self):
        print("\n--- HIRSIPUU ---")
        print(f"1: {Color.OKGREEN}Alota Uusi Peli")
        print(Color.ENDC, end="")
        print(f"2: {Color.FAIL}Lopeta Peli")
        print(Color.ENDC)

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

    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')


def main():
    sovellus = Sovellus()
    sovellus.alotusruutu()

main()