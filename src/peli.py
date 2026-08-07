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
                if sana in sanat:
                    continue
                sanat.append(sana)
        self.valitse_sana(sanat)


    def valitse_sana(self, sanat: list[str]):
        """ Valitsee Sanat listasta satunnaisen sanan. """
        self.Sana = choice(sanat)
        self.ArvausSana = "_" * (len(self.Sana) - 1)

    def aloitus(self):
        """ Aloitaa pelin loopin """

        self.lue_sanat_tiedosto(self.SanatPolku)
        print(self.Sana)

        while True:
            self.piirra_arvaus()

            kirjain = str(input("Arvaa kirjain: "))
            if kirjain == "":
                break

            if not self.tarkista_kirjain(kirjain):
                havio = self.vahenna_aravuas_maaraa()
                if havio: break

            

            

    
    def piirra_arvaus(self):
        print(f"Arvaus Määrä: {self.ArvausMaara}")
        print(" ".join(self.ArvausSana))

    def tarkista_kirjain(self, arvausKirjain: str) -> bool:
        """ Tarkistaa onko kirjain sanassa jos on niin palautaa True """
        tulos = False

        for i, kirjain in enumerate(self.Sana):
            if kirjain == arvausKirjain:
                self.lisaa_kirjain(i, kirjain)
                tulos = True
        
        return tulos

    def vahenna_aravuas_maaraa(self):
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