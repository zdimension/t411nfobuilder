import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from tnb_gui import Ui_MainWindow
import os
import datetime
import textwrap

NFO_WIDTH = 69

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def sizeof_fmt(num, suffix='o'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)

def sztxt(p):
    return sizeof_fmt(get_size(p))

app = QApplication(sys.argv)
app.setStyle(QStyleFactory.create("Fusion"))
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
ui.stackedWidget.setCurrentIndex(0)

def getCurPage():
    return ui.pages.currentIndex()

def firmV(v):
    if(v):
        ui.formLayout_10.insertRow(3, ui.con_lblFirmw, ui.con_firmw)
        ui.con_lblFirmw.show()
        ui.con_firmw.show()
    else:
        ui.con_firmw.hide()
        ui.con_firmw.setText("")
        ui.con_lblFirmw.hide()
        ui.formLayout_10.removeWidget(ui.con_firmw)
        ui.formLayout_10.removeWidget(ui.con_lblFirmw)
firmV(False)

def loadCon(id):
    if id == 0: # Microsoft
        ui.con_console.clear()
        ui.con_console.addItems(["Xbox", "Xbox 360", "Xbox One"])
    elif id == 1: # Nintendo
        ui.con_console.clear()
        ui.con_console.addItems(["3DS", "DS", "GameCube", "Wii", "Wii U"])
    elif id == 2: # Sony
        ui.con_console.clear()
        ui.con_console.addItems(["PlayStation", "PlayStation 2", "PlayStation 3", "PlayStation 4", "PlayStation Portable", "PlayStation Vita"])
    ui.con_console.setCurrentIndex(-1)

def ebookdim(v):
    if(v):
        ui.formLayout_5.insertRow(11, ui.lblDim, ui.ebook_dimensions)
        ui.lblDim.show()
        ui.ebook_dimensions.show()
    else:
        ui.ebook_dimensions.hide()
        ui.ebook_dimensions.setText("")
        ui.lblDim.hide()
        ui.formLayout_5.removeWidget(ui.ebook_dimensions)
        ui.formLayout_5.removeWidget(ui.lblDim)
ebookdim(False)

ui.con_type.currentIndexChanged.connect(lambda index: loadCon(index))
ui.con_console.currentIndexChanged.connect(lambda index: firmV(ui.con_type.currentIndex() == 2 and index in [2, 4]))
ui.ebook_format.currentIndexChanged.connect(lambda index: ebookdim(index in [1, 2, 3, 4, 5, 9, 12]))
ui.app_os.currentIndexChanged.connect(lambda index: ui.app_swCon.setCurrentIndex(index == 4))
ui.app_swCon.setCurrentIndex(0)



def goto(id, name=""):
    if id == -1:
        ui.stackedWidget.setCurrentIndex(0)
    else:
        ui.pages.setCurrentIndex(id)
        ui.stackedWidget.setCurrentIndex(1)
        ui.lbl_pageTitle.setText(name)
    if name == "Application":
        ui.groupBox_4.setTitle("Infos sur l'application")
        ui.app_os.removeItem(4)
        ui.app_os.setCurrentIndex(-1)
    elif name == "Jeu":
        ui.groupBox_4.setTitle("Infos sur le jeu")
        if ui.app_os.count() == 4:
            ui.app_os.addItem("Console")
        ui.app_os.setCurrentIndex(-1)

def path_leaf(path):
    #head, tail = splitext(path)
    #return head or basename(head)
    return splitext(basename(path))[0]

def audio_addFiles():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.ExistingFiles)
    fnames = dialog.getOpenFileNames(None, "Fichiers audio", os.path.expanduser("~"), "Fichiers audio (*.aac *.ac3 *.aif *.alac *.flac *.ape *.m4a *.mp3 *.mpc *.ogg *.wav *.wv *.wma)")[0]
    for file in fnames:
        if(isfile(file)):
            rowPos = ui.audio_files.rowCount()
            ui.audio_files.insertRow(rowPos)
            ui.audio_files.setItem(rowPos, 1, QTableWidgetItem(path_leaf(file)))

def app_browse():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.Directory)
    dialog.exec_()
    f = dialog.selectedFiles()[0]
    ui.jeu_fileName.setText(f)
    ui.app_taille.setText(sztxt(f))

ui.btnAppli.clicked.connect(lambda: goto(4, "Application"))
ui.btnAudio.clicked.connect(lambda: goto(0, "Audio"))
ui.btnEBook.clicked.connect(lambda: goto(1, "eBook"))
ui.btnEBooks.clicked.connect(lambda: goto(2, "eBooks"))
ui.btnJeu.clicked.connect(lambda: goto(4, "Jeu"))
ui.btnVideo.clicked.connect(lambda: goto(3, "Vidéo"))
ui.btnGoHome.clicked.connect(lambda: goto(-1))
ui.audio_addFiles.clicked.connect(audio_addFiles)
ui.jeu_browseFile.clicked.connect(app_browse)

def isEmpty(str):
    return not bool(str.strip())

def saveNFO():
    dlg = QFileDialog()
    fn = dlg.getSaveFileName(None, "Enregistrer le NFO", "", "Fichiers NFO (*.nfo)")[0]
    f = open(fn, "w")
    f.write(ui.plainTextEdit.toPlainText())
    f.close()

ui.final_genNFO.clicked.connect(saveNFO)

def centerStr(str, length):
    pos = int(length / 2 - len(str) / 2)
    return " " * pos + str + " " * (NFO_WIDTH - 2 - pos - len(str))

def getHeader(str, sym="-", sym2="|"):
    return sym * NFO_WIDTH + "\n" + sym2 + centerStr(str, NFO_WIDTH - 2) + sym2 + "\n" + sym * NFO_WIDTH + "\n"

def getFields(fields, pad=3, sym=".", fix=-1, removeEmpty=True):
    maxl = len(max(fields.keys(), key=lambda k: len(k))) + pad
    ret = ""
    for f, v in fields.items():
        if removeEmpty and isEmpty(v): continue
        cur = f + sym * (maxl - len(f)) + ": "
        rem = NFO_WIDTH - len(cur)
        if len(v) > rem:
            pass
        else:
            cur += v
        ret += cur + "\n"
    return ret + "\n"

def fisEmpty(field):
    if not field.isEnabled():
        return False
    if type(field) is QLineEdit:
        return isEmpty(field.text())
    elif type(field) in [QTextEdit, QPlainTextEdit]:
        return isEmpty(field.toPlainText())
    elif type(field) is QComboBox:
        return field.currentIndex() == -1
    elif type(field) is QSpinBox:
        return field.value() == field.minimum()

def validate():
    cur = getCurPage()
    required = []

    if cur == 0: # Audio
        pass
    elif cur == 1: # eBook
        pass
    elif cur == 2: # eBooks
        pass
    elif cur == 3: # Vidéo
        pass
    elif cur == 4: # Appli / Jeu
        pass

    # Infos up
    if fisEmpty(ui.txt_relName): required.append("Nom du torrent")
    if fisEmpty(ui.txt_upName): required.append("Uploader")

    if len(required) > 0:
        msg = QMessageBox()
        msg.setWindowTitle("Erreur")
        #msg.setIcon(QMessageBox.Critical)
        msg.setWindowIcon(QIcon(":/image/icon.png"))
        msg.setText("Les champs suivants sont requis :<b><ul>" + ''.join(["<li>&nbsp;&nbsp;" + x + "</li>" for x in required]) + "</ul></b><br>")
        msg.exec_()
        return False

    return True

def genNFO():
    if not validate():
        return

    nfo = ""
    nfo += getHeader(ui.txt_relName.text(), "*", "*")
    nfo += "\n"
    #attr

    # Infos sur l'up
    nfo += getHeader("Infos sur le torrent")
    nfo += getFields(
        {
            "Uploadé par": ui.txt_upName.text(),
            "Uploadé le": datetime.datetime.now().strftime("%d/%m/%Y")
        }
    )
    if not fisEmpty(ui.txt_relNotes):
        nfo += getHeader("Notes")
        nfo += ui.txt_relNotes.toPlainText() + "\n"

    nfo += "  .: NFO créé avec t411nfobuilder  -  http://v.ht/t411nfobuilder :.  \n"
    ui.plainTextEdit.setPlainText(nfo)
    ui.stackedWidget.setCurrentIndex(2)

ui.btnGenNfo.clicked.connect(genNFO)

ui.final_goBack.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(1))

window.show()
sys.exit(app.exec_())

