from random import choice
from varit import Vari
import subprocess
import ascii as ac
import sys

#######
#     |
#     O
#    /|\
#    / \

debug = True

class Peli:
    """ Hoitaa kaiken pelin logiikan. """
    TikkuUkot = [
        [" +-----+", " |     |", " |", " |", " |", "==="],
        [" +-----+", " |     |", " |     O", " |", " |", "==="],
        [" +-----+", " |     |", " |     O", " |     |", " |", "==="],
        [" +-----+", " |     |", " |     O", " |     |", " |      \\", "==="],
        [" +-----+", " |     |", " |     O", " |     |", " |    / \\", "==="],
        [" +-----+", " |     |", " |     O", " |     |\\", " |    / \\", "==="],
        [" +-----+", " |     |", " |     O", " |    /|\\", " |    / \\", "==="]
    ]

    def __init__(self, sanatPolku: str, arvausMaara: int):
        # Randomisti valittu sana
        self.Sana = ""

        # Sanan jonka pelaaja näkee johon listään oiken arvatut kirjaimet
        self.ArvausSana = ""

        # Elämä määrä eli kuinka monta yritystä on jäljellä
        self.ArvausMaara = arvausMaara
        self.IsoinArvausMäärä = arvausMaara

        # Polku teksti tiedostolle jossa on kaikki sanat
        self.SanatPolku = sanatPolku

        # Kaikki Annetut Kirjaimet pelaajalta
        self.AnnetutKirjaimet = ""

        # main tarvitsee tätä tarkistuksiin.
        self.Break = False

    def lue_sanat_tiedosto(self, polku: str):
        """ Lukee annetun polun tiedoston sanat ja lisää ne listaan. Jonka jälkeen se suoritaa valitse sana"""
        sanat = []
        with open(polku, "r", encoding="utf-8") as tiedosto:
            for sana in tiedosto:
                sana = sana.strip()

                if sana in sanat:
                    continue

                sanat.append(sana)

        self.valitse_sana(sanat)

    def tyhjenna_terminaali(self):
        """ Tyhjentää terminaalin seurvaa piirtoa varten. Jos Linux niin clear muuten cls komento """
        subprocess.run(["clear" if sys.platform == "linux" else "cls"], shell=True)


    def valitse_sana(self, sanat: list[str]):
        """ Valitsee Sanat listasta satunnaisen sanan. """
        self.Sana = choice(sanat)
        self.ArvausSana = "_" * len(self.Sana)

    def aloitus(self):
        """ Aloitaa pelin loopin """

        lopeta_loop = False

        self.lue_sanat_tiedosto(self.SanatPolku)

        # Pelin looppi jossa pyydetään pelaajalta kirjainta ja tehdää kaikki tarkistukset.
        while True:
            self.tyhjenna_terminaali()

            print(ac.logo)

            if debug: print(self.Sana)

            print("Kirjoita Lopeta jos haluat lopettaa tai paina ctrl + c")
            print()

            self.piirra_tikkiukko()
            self.piirra_arvaus()

            kirjain, onnistui = self.pyyda_kirjainta()

            if not onnistui:
                self.Break = True
                break

            if kirjain == "":
                continue
            
            if len(kirjain) > 1:

                kirjaimet = [k for k in kirjain if k not in self.AnnetutKirjaimet]

                for k in kirjaimet:
                    oliKirjain, kirjainLaitettu = self.tarkista_kirjain(k)

                    if not kirjainLaitettu:
                        continue

                    if self.vahennus_tarkistus(oliKirjain):
                        lopeta_loop = True
                        break
                    
            else:

                if any([k for k in kirjain if k in self.AnnetutKirjaimet]):
                    continue
                
                oliKirjain, kirjainLaitettu = self.tarkista_kirjain(kirjain)

                if not kirjainLaitettu:
                    print("Olet jo antanut tämän kirjaimen.")
                    continue
                
                if self.vahennus_tarkistus(oliKirjain):
                    lopeta_loop = True
                
            if self.sana_tarkistus():
                self.piirra_voittu_ruutu()
                break

            if lopeta_loop:
                print(ac.havisit_pelin)
                print(f"Sana oli: {Vari.OKGREEN}{self.Sana}{Vari.ENDC}")
                self.piirra_testatut_kirjaimet()
                break


    def piirra_arvaus(self):
        """ Printaa peli ruudulle Arvaus määrän, testatut kirjaimet ja nykesen arvatun sanan. """
        vari = Vari.OKGREEN if (self.IsoinArvausMäärä - self.ArvausMaara) < (self.IsoinArvausMäärä / 2) else Vari.FAIL
        print(f"Arvaus Määrä: {vari}{self.ArvausMaara}{Vari.ENDC}")
        self.piirra_testatut_kirjaimet()
        print(" ".join(self.ArvausSana))

    def piirra_testatut_kirjaimet(self):
        """ Printaa kirjaimet jota pelaaja on testannut. väri on punanen jos väärin ja vihree jos oikein. """

        print("Testatut Kirjaimet: ", end="")
        for i, k in enumerate(self.AnnetutKirjaimet):
            vari = Vari.OKGREEN if k in self.Sana else Vari.FAIL

            print(f"{"|" if i > 0 else ""}{vari}{k}{Vari.ENDC}", end="")
        print()

    def piirra_tikkiukko(self):
        """ Printaa TikkuUkon käytäen self.TikkuUkot listaa"""
        index = self.IsoinArvausMäärä - self.ArvausMaara
        try:
            for rivi in self.TikkuUkot[index]:
                print(Vari.FAIL, end="")
                print(rivi)
                print(Vari.ENDC, end="")
        except IndexError:
            for rivi in self.TikkuUkot[len(self.TikkuUkot) - 1]:
                print(Vari.FAIL, end="")
                print(rivi)
                print(Vari.ENDC, end="")

    def piirra_voittu_ruutu(self):
        """ Printaa voittu ruudun jossa on kaikki tiedot miten peli meni """
        self.tyhjenna_terminaali()
        print(ac.voitit_pelin)

        print(f"Sana: {Vari.OKGREEN}{self.Sana}{Vari.ENDC}")

        vari = Vari.OKGREEN if (self.IsoinArvausMäärä - self.ArvausMaara) < (self.IsoinArvausMäärä / 2) else Vari.FAIL
        print(f"Väärin annettu: {vari}{self.IsoinArvausMäärä - self.ArvausMaara}{Vari.ENDC}")

    def pyyda_kirjainta(self) -> tuple[str, bool]:
        """ Pyytää pelaajalta kirjaimen/kirjaimet aravausta varten ja palautaa kirjemen/kirjaimet ja onnistumis boolin. """
        onnistui = True
        kirjain = ""
        try:
            kirjain = str(input("Arvaa kirjain: "))
        except KeyboardInterrupt:
            self.tyhjenna_terminaali()
            onnistui = False


        if kirjain.lower() == "lopeta":
            self.tyhjenna_terminaali()
            onnistui = False
        
        kirjain = kirjain.replace(" ", "")
        return (kirjain, onnistui)

    def tarkista_kirjain(self, arvausKirjain: str) -> tuple[bool, bool]:
        """ Tarkistaa onko kirjain sanassa jos on niin palautaa True """
        oliKirjain = False
        kirjainLaitettu = True

        for i, kirjain in enumerate(self.Sana):
            if kirjain == arvausKirjain:
                kirjainLaitettu = self.lisaa_kirjain(i, kirjain)
                oliKirjain = True
        
        if arvausKirjain not in self.AnnetutKirjaimet:
            self.AnnetutKirjaimet += arvausKirjain.lower()
        
        return (oliKirjain, kirjainLaitettu)

    def sana_tarkistus(self) -> bool:
        """ Tarkistaa onko arvattu sana sama kuin sana ja palautaa True jos on valmis """
        if self.Sana.lower() == self.ArvausSana.lower():
            return True
        return False

    def vahennus_tarkistus(self, oliKirjain: bool) -> bool:
        """ Suoritaa vahenna_arvaus_maaraa ja clearaa terminaalin. return True jos hävisit """
        if not oliKirjain:
            havio = self.vahenna_arvaus_maaraa()
            if havio:
                self.tyhjenna_terminaali()
                return True
        return False

    def vahenna_arvaus_maaraa(self) -> bool:
        """ Vähentää Arvaus määrää ja jos se menee 0 niin palauttaa True """

        self.ArvausMaara -= 1
        if self.ArvausMaara == 0:
            return True
        return False

    def lisaa_kirjain(self, index: int, kirjain: str) -> bool:
        """ Lisää arvatun kirjaimen Arvaus Sanaan, jos kirjain on jo siinä niin palautaa False """
        sana = self.ArvausSana

        if sana[index] == kirjain:
            return False

        self.ArvausSana = sana[:index] + kirjain + sana[index + 1:]
        return True

if __name__ == "__main__":
    print("Pyöritä main.py")
    input("Paina Enter")