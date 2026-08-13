import subprocess
from peli import Peli
from colors import Color
import os

class Sovellus:
    """ Ohjelman pää objecti joka joka hoitaa pelin luonnin """
    def __init__(self):
        self.Peli = None

    def uusi_peli(self, sanat: str):
        self.Peli = Peli(
            sanatPolku=sanat, 
            arvausMaara=6
        )
        self.Peli.aloitus()

    def alotusruutu(self):
        while True:
            
            if self.Peli == None or self.Peli.Break:
                self.cls()
                self.piirrä_alotusruutu()
            
            try:
                komento = int(input("Valitse komento: "))
            except ValueError:
                self.Peli = None
                print("Anna numero.\n")
                self.cls()
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
        print(Color.ENDC, end="")
        print(f"""{Color.OKBLUE}
████████████████████████████████████████████████████████████████████
██                                                                ██
██                                                                ██
██    ██╗  ██╗██╗██████╗ ███████╗██╗██████╗ ██╗   ██╗██╗   ██╗    ██
██    ██║  ██║██║██╔══██╗██╔════╝██║██╔══██╗██║   ██║██║   ██║    ██
██    ███████║██║██████╔╝███████╗██║██████╔╝██║   ██║██║   ██║    ██
██    ██╔══██║██║██╔══██╗╚════██║██║██╔═══╝ ██║   ██║██║   ██║    ██
██    ██║  ██║██║██║  ██║███████║██║██║     ╚██████╔╝╚██████╔╝    ██
██    ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝      ╚═════╝  ╚═════╝     ██
██                                                                ██
██                                                                ██
████████████████████████████████████████████████████████████████████
        {Color.ENDC}""")
        print(f"1: {Color.OKGREEN}Alota Uusi Peli")
        print(Color.ENDC, end="")
        print(f"2: {Color.FAIL}  Lopeta Peli")
        print(Color.ENDC)


    def suorita_komento(self, komento) -> bool:
        match komento:
            case 1:
                tiedostot = self.hae_tiedostot()
                try:
                    index = int(input("Tiedosto numero: "))
                except ValueError:
                    return True
                except KeyboardInterrupt:
                    return True
                
                try:
                    sanat = tiedostot[index]
                except IndexError:
                    return True

                self.uusi_peli(sanat)
                return False
            case 2:
                return True
            case _:
                print("Virheellinen komento.")
                return False

    def hae_tiedostot(self) -> list[str]:
        """ Hakee sanat txt tiedostoja ja palautaa listan niiten poluista """
        tiedosto_polku = os.path.realpath(__file__)
        tiedosto_polku = tiedosto_polku.rstrip("main.py")
        tiedosto_polku += "sanat"

        tiedostot = []
        for dirpath,_,filenames in os.walk(tiedosto_polku):
            for i, f in enumerate(filenames):
                tiedostot.append(os.path.abspath(os.path.join(dirpath, f)))
                print(f"{i}: {f}")
        return tiedostot

    def cls(self):
        subprocess.run(["clear"], shell=True)


def main():
    sovellus = Sovellus()
    sovellus.alotusruutu()


if __name__ == "__main__":
    main()