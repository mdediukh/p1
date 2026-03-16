import sys, os, uuid
from PyQt5 import QtWidgets, uic
 
class MainWindow(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
 
        uic.loadUi(r"D:\student\Bozek\Maksym_Dediukh\Biblioteka_UI.ui", self)
        self.AutorComboBox.addItems(['Adam Mickiewicz', 'Jan Kochanowski', 'Juliusz Słowacki'])
        self.ZalozBaze.clicked.connect(self.zaloz_baze)
        self.ZalozKonto.clicked.connect(self.zaloz_uzytkownika)
        self.pobierz()
 
    def pobierz(self):
        print('test')
 
    def zaloz_uzytkownika(self):
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
                            odczyt_uzytkownik.write(str(self.u_imie) + '#' +str(self.u_imie)+ '#' + str(self.uid_uzytkownik+ '\n'))

    def zaloz_baze(self):
 
        self.lista_plikow = ['uzytkownik.txt', 'ksiazki_dostepne.txt', 'ksiazki_wypozyczone.txt']
        self.LokalizacjaBazy = self.LokalizacjaBazy.toPlainText().strip()
 
        for plik in self.lista_plikow:
 
            plik = self.LokalizacjaBazy + '\\' + plik
 
            if os.path.exists(plik):
                print(f'Plik_istnieje: {plik}')
               
            elif not os.path.exists(plik):
                with open(plik, 'w') as zapis:
                    print(f'Tworze: {plik}')
 
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())