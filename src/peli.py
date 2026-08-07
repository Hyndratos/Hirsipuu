from random import choice

class Peli:
    """ Hoitaa kaiken pelin logiikan. """
    def __init__(self, sanatPolku: str, arvausMaara: int):
        self.Sana = ""
        self.ArvausSana = ""
        self.ArvausMaara = arvausMaara
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


    def valitse_sana(self, sanat: list[str]):
        """ Valitsee Sanat listasta satunnaisen sanan. """
        self.Sana = choice(sanat)
        self.ArvausSana = "_" * len(self.Sana)

    def aloitus(self):
        """ Aloitaa pelin loopin """

        self.lue_sanat_tiedosto(self.SanatPolku)
        print(self.Sana)
        print("Kirjoita Lopeta jos haluat lopettaa")
        while True:
            self.piirra_arvaus()

            try:
                kirjain = str(input("Arvaa kirjain: "))
            except KeyboardInterrupt:
                print("\nLopetit pelin.")
                break

            if kirjain.lower() == "lopeta":
                print("\nLopetit pelin.")
                break

            oliKirjain, kirjainLaitettu = self.tarkista_kirjain(kirjain)

            if self.sana_tarkistus():
                print("Arvasit koko sanan")
                break

            if not kirjainLaitettu:
                print("Olet jo antanut tämän kirjaimen.")
                continue
            
            if not oliKirjain:
                havio = self.vahenna_aravuas_maaraa()
                if havio: break


            

            

    
    def piirra_arvaus(self):
        print(f"Arvaus Määrä: {self.ArvausMaara}")
        print(" ".join(self.ArvausSana))

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