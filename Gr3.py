import sys, os, uuid
from PyQt5 import QtWidgets, uic
 
class MainWindow(QtWidgets.QDialog):
    def accept(self):
        pass
    def reject(self):
        pass
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Biblioteka_UI.ui", self)
        self.AutorComboBox.addItems(['Adam Mickiewicz', 'Jan Kochanowski', 'Juliusz Słowacki'])
        self.ZalozBaze.clicked.connect(self.zaloz_baze)
        self.ZalozKonto.clicked.connect(self.zaloz_uzytkownika)
        self.Zaloguj.clicked.connect(self.zaloguj_uzytkownika)
        self.Dodaj.clicked.connect(self.dodaj_ksiazke)
        self.Zwroc.clicked.connect(self.zwroc_ksiazke)
        self.Wypozycz.clicked.connect(self.wypozycz_ksiazke)
 
    def pobierz(self):
        print('test')
 
    def zaloz_baze(self):
        self.lista_plikow = ['uzytkownik.txt', 'ksiazki_dostepne.txt', 'ksiazki_wypozyczone.txt']
        self.LokalizacjaBazy = self.LokalizacjaBazy.toPlainText().strip()
        self.aktualny_uzytkownik = None
        
        for plik in self.lista_plikow:
            plik = self.LokalizacjaBazy + '\\' + plik
            if os.path.exists(plik):
                print(f'plik istnieje {plik}')
            elif not os.path.exists(plik):
                with open(plik,'w') as zapis:
                    print(f'tworze {plik}')


    def zaloz_uzytkownika(self):
        plik_uzytkownika = self.LokalizacjaBazy + '\\' + self.lista_plikow[0]
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
        self.aktualny_uzytkownik = str(self.uzytkownik_imie) + str(self.uzytkownik_nazwisko)
        print(self.aktualny_uzytkownik)

    def dodaj_ksiazke(self):
        self_ksiazka_tytul = self.TytulComboBox.currentText().strip()
        self_ksiazka_autor = self.AutorComboBox.currentText().strip()
        self_ksiazka_gatunek = self.GatunekComboBox.currentText().strip()
        self_ksiazka_rok = self.RokComboBox.currentText().strip()
        self_ksiazka_isbn = self.ISBNComboBox.currentText().strip()
        uid_ksiazki = uuid.uuid4().hex 
        plik_ksiazki = self.LokalizacjaBazy + '\\' + self.lista_plikow[1]
        if os.path.exists(plik_ksiazki):
            with open(plik_ksiazki, 'a', encoding='UTF-8') as zapis:
                zapis.write(f"{self_ksiazka_autor}#{self_ksiazka_tytul}#{self_ksiazka_gatunek}#{self_ksiazka_rok}#{self_ksiazka_isbn}#{uid_ksiazki}\n")
                print(f"Dodano książkę: {self_ksiazka_tytul} z ID: {uid_ksiazki}")
                
    def odswiez_listy(self):
        self.TytulComboBox.clear()
        self.Tytul_2ComboBox.clear()
        p_dostepne = self.LokalizacjaBazy + '\\' + self.lista_plikow[1]
        if os.path.exists(p_dostepne):
            with open(p_dostepne, 'r', encoding='UTF-8') as f:
                for line in f:
                    dane = line.strip().split('#')
                    if len(dane) >= 2:
                        self.TytulComboBox.addItem(dane[1])
        p_wypozyczone = self.LokalizacjaBazy + '\\' + self.lista_plikow[2]
        if os.path.exists(p_wypozyczone) and self.aktualny_uzytkownik:
            with open(p_wypozyczone, 'r', encoding='UTF-8') as f:
                for line in f:
                    dane = line.strip().split('#')
                    if len(dane) >= 7 and dane[6] == self.aktualny_uzytkownik:
                        self.Tytul_2ComboBox.addItem(dane[1])
    
    def wypozycz_ksiazke(self):
        if not self.aktualny_uzytkownik:
            print("Najpierw się zaloguj!")
            return
        tytul = self.TytulComboBox.currentText()
        if not tytul: return
        p_dostepne = self.LokalizacjaBazy + '\\' + self.lista_plikow[1]
        p_wypozyczone = self.LokalizacjaBazy + '\\' + self.lista_plikow[2]
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
        p_dostepne = self.LokalizacjaBazy + '\\' + self.lista_plikow[1]
        p_wypozyczone = self.LokalizacjaBazy + '\\' + self.lista_plikow[2]
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