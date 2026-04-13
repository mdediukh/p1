import sys, os, uuid
from PyQt5 import QtWidgets, uic
 
class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"C:\Users\student\Downloads\Biblioteka_UI.ui", self)
        self.ZalozBaze.clicked.connect(self.zaloz_baze)
        self.ZalozKonto.clicked.connect(self.zaloz_uzytkownika)
        self.Zaloguj.clicked.connect(self.zaloguj_uzytkownika)
        self.Dodaj.clicked.connect(self.dodaj_ksiazke)
        self.Zwroc.clicked.connect(self.zwroc_ksiazke)
        self.Wypozycz.clicked.connect(self.wypozycz_ksiazke)

        self.szlak = ""
        self.blokuj_sync = False 
        self.aktualny_uzytkownik = None

        self.AutorComboBox.activated[str].connect(self.synchronizuj_pola)
        self.TytulComboBox.activated[str].connect(self.synchronizuj_pola)
        self.GatunekComboBox.activated[str].connect(self.synchronizuj_pola)
        self.RokComboBox.activated[str].connect(self.synchronizuj_pola)
        self.ISBNComboBox.activated[str].connect(self.synchronizuj_pola)
 
    def pobierz(self):
        print('test')

    def synchronizuj_pola(self, tekst):
        if self.blokuj_sync or not tekst or not self.szlak:
            return
        
        nadawca = self.sender()
        indeks = 0 if nadawca == self.AutorComboBox else 1 if nadawca == self.TytulComboBox else 2 if nadawca == self.GatunekComboBox else 3 if nadawca == self.RokComboBox else 4
        
        p_dostepne = self.szlak + '\\' + self.lista_plikow[1]
        if os.path.exists(p_dostepne):
            with open(p_dostepne, 'r', encoding='UTF-8') as f:
                for line in f:
                    dane = line.strip().split('#')
                    if len(dane) >= 6 and dane[indeks] == tekst:
                        self.blokuj_sync = True
                        self.AutorComboBox.setCurrentText(dane[0])
                        self.TytulComboBox.setCurrentText(dane[1])
                        self.GatunekComboBox.setCurrentText(dane[2])
                        self.RokComboBox.setCurrentText(dane[3])
                        self.ISBNComboBox.setCurrentText(dane[4])
                        self.blokuj_sync = False
                        break
 
    def zaloz_baze(self):
        self.lista_plikow = ['uzytkownik.txt', 'ksiazki_dostepne.txt', 'ksiazki_wypozyczone.txt']
        self.szlak = self.LokalizacjaBazy.toPlainText().strip()
        self.aktualny_uzytkownik = None
        
        for plik in self.lista_plikow:
            pelny_plik = self.szlak + '\\' + plik
            if os.path.exists(pelny_plik):
                print(f'plik istnieje {pelny_plik}')
            elif not os.path.exists(pelny_plik):
                os.makedirs(self.szlak, exist_ok=True)
                with open(pelny_plik,'w') as zapis:
                    print(f'tworze {pelny_plik}')
        self.odswiez_listy()

    def zaloz_uzytkownika(self):
        plik_uzytkownika = self.LokalizacjaBazy.toPlainText().strip() + '\\' + self.lista_plikow[0]
        if os.path.exists(plik_uzytkownika):
            print(plik_uzytkownika)
            self.u_imie = self.Imie.toPlainText().strip()
            self.u_nazwisko = self.Nazwisko.toPlainText().strip()
            self.uid_uzytkownik = uuid.uuid4().hex
            print(self.u_imie, self.u_nazwisko, self.uid_uzytkownik)
            with open(plik_uzytkownika, 'r+', encoding='UTF-8') as odczyt_uzytkownik:
                linie = odczyt_uzytkownik.readlines()
                istnieje = False
                for line in linie:
                    if line.startswith(self.u_imie + '#'):
                        print(f'juz {self.u_imie} istnieje')
                        istnieje = True
                        break
                if not istnieje:
                    odczyt_uzytkownik.write(f"{self.u_imie}#{self.u_nazwisko}#{self.uid_uzytkownik}\n")  
                    
    def zaloguj_uzytkownika(self):
        self.uzytkownik_imie = self.Imie.toPlainText().strip()
        self.uzytkownik_nazwisko = self.Nazwisko.toPlainText().strip()
        
        if not self.szlak: return
        p_uzytk = self.szlak + '\\' + self.lista_plikow[0]
        if os.path.exists(p_uzytk):
            with open(p_uzytk, 'r', encoding='UTF-8') as f:
                for line in f:
                    dane = line.strip().split('#')
                    if len(dane) >= 3 and dane[0] == self.uzytkownik_imie and dane[1] == self.uzytkownik_nazwisko:
                        self.aktualny_uzytkownik = dane[2]
                        print(f"Zalogowano UUID: {self.aktualny_uzytkownik}")
                        self.odswiez_listy()
                        return
        print("Użytkownik nie istnieje!")

    def dodaj_ksiazke(self):
        self_ksiazka_tytul = self.TytulComboBox.currentText().strip()
        self_ksiazka_autor = self.AutorComboBox.currentText().strip()
        self_ksiazka_gatunek = self.GatunekComboBox.currentText().strip()
        self_ksiazka_rok = self.RokComboBox.currentText().strip()
        self_ksiazka_isbn = self.ISBNComboBox.currentText().strip()
        uid_ksiazki = uuid.uuid4().hex 
        
        if not self.szlak: return
        plik_ksiazki = self.szlak + '\\' + self.lista_plikow[1]
        if os.path.exists(plik_ksiazki):
            with open(plik_ksiazki, 'a', encoding='UTF-8') as zapis:
                zapis.write(f"{self_ksiazka_autor}#{self_ksiazka_tytul}#{self_ksiazka_gatunek}#{self_ksiazka_rok}#{self_ksiazka_isbn}#{uid_ksiazki}\n")
                print(f"Dodano książkę: {self_ksiazka_tytul} z ID: {uid_ksiazki}")
        self.odswiez_listy()
                
    def odswiez_listy(self):
        if not getattr(self, 'szlak', None): return
        self.blokuj_sync = True
        
        for combo in [self.AutorComboBox, self.TytulComboBox, self.GatunekComboBox, self.RokComboBox, self.ISBNComboBox, self.Tytul_2ComboBox]:
            combo.clear()
        
        p_dostepne = self.szlak + '\\' + self.lista_plikow[1]
        if os.path.exists(p_dostepne):
            with open(p_dostepne, 'r', encoding='UTF-8') as f:
                for line in f:
                    d = line.strip().split('#')
                    if len(d) >= 6:
                        if self.AutorComboBox.findText(d[0]) == -1: self.AutorComboBox.addItem(d[0])
                        if self.TytulComboBox.findText(d[1]) == -1: self.TytulComboBox.addItem(d[1])
                        if self.GatunekComboBox.findText(d[2]) == -1: self.GatunekComboBox.addItem(d[2])
                        if self.RokComboBox.findText(d[3]) == -1: self.RokComboBox.addItem(d[3])
                        if self.ISBNComboBox.findText(d[4]) == -1: self.ISBNComboBox.addItem(d[4])

        p_wypoz = self.szlak + '\\' + self.lista_plikow[2]
        if os.path.exists(p_wypoz) and getattr(self, 'aktualny_uzytkownik', None):
            with open(p_wypoz, 'r', encoding='UTF-8') as f:
                for line in f:
                    d = line.strip().split('#')
                    if len(d) >= 7 and d[6] == self.aktualny_uzytkownik:
                        self.Tytul_2ComboBox.addItem(d[1])
        
        self.blokuj_sync = False
    
    def wypozycz_ksiazke(self):
        if not self.aktualny_uzytkownik:
            print("Najpierw się zaloguj!")
            return
        tytul = self.TytulComboBox.currentText()
        if not tytul: return
        p_dostepne = self.szlak + '\\' + self.lista_plikow[1]
        p_wypozyczone = self.szlak + '\\' + self.lista_plikow[2]
        dostepne_zostaja = []
        wybrana_ksiazka = ""
        with open(p_dostepne, 'r', encoding='UTF-8') as f:
            for line in f:
                dane = line.strip().split('#')
                if len(dane) >= 2 and dane[1] == tytul and not wybrana_ksiazka:
                    wybrana_ksiazka = line.strip()
                else:
                    dostepne_zostaja.append(line)
        if wybrana_ksiazka:
            with open(p_dostepne, 'w', encoding='UTF-8') as f:
                f.writelines(dostepne_zostaja)
            with open(p_wypozyczone, 'a', encoding='UTF-8') as f:
                f.write(f"{wybrana_ksiazka}#{self.aktualny_uzytkownik}#2026-03-15\n")
            print(f"Wypożyczono: {tytul}")
            self.odswiez_listy()
    
    def zwroc_ksiazke(self):
        tytul = self.Tytul_2ComboBox.currentText()
        if not tytul: return
        p_dostepne = self.szlak + '\\' + self.lista_plikow[1]
        p_wypozyczone = self.szlak + '\\' + self.lista_plikow[2]
        wypozyczone_zostaja = []
        ksiazka_do_zwrotu = ""
        with open(p_wypozyczone, 'r', encoding='UTF-8') as f:
            for line in f:
                dane = line.strip().split('#')
                if len(dane) >= 7 and dane[1] == tytul and dane[6] == self.aktualny_uzytkownik:
                    ksiazka_do_zwrotu = "#".join(dane[:6]) + "\n"
                else:
                    wypozyczone_zostaja.append(line)
        with open(p_wypozyczone, 'w', encoding='UTF-8') as f:
            f.writelines(wypozyczone_zostaja)
        if ksiazka_do_zwrotu:
            with open(p_dostepne, 'a', encoding='UTF-8') as f:
                f.write(ksiazka_do_zwrotu)
        self.odswiez_listy()   
                       
                        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())