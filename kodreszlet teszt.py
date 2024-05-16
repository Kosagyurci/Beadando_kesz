# Szoba osztály

from abc import ABC, abstractmethod

class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam
        self.foglalasok = []

    @abstractmethod
    def get_szolgaltatasok(self):
        pass

    def __str__(self):
        return f"Szoba {self.szobaszam}, Ár: {self.ar} Ft"


# Egy és két ágyas szoba

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(5000, szobaszam)  # Egyágyas szoba ára: 5000 Ft

    def get_szolgaltatasok(self):
        return ["Ingyenes wifi", "TV", "Fürdőszoba"]

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(8000, szobaszam)  # Kétágyas szoba ára: 8000 Ft

    def get_szolgaltatasok(self):
        return ["Ingyenes wifi", "TV", "Fürdőszoba", "Konyha használat"]


# Szálloda osztály

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def uj_szoba(self, szoba):
        self.szobak.append(szoba)

    def osszes_szoba_ar(self):
        osszeg = 0
        for szoba in self.szobak:
            osszeg += szoba.ar
        return osszeg

    def foglalasok_listazasa(self):
        if not self.szobak:
            print("Nincsenek foglalások.")
        else:
            print("Foglalások listája:")
            for szoba in self.szobak:
                for foglalas in szoba.foglalasok:
                    print(f"Foglalás a {szoba.szobaszam} számú szobára, dátum: {foglalas.datum}")

    def foglalas_lemondasa(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                for foglalas in szoba.foglalasok:
                    if foglalas.datum == datum:
                        szoba.foglalasok.remove(foglalas)
                        print("A foglalás sikeresen lemondva.")
                        return
                print("A megadott foglalás nem található.")
                return
        print("A megadott szobaszám nem található.")

    def foglalas_lehetseges(self, szoba, datum):
        from datetime import datetime

        # Ellenőrizzük, hogy a dátum jövőbeni-e
        try:
            foglalas_datum = datetime.strptime(datum, "%Y-%m-%d")
            if foglalas_datum < datetime.today():
                print("A megadott dátum már elmúlt.")
                return False
        except ValueError:
            print("Hibás dátumformátum. Kérem használja az ÉÉÉÉ-HH-NN formátumot.")
            return False

        # Ellenőrizzük, hogy a szoba elérhető-e az adott dátumon
        for foglalas in szoba.foglalasok:
            if foglalas.datum == datum:
                print("A megadott szoba már foglalt ezen a dátumon.")
                return False

        return True

    def szoba_foglalasa(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                if self.foglalas_lehetseges(szoba, datum):
                    foglalas = Foglalas(szoba, datum)
                    szoba.foglalasok.append(foglalas)
                    return szoba.ar
                else:
                    return None
        return None


# Foglalas osztály

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

    def __str__(self):
        return f"Foglalás a {self.szoba.szobaszam} számú szobára, dátum: {self.datum}"


# Feltöltés

def feltoltes(szalloda):
    egyagyas1 = EgyagyasSzoba("101")
    egyagyas2 = EgyagyasSzoba("102")
    ketagyas1 = KetagyasSzoba("201")
    szalloda.uj_szoba(egyagyas1)
    szalloda.uj_szoba(egyagyas2)
    szalloda.uj_szoba(ketagyas1)

    foglalas1 = Foglalas(egyagyas1, "2024-06-01")
    foglalas2 = Foglalas(egyagyas1, "2024-06-05")
    foglalas3 = Foglalas(egyagyas2, "2024-06-02")
    foglalas4 = Foglalas(ketagyas1, "2024-06-03")
    foglalas5 = Foglalas(ketagyas1, "2024-06-07")
    egyagyas1.foglalasok.extend([foglalas1, foglalas2])
    egyagyas2.foglalasok.append(foglalas3)
    ketagyas1.foglalasok.extend([foglalas4, foglalas5])


# Felhasználói interfész

def main():
    szalloda = Szalloda("Példa Szálloda")
    feltoltes(szalloda)

    while True:
        print("\nVálasszon műveletet:")
        print("1. Szoba foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("0. Kilépés")

        valasztas = input("Kérem válasszon egy számot: ")

        if valasztas == "1":
            szobaszam = input("Adja meg a foglalni kívánt szoba számát: ")
            datum = input("Adja meg a foglalás dátumát (ÉÉÉÉ-HH-NN formátumban): ")
            ar = szalloda.szoba_foglalasa(szobaszam, datum)
            if ar is not None:
                print(f"A foglalás sikeres. Az ára: {ar} Ft.")
            else:
                print("A foglalás sikertelen.")

        elif valasztas == "2":
            szobaszam = input("Adja meg a lemondani kívánt foglalás szobaszámát: ")
            datum = input("Adja meg a lemondani kívánt foglalás dátumát (ÉÉÉÉ-HH-NN formátumban): ")
            szalloda.foglalas_lemondasa(szobaszam, datum)

        elif valasztas == "3":
            szalloda.foglalasok_listazasa()

        elif valasztas == "0":
            print("Kilépés...")
            break

        else:
            print("Érvénytelen választás. Kérem válasszon újra.")

if __name__ == "__main__":
    main()
