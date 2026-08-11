from random import choice
from colors import Color
import os
import subprocess
import string

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
        self.Sana = ""
        self.ArvausSana = ""
        self.ArvausMaara = arvausMaara
        self.IsoinArvausMäärä = arvausMaara
        self.SanatPolku = sanatPolku
        self.AnnetutKirjaimet = ""
        self.Break = False

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
        subprocess.run(["clear"], shell=True)


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
            if debug: print(self.Sana)
            print("Kirjoita Lopeta jos haluat lopettaa tai paina ctrl + c")
            print()
            self.piirra_tikkiukko()
            self.piirra_arvaus()

            try:
                kirjain = str(input("Arvaa kirjain: "))
            except KeyboardInterrupt:
                self.cls()
                self.Break = True
                break


            if kirjain.lower() == "lopeta":
                self.cls()
                break
            
            kirjain = kirjain.replace(" ", "")
            if kirjain == "":
                continue
            
            if len(kirjain) > 1:

                kirjaimet = [k for k in kirjain if k not in self.AnnetutKirjaimet]

                for k in kirjaimet:
                    oliKirjain, kirjainLaitettu = self.tarkista_kirjain(k)

                    if not kirjainLaitettu:
                        continue

                    if self.vahennus_tarkistus(oliKirjain):
                        loopiBreak = True
                        break
                    
            else:

                if any([k for k in kirjain if k in self.AnnetutKirjaimet]):
                    continue
                
                oliKirjain, kirjainLaitettu = self.tarkista_kirjain(kirjain)

                if not kirjainLaitettu:
                    print("Olet jo antanut tämän kirjaimen.")
                    continue
                
                if self.vahennus_tarkistus(oliKirjain):
                    loopiBreak = True
                
            if self.sana_tarkistus():
                self.cls()
                print(f"""{Color.OKGREEN}
████████████████████████████████████████████████████████████████████████████████████████████████
██                                                                                            ██ 
██                                                                                            ██ 
██     ██╗   ██╗ ██████╗ ██╗████████╗██╗████████╗    ██████╗ ███████╗██╗     ██╗███╗   ██╗    ██
██     ██║   ██║██╔═══██╗██║╚══██╔══╝██║╚══██╔══╝    ██╔══██╗██╔════╝██║     ██║████╗  ██║    ██
██     ██║   ██║██║   ██║██║   ██║   ██║   ██║       ██████╔╝█████╗  ██║     ██║██╔██╗ ██║    ██
██     ╚██╗ ██╔╝██║   ██║██║   ██║   ██║   ██║       ██╔═══╝ ██╔══╝  ██║     ██║██║╚██╗██║    ██
██      ╚████╔╝ ╚██████╔╝██║   ██║   ██║   ██║       ██║     ███████╗███████╗██║██║ ╚████║    ██
██       ╚═══╝   ╚═════╝ ╚═╝   ╚═╝   ╚═╝   ╚═╝       ╚═╝     ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝    ██
██                                                                                            ██
██                                                                                            ██
████████████████████████████████████████████████████████████████████████████████████████████████
                {Color.ENDC}""")
                print(f"{Color.OKGREEN}Sana: {self.Sana}")
                print(Color.ENDC, end="")

                color = Color.OKGREEN if (self.IsoinArvausMäärä - self.ArvausMaara) < (self.IsoinArvausMäärä / 2) else Color.FAIL
                print(f"{color}Väärin annettu: {self.IsoinArvausMäärä - self.ArvausMaara}")
                print(Color.ENDC)
                break

            if loopiBreak:
                #print(f"{Color.FAIL}Hävisit Pelin!{Color.ENDC}")
                print(f"""{Color.FAIL}
██████████████████████████████████████████████████████████████████████████████████████████████████████
██                                                                                                  ██
██                                                                                                  ██
██     ██╗  ██╗ █████╗ ██╗   ██╗██╗███████╗██╗████████╗    ██████╗ ███████╗██╗     ██╗███╗   ██╗    ██
██     ██║  ██║██╔══██╗██║   ██║██║██╔════╝██║╚══██╔══╝    ██╔══██╗██╔════╝██║     ██║████╗  ██║    ██
██     ███████║███████║██║   ██║██║███████╗██║   ██║       ██████╔╝█████╗  ██║     ██║██╔██╗ ██║    ██
██     ██╔══██║██╔══██║╚██╗ ██╔╝██║╚════██║██║   ██║       ██╔═══╝ ██╔══╝  ██║     ██║██║╚██╗██║    ██
██     ██║  ██║██║  ██║ ╚████╔╝ ██║███████║██║   ██║       ██║     ███████╗███████╗██║██║ ╚████║    ██
██     ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝╚═╝   ╚═╝       ╚═╝     ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝    ██
██                                                                                                  ██
██                                                                                                  ██
██████████████████████████████████████████████████████████████████████████████████████████████████████
                {Color.ENDC}""")
                print(f"{Color.OKGREEN}Sana oli: {self.Sana}{Color.ENDC}")
                break


    def piirra_arvaus(self):
        print(Color.OKCYAN)
        print(f"Arvaus Määrä: {self.ArvausMaara}")
        print(Color.ENDC)
        self.piirra_testatut_kirjaimet()
        print()
        #print("Testatut Kirjaimet: " + f"{Color.FAIL if },".join(self.AnnetutKirjaimet))
        print(" ".join(self.ArvausSana))

    def piirra_testatut_kirjaimet(self):
        print("Testatut Kirjaimet: ", end="")
        for i, k in enumerate(self.AnnetutKirjaimet):
            color = Color.OKGREEN if k in self.Sana else Color.FAIL

            print(f"{"|" if i > 0 else ""}{color}{k}{Color.ENDC}", end="")

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
        
        if arvausKirjain not in self.AnnetutKirjaimet:
            self.AnnetutKirjaimet += arvausKirjain.lower()
        
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
                #self.piirra_tikkiukko()
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

if __name__ == "__main__":
    print("Ei tee mitään")