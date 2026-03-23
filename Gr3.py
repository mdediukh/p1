
#ETO VSE

#POLNAJA ZALUPA

#I ETO VSE

#NADO PEREDELYVAT 



import sys, os, uuid
from PyQt5 import QtWidgets, uic
 
class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"D:\student\Bozek\Maksym_Dediukh\Biblioteka_UI.ui", self)
        self.AutorComboBox.addItems(['Adam Mickiewicz', 'Jan Kochanowski', 'Juliusz Słowacki'])
        self.ZalozBaze.clicked.connect(self.zaloz_baze)
        self.ZalozKonto.clicked.connect(self.zaloz_uzytkownika)

        #self.pobierz()
        #self.AutorComboBox.setEditable(True)
        #self.TytulComboBox.setEditable(True)
        #self.GatunekComboBox.setEditable(True)
        #self.RokComboBox.setEditable(True)
        #self.ISBNComboBox.setEditable(True)
 
    def pobierz(self):
        print('test')
 
    def zaloz_baze(self):
        self.lista_plikow = ['uzytkownik.txt', 'ksiazki_dostepne.txt', 'ksiazki_wypozyczone.txt']
        self.LokalizacjaBazy = self.LokalizacjaBazy.toPlainText().strip()
        self.aktualny_uzytkownik = None
 
        '''for plik in self.lista_plikow:
 
            plik = self.LokalizacjaBazy + '\\' + plik
 
            if os.path.exists(plik):
                print(f'Plik_istnieje: {plik}')
               
            elif not os.path.exists(plik):
                with open(plik, 'w') as zapis:
                    print(f'Tworze: {plik}')'''
        
        for plik in self.lista_plikow:
            plik = self.LokalizacjaBazy + '\\' + plik
            if os.path.exists(plik):
                print(f'plik istnieje {plik}')
            elif not os.path.exists(plik):
                with open(plik,'w') as zapis:
                    print(f'tworze {plik}')


    def zaloz_uzytkownika(self):
        #self.LokalizacjaBazy = self.te_konfig__baza.toPlainText().strip()
        plik_uzytkownika = self.LokalizacjaBazy + '\\' + self.lista_plikow[0]
        if os.path.exists(plik_uzytkownika):
            print(plik_uzytkownika)
            self.u_imie = self.Imie.toPlainText().strip()
            self.u_nazwisko = self.Nazwisko.toPlainText().strip()
            self.uid_uzytkownik = uuid.uuid4().hex
            print(self.u_imie, self.u_nazwisko, self.uid_uzytkownik)
            with open(plik_uzytkownika, 'r+', encoding='UTF-8') as odczyt_uzytkownik:
                for numer, line in enumerate(odczyt_uzytkownik):
                    if numer >= 0:
                        s_imie = line.split('#')[0]
                        s_nazwisko = line.split('#')[1]
                        if self.u_imie == s_imie:
                            print('juz {self.u_imie} istnieje')
                        else: 
                            odczyt_uzytkownik.write(str(self.u_imie) + '#' +str(self.u_imie)+ '#' + str(self.uid_uzytkownik) + '\n')                
 
    '''def zaloz_konto(self):
            plik_uzytkownika = self.lok_bazy + '\\' + self.lista_plikow[0]
            if os.path.exists(plik_uzytkownika):
                self.u_imie = self.plain_imie.toPlainText().strip()
                self.u_nazwisko = self.plain_nazwisko.toPlainText().strip()
                self.uid_uzytkownika = uuid.uuid4().hex
                print(self.u_imie, self.u_nazwisko, self.uid_uzytkownika)
                with open(plik_uzytkownika, 'r+', encoding='UTF-8') as odczyt_uzytkownik:
                    for numer, line in enumerate(odczyt_uzytkownik):
                        if numer >= 0:
                            s_imie = line.split('#')[0]
                            s_nazwisko = line.split('#')[1]
                            if self.u_imie == s_imie:
                                print(f'już {self.u_imie} istnieje')
                            else:
                                odczyt_uzytkownik.write(str(self.u_imie) + '#' + str(self.u_nazwisko)+ '#' +str(self.uid_uzytkownika) + '\n')'''

    
    def zaloguj_uzytkownika(self):
        self.uzytkownik_imie = self.te_imie.toPlainText().strip()
        self.uzytkownik_nazwisko = self.te_nazwisko.toPlainText().strip()
        self.aktualny_uzytkownik = str(self.uzytkownik_imie) + str(self.uzytkownik_nazwisko)
        print(self.aktualny_uzytkownik)

    def dodaj_ksiazke(self):
        self_ksiazka_tytul = self.TytulComboBox.currentText().strip()
        self_ksiazka_autor = self.AutorComboBox.currentText().strip()
        self_ksiazka_gatunek = self.GatunekComboBox.currentText().strip()
        self_ksiazka_rok = self.RokComboBox.currentText().strip()
        self_ksiazka_isbn = self.ISBNComboBox.currentText().strip()
        #if self_ksiazka_tytul == ' ' or self.ksiazka_autor == or self_ksiazka_isbn:
        #    QMessageBox.critical(self, "Błąd")
        #    return
        #plik_ksiazki_dostepne = self.LokalizacjaBazy + '\\' + self.lista_plikow
        #if os.path.exists(plik_ksiazki_dostepne):
        #    with open

    


 
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())