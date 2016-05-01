import sys
from PyQt5.QtWidgets import *
from tnb_gui import Ui_MainWindow
from os.path import *

app = QApplication(sys.argv)
app.setStyle(QStyleFactory.create("Fusion"))
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
ui.stackedWidget.setCurrentIndex(0)
def goto(id, name=""):
    if id == -1:
        ui.stackedWidget.setCurrentIndex(0)
    else:
        ui.pages.setCurrentIndex(id)
        ui.stackedWidget.setCurrentIndex(1)
        ui.lbl_pageTitle.setText(name)
    if name == "Application":
        ui.groupBox_4.setTitle("Infos sur l'application")
    elif name == "Jeu":
        ui.groupBox_4.setTitle("Infos sur le jeu")

def path_leaf(path):
    #head, tail = splitext(path)
    #return head or basename(head)
    return splitext(basename(path))[0]

def audio_addFiles():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.ExistingFiles)
    fnames = dialog.getOpenFileNames(None, "Fichiers audio", expanduser("~"), "Fichiers audio (*.aac *.ac3 *.aif *.alac *.flac *.ape *.m4a *.mp3 *.mpc *.ogg *.wav *.wv *.wma)")[0]
    for file in fnames:
        if(isfile(file)):
            rowPos = ui.audio_files.rowCount()
            ui.audio_files.insertRow(rowPos)
            ui.audio_files.setItem(rowPos, 1, QTableWidgetItem(path_leaf(file)))

ui.btnAppli.clicked.connect(lambda: goto(4, "Application"))
ui.btnAudio.clicked.connect(lambda: goto(0, "Audio"))
ui.btnEBook.clicked.connect(lambda: goto(1, "eBook"))
ui.btnEBooks.clicked.connect(lambda: goto(2, "eBooks"))
ui.btnJeu.clicked.connect(lambda: goto(4, "Jeu"))
ui.btnVideo.clicked.connect(lambda: goto(3, "Vidéo"))
ui.btnGoHome.clicked.connect(lambda: goto(-1))
ui.audio_addFiles.clicked.connect(audio_addFiles)

window.show()
sys.exit(app.exec_())

