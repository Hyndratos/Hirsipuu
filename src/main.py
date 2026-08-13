import subprocess
from peli import Peli
import ascii as ac
from colors import Color
import os
import sys

class Sovellus:
    """ Ohjelman pää objecti joka joka hoitaa pelin luonnin """
    def __init__(self):
        self.Peli = None
        self.SanaTiedosto = None

    def uusi_peli(self, sanat: str):
        """ Luo uuden pelin ja aloitaa sen. """
        self.Peli = Peli(
            sanatPolku=sanat, 
            arvausMaara=6
        )
        self.Peli.aloitus()

    def alotusruutu(self):
        """ Pyöritää mainin loopin jossa se ottaa inputit ja tekee niilä asioita. """
        while True:
            
            if self.Peli == None or self.Peli.Break:
                self.cls()
                self.Peli = None
                self.piirrä_alotusruutu()

            if self.Peli != None:
                input("Paina Enter Jatkaaksesi")
                self.Peli = None
                self.cls()
                continue
            
            try:
                komento = int(input("Valitse komento: "))
            except ValueError:
                #self.Peli = None
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
        """ Printaa aloitusruudun """
        print(Color.ENDC, end="")
        
        print(ac.logo)

        print(f"1: {Color.OKGREEN}Alota Uusi Peli")
        print(Color.ENDC, end="")

        print(f"2: {Color.OKBLUE}Valitse Sana lista")
        print(Color.ENDC, end="")

        print(f"3: {Color.FAIL}Lopeta Peli")
        print(Color.ENDC)


    def suorita_komento(self, komento: int) -> bool:
        """ Suoritaa tietyn komennon riipuen siitä minkä numeron se saa ja jos retrun on True niin se sammutaa sovelluksen muuten jatkaa """

        match komento:
            case 1:
                if self.SanaTiedosto == None:
                    if self.valitse_tiedosto():
                        return False
                
                self.uusi_peli(self.SanaTiedosto)
                return False
            case 2:
                if self.valitse_tiedosto():
                    return False
                
            case 3:
                return True
            case _:
                print("Virheellinen komento.")
                return False

    def valitse_tiedosto(self) -> bool:
        """ Valitsee sana tiedoston ja palautaa True jos ei onnistunut muuten False """

        tiedostot = self.hae_tiedostot()
        try:
            index = int(input("Tiedosto numero: "))
        except ValueError:
            return True
        except KeyboardInterrupt:
            return True

        try:
            self.SanaTiedosto = tiedostot[index]
        except IndexError:
            return True
        
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
        subprocess.run(["clear" if sys.platform == "linux" else "cls"], shell=True)


def main():
    sovellus = Sovellus()
    sovellus.alotusruutu()


if __name__ == "__main__":
    main()