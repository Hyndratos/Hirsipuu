import subprocess
from peli import Peli
import ascii as ac
from varit import Vari
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
                self.tyhjenna_terminaali()
                self.Peli = None
                self.piirrä_alotusruutu()

            if self.Peli != None:
                input("Paina Enter Jatkaaksesi")
                self.Peli = None
                self.tyhjenna_terminaali()
                continue
            
            try:
                komento = int(input("Valitse komento: "))
            except ValueError:
                print("Anna numero.\n")
                self.tyhjenna_terminaali()
                continue
            except KeyboardInterrupt:
                self.tyhjenna_terminaali()
                print("\nPeli lopetettu.")
                break

            if self.suorita_komento(komento):
                self.tyhjenna_terminaali()
                print("\nPeli lopetettu.")
                break


    def piirrä_alotusruutu(self):
        """ Printaa aloitusruudun """
        print(Vari.ENDC, end="")
        
        print(ac.logo)

        print(f"1: {Vari.OKGREEN}Alota Uusi Peli")
        print(Vari.ENDC, end="")

        print(f"2: {Vari.OKBLUE}Valitse Sana lista")
        print(Vari.ENDC, end="")

        print(f"3: {Vari.FAIL}Lopeta Peli")
        print(Vari.ENDC)


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
        for sijainti, _, tiedostonimi in os.walk(tiedosto_polku):
            for i, f in enumerate(tiedostonimi):
                tiedostot.append(os.path.abspath(os.path.join(sijainti, f)))
                print(f"{i}: {f}")
        return tiedostot

    def tyhjenna_terminaali(self):
        """ Tyhjentää terminaalin seurvaa piirtoa varten """
        subprocess.run(["clear" if sys.platform == "linux" else "cls"], shell=True)


def main():
    sovellus = Sovellus()
    sovellus.alotusruutu()


if __name__ == "__main__":
    main()