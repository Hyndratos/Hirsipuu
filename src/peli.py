from random import choice
from colors import Color
import os

#######
#     |
#     O
#    /|\
#    / \

# x o x o x o x o x o x
# o x o x o x o x o x o
# x o x o x o x o x o x
# o x o x o x o x o x o
# x o x o x o x o x o x
# o x o x o x o x o x o
# x o x o x o x o x o x
# o x o x o x o x o x o
# x o x o x o x o x o x
# o x o x o x o x o x o

class Peli:
    """ Hoitaa kaiken pelin logiikan. """
    TikkuUkot = [
        ["+-----+", "|     |", "|", "|", "|"],
        ["+-----+", "|     |", "|     O", "|", "|"],
        ["+-----+", "|     |", "|     O", "|     |", "|"],
        ["+-----+", "|     |", "|     O", "|     |", "|      \\"],
        ["+-----+", "|     |", "|     O", "|     |", "|    / \\"],
        ["+-----+", "|     |", "|     O", "|     |\\", "|    / \\"],
        ["+-----+", "|     |", "|     O", "|    /|\\", "|    / \\"]
    ]

    def __init__(self, sanatPolku: str, arvausMaara: int):
        self.Sana = ""
        self.ArvausSana = ""
        self.ArvausMaara = arvausMaara
        self.IsoinArvausMäärä = arvausMaara
        self.SanatPolku = sanatPolku

    def lue_sanat_tiedosto(self, polku: str):
        """ Lukee annetun polun tiedoston sanat ja lisää ne listaan. Jonka jälkeen se suoritaa valitse sana"""
        sanat = []
        with open(polku, "r") as tiedosto:
            for sana in tiedosto:
                sana = sana.strip()

                if sana in sanat:
                    continue

                sanat.append(sana)

        self.valitse_sana(sanat)

    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')


    def valitse_sana(self, sanat: list[str]):
        """ Valitsee Sanat listasta satunnaisen sanan. """
        self.Sana = choice(sanat)
        self.ArvausSana = "_" * len(self.Sana)

    def aloitus(self):
        """ Aloitaa pelin loopin """
        loopiBreak = False
        self.lue_sanat_tiedosto(self.SanatPolku)
        while True:
            self.cls()
            print(self.Sana)
            print("Kirjoita Lopeta jos haluat lopettaa tai paina ctrl + c")
            print()
            self.piirra_tikkiukko()

            self.piirra_arvaus()
            try:
                kirjain = str(input("Arvaa kirjain: "))
            except KeyboardInterrupt:
                self.cls()
                break

            if kirjain.lower() == "lopeta":
                self.cls()
                break

            if len(kirjain) > 1:
                for k in kirjain:
                    oliKirjain, kirjainLaitettu = self.tarkista_kirjain(k)

                    if not kirjainLaitettu:
                        continue

                    if self.vahennus_tarkistus(oliKirjain):
                        break
            else:

                oliKirjain, kirjainLaitettu = self.tarkista_kirjain(kirjain)

                if not kirjainLaitettu:
                    print("Olet jo antanut tämän kirjaimen.")
                    continue
                
                if self.vahennus_tarkistus(oliKirjain):
                    break
                
            if self.sana_tarkistus():
                self.cls()
                print("Arvasit koko sanan")
                print(f"{Color.OKGREEN}Sana: {self.Sana}")
                print(Color.ENDC, end="")

                color = Color.OKGREEN if (self.IsoinArvausMäärä - self.ArvausMaara) < (self.IsoinArvausMäärä / 2) else Color.FAIL
                print(f"{color}Väärin annettu: {self.IsoinArvausMäärä - self.ArvausMaara}")
                print(Color.ENDC)
                break

            if loopiBreak:
                self.cls()
                break


    def piirra_arvaus(self):
        print(Color.OKCYAN)
        print(f"Arvaus Määrä: {self.ArvausMaara}")
        print(Color.ENDC, end="")
        print(" ".join(self.ArvausSana))

    def piirra_tikkiukko(self):
        for rivi in self.TikkuUkot[self.IsoinArvausMäärä - self.ArvausMaara]:
            print(Color.FAIL, end="")
            print(rivi)
            print(Color.ENDC, end="")

    def tarkista_kirjain(self, arvausKirjain: str) -> tuple[bool, bool]:
        """ Tarkistaa onko kirjain sanassa jos on niin palautaa True """
        oliKirjain = False
        kirjainLaitettu = True

        for i, kirjain in enumerate(self.Sana):
            if kirjain == arvausKirjain:
                kirjainLaitettu = self.lisaa_kirjain(i, kirjain)
                oliKirjain = True
        
        return (oliKirjain, kirjainLaitettu)

    def sana_tarkistus(self) -> bool:
        """ Tarkistaa onko arvattu sana sama kuin sana ja palautaa True jos on valmis """
        if self.Sana.lower() == self.ArvausSana.lower():
            return True
        return False

    def vahennus_tarkistus(self, oliKirjain: bool) -> bool:
        if not oliKirjain:
            havio = self.vahenna_aravuas_maaraa()
            if havio:
                self.cls()
                self.piirra_tikkiukko()
                print(f"{Color.OKGREEN}Sana oli: {self.Sana}")
                return True
        return False

    def vahenna_aravuas_maaraa(self) -> bool:
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