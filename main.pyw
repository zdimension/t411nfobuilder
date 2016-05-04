import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from tnb_gui import Ui_MainWindow
import os
import datetime
import textwrap

__version__ = "0.2"


def get_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def sizeof_fmt(num, suffix='o'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


def sztxt(p):
    return sizeof_fmt(get_size(p))


def ebookdim(v):
    if (v):
        ui.formLayout_5.insertRow(11, ui.lblDim, ui.ebook_dimensions)
        ui.lblDim.show()
        ui.ebook_dimensions.show()
    else:
        ui.ebook_dimensions.hide()
        ui.ebook_dimensions.setText("")
        ui.lblDim.hide()
        ui.formLayout_5.removeWidget(ui.ebook_dimensions)
        ui.formLayout_5.removeWidget(ui.lblDim)


def firmV(v):
    if (v):
        ui.formLayout_10.insertRow(3, ui.con_lblFirmw, ui.con_firmw)
        ui.con_lblFirmw.show()
        ui.con_firmw.show()
    else:
        ui.con_firmw.hide()
        ui.con_firmw.setText("")
        ui.con_lblFirmw.hide()
        ui.formLayout_10.removeWidget(ui.con_firmw)
        ui.formLayout_10.removeWidget(ui.con_lblFirmw)


class myMainWindow(QMainWindow):
    def closeEvent(self, event):
        msg = QMessageBox()
        msg.setWindowTitle("t411 NFO Builder")
        msg.setIcon(QMessageBox.Question)
        msg.setStyle(DEFAULT_STYLE)
        msg.setWindowIcon(QIcon(":/image/icon.png"))
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setText("Voulez-vous vraiment quitter ?\nToutes les modifications non sauvegardées seront perdues.")
        event.ignore()
        if msg.exec_() == QMessageBox.Yes:
            event.accept()


def initUi():
    ui.con_type.currentIndexChanged.connect(lambda index: loadCon(index))
    ui.con_console.currentIndexChanged.connect(lambda index: firmV(ui.con_type.currentIndex() == 2 and index in [2, 4]))
    ui.ebook_format.currentIndexChanged.connect(lambda index: ebookdim(index in [1, 2, 3, 4, 5, 9, 12]))
    ui.app_os.currentIndexChanged.connect(lambda index: setAppGame(index == 4))
    ui.app_swCon.setCurrentIndex(0)

    ui.btnAppli.clicked.connect(lambda: goto(4, "Application"))
    ui.btnAudio.clicked.connect(lambda: goto(0, "Audio"))
    ui.btnEBook.clicked.connect(lambda: goto(1, "eBook"))
    ui.btnEBooks.clicked.connect(lambda: goto(2, "eBooks"))
    ui.btnJeu.clicked.connect(lambda: goto(4, "Jeu"))
    ui.btnVideo.clicked.connect(lambda: goto(3, "Vidéo"))
    ui.btnGoHome.clicked.connect(lambda: goto(-1))
    ui.audio_addFiles.clicked.connect(lambda: audio_addFiles())
    ui.jeu_browseFile.clicked.connect(lambda: app_browse())

    ui.final_genNFO.clicked.connect(lambda: saveNFO())

    ui.btnGenNfo.clicked.connect(lambda: genNFO())

    ui.final_goBack.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(1))

    ebookdim(False)

    firmV(False)

    ui.stackedWidget.setCurrentIndex(0)
    window.setWindowTitle("t411 NFO Builder " + __version__)
    ui.label.setText("t411 NFO Builder " + __version__)


app = QApplication(sys.argv)
DEFAULT_STYLE = QStyleFactory.create(app.style().objectName())
app.setStyle(QStyleFactory.create("Fusion"))
window = myMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
initUi()


def getCurPage():
    return ui.pages.currentIndex()


def loadCon(id):
    if id == 0:  # Microsoft
        ui.con_console.clear()
        ui.con_console.addItems(["Xbox", "Xbox 360", "Xbox One"])
    elif id == 1:  # Nintendo
        ui.con_console.clear()
        ui.con_console.addItems(["3DS", "DS", "GameCube", "Wii", "Wii U"])
    elif id == 2:  # Sony
        ui.con_console.clear()
        ui.con_console.addItems(
            ["PlayStation", "PlayStation 2", "PlayStation 3", "PlayStation 4", "PlayStation Portable",
             "PlayStation Vita"])
    ui.con_console.setCurrentIndex(-1)


def setAppGame(ok):
    if ok:
        ui.con_type.setEnabled(True)
        ui.con_console.setEnabled(True)
        ui.con_firmw.setEnabled(True)
        ui.app_confMin.setEnabled(False)
        ui.app_install.setEnabled(False)
        ui.app_swCon.setCurrentIndex(1)
    else:
        ui.con_type.setEnabled(False)
        ui.con_console.setEnabled(False)
        ui.con_firmw.setEnabled(False)
        ui.app_confMin.setEnabled(True)
        ui.app_install.setEnabled(True)
        ui.app_swCon.setCurrentIndex(0)


def goto(id, name=""):
    if id == -1:
        msg = QMessageBox()
        msg.setWindowTitle("t411 NFO Builder")
        msg.setIcon(QMessageBox.Question)
        msg.setStyle(DEFAULT_STYLE)
        msg.setWindowIcon(QIcon(":/image/icon.png"))
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setText(
            "Voulez-vous vraiment retourner à l'accueil ?\nToutes les modifications non sauvegardées seront perdues.")
        if msg.exec_() == QMessageBox.Yes:
            ui.setupUi(window)
            initUi()
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
    return splitext(basename(path))[0]


def audio_addFiles():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.ExistingFiles)
    fnames = dialog.getOpenFileNames(None, "Fichiers audio", os.path.expanduser("~"),
                                     "Fichiers audio (*.aac *.ac3 *.aif *.alac *.flac *.ape *.m4a *.mp3 *.mpc *.ogg *.wav *.wv *.wma)")[
        0]
    for file in fnames:
        if (isfile(file)):
            rowPos = ui.audio_files.rowCount()
            ui.audio_files.insertRow(rowPos)
            ui.audio_files.setItem(rowPos, 1, QTableWidgetItem(path_leaf(file)))


def app_browse():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.Directory)
    dialog.exec_()
    f = dialog.selectedFiles()[0]
    ui.jeu_fileName.setText(f)
    ui.txt_totalSize.setText(sztxt(f))


def isEmpty(str):
    return not bool(str.strip())


def saveNFO():
    dlg = QFileDialog()
    fn = dlg.getSaveFileName(None, "Enregistrer le NFO", "", "Fichiers NFO (*.nfo)")[0]
    f = open(fn, "w")
    f.write(ui.plainTextEdit.toPlainText())
    f.close()


def centerStr(str, length):
    import math
    pos = math.ceil(length / 2 - len(str) / 2)
    return " " * pos + str + " " * (length - pos - len(str))


def getHeader(str, sym="-", add=0):
    return sym * (82 + add) + "\n" + centerStr(str, 82 + add) + "\n" + sym * (82 + add) + "\n"


def getFields(fields, pad=3, sym=".", fix=-1, removeEmpty=True):
    maxl = 21 + pad
    ret = ""
    for f, v in fields.items():
        if removeEmpty and isEmpty(v): continue
        cur = f + sym * (maxl - len(f)) + ": "
        curl = len(cur)
        rem = 82 - curl

        spc = " " * curl
        ret += cur
        i = 0
        for c in v:
            if c == "\n" or i == rem:
                ret += "\n"
                ret += spc
                if c != "\n": ret += c
                i = -1
            else:
                ret += c
            i += 1
        ret += "\n"

    return ret + "\n"


def fisEmpty(field):
    # if not field.isEnabled(): return False
    if type(field) is QLineEdit:
        return isEmpty(field.text())
    elif type(field) in [QTextEdit, QPlainTextEdit]:
        return isEmpty(field.toPlainText())
    elif type(field) is QComboBox:
        return field.currentIndex() == -1
    elif type(field) is QSpinBox:
        return field.value() == field.minimum()
    elif type(field) is QTableWidget:
        return field.rowCount() == 0


def validate():
    cur = getCurPage()
    from collections import OrderedDict
    required = OrderedDict()

    if cur == 0:  # Audio
        required[ui.audio_files] = "Fichiers audio"
        required[ui.audio_codec] = "Codec"
        required[ui.audio_channel] = "Canaux"
        required[ui.audio_avrBitrate] = "Bitrate moyen"
    elif cur == 1:  # eBook
        required[ui.ebook_titre] = "Titre"
        required[ui.ebook_format] = "Format"
        required[ui.ebook_pages] = "Nombre de pages"
        required[ui.ebook_dimensions] = "Dimensions"
    elif cur == 2:  # eBooks
        required[ui.ebooks_files] = "Fichiers eBooks"
        required[ui.ebooks_format] = "Format"
    elif cur == 3:  # Vidéo
        required[ui.film_files] = "Fichiers vidéo"
        required[ui.film_format] = "Format"
    elif cur == 4:  # Appli / Jeu
        required[ui.app_nom] = "Nom"
        required[ui.app_langue] = "Langue"
        required[ui.app_os] = "Plateforme"
        required[ui.app_confMin] = "Config. minimum"
        required[ui.app_install] = "Étapes d'installation"
        required[ui.con_type] = "Constructeur"
        required[ui.con_console] = "Console"
        required[ui.con_firmw] = "Firmware"

    # Infos up
    required[ui.txt_relName] = "Nom du torrent"
    required[ui.txt_upName] = "Uploader"
    required[ui.txt_totalSize] = "Taille totale"
    required[ui.txt_relNotes] = "Description"

    req = [("<li>&nbsp;&nbsp;" + v + "</li>") for (k, v) in required.items() if
           (fisEmpty(k) and k.isVisible() and k.isEnabled())]
    if len(req) > 0:
        msg = QMessageBox()
        msg.setWindowTitle("Erreur")
        msg.setIcon(QMessageBox.Critical)
        msg.setStyle(DEFAULT_STYLE)
        msg.setWindowIcon(QIcon(":/image/icon.png"))
        msg.setText("Les champs suivants sont requis :<b><ul>" + ''.join(req) + "</ul></b>")
        msg.exec_()
        return False

    return True


def genNFO():
    # if not validate():
    #    return


    nfoTop = ""
    nfoTop += "+----------------------------------------------------------------------------------------+\n"
    nfoTop += "|*+------------------------------------------------------------------------------------+*|\n"
    nfoTop += "|*|                                                                                    |*|\n"

    nfo = ""
    nfo += getHeader(ui.txt_relName.text(), "*", 2)
    nfo += "\n"

    cur = getCurPage()

    if cur == 0:  # Audio
        nfo += getFields(
            {
                "Codec": ui.audio_codec.text(),
                "Fréquence": ui.audio_freq.text(),
                "Canaux": ui.audio_channel.text(),
                "Encodeur": ui.audio_encoder.text(),
                "Bitrate moyen": ui.audio_avrBitrate.text(),
                "Genre": ui.audio_genre.currentText(),
                "Durée totale": ui.audio_totalTime.text(),
            }
        )
    elif cur == 1:  # eBook
        nfo += getFields(
            {
                "Titre": ui.ebook_titre.text(),
                "Format": ui.ebook_format.currentText(),
                "Nombre de pages": ui.ebook_pages.value(),
                "Dimensions": ui.ebook_dimensions.text()
            }
        )
    elif cur == 2:  # eBooks
        nfo += getFields(
            {
                "Format": ui.ebooks_format.currentText()
            }
        )
    elif cur == 3:  # Vidéo
        nfo += getFields(
            {
                "Format": ui.film_format.text()
            }
        )
    elif cur == 4:  # Appli / Jeu
        nfo += getFields(
            {
                "Nom": ui.app_nom.text(),
                "Langue": ui.app_langue.currentText()
            }
        )
        if ui.app_swCon.currentIndex() == 0:
            nfo += getFields(
                {
                    "Plateforme": ui.app_os.currentText(),
                    "Config. minimum": ui.app_confMin.toPlainText(),
                    "Étapes d'installation": ui.app_install.toPlainText()
                }
            )
        else:
            nfo += getFields(
                {
                    "Constructeur": ui.con_type.text(),
                    "Console": ui.con_console.text(),
                    "Firmware": ui.con_firmw.text()
                }
            )

    # Infos sur l'up
    nfo += getHeader("Infos sur le torrent")
    nfo += getFields(
        {
            "Uploadé par": ui.txt_upName.text(),
            "Uploadé le": datetime.datetime.now().strftime("%d/%m/%Y"),
            "Taille totale": ui.txt_totalSize.text()
        }
    )
    if not fisEmpty(ui.txt_relNotes):
        nfo += getHeader("Notes")
        nfo += textwrap.fill(ui.txt_relNotes.toPlainText(), width=82, replace_whitespace=False) + "\n"

    nfoBottom = "\n"
    nfoBottom += "|*|                                                                                    |*|\n"
    nfoBottom += "|*|                                                                                    |*|\n"
    nfoBottom += "|*| |--------------------------------------------------------------------------------| |*|\n"
    nfoBottom += "|*+-|                        NFO créé avec t411nfobuilder X.X                        |-+*|\n".replace(
        "X.X", __version__)
    nfoBottom += "+---|                  https://github.com/zdimension/t411nfobuilder                  |---+\n"
    nfoBottom += "    |--------------------------------------------------------------------------------|    \n"
    nfo = nfoTop + "\n".join(["|*|" + x.ljust(83).rjust(84) + "|*|" for x in nfo.split("\n")]) + nfoBottom

    ui.plainTextEdit.setPlainText(nfo)
    ui.stackedWidget.setCurrentIndex(2)


window.show()
sys.exit(app.exec_())
