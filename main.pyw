import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from tnb_gui import Ui_MainWindow
import os
import datetime
import collections
import textwrap
from pymediainfo import MediaInfo
# http://stackoverflow.com/a/1520716/2196124
def most_common(L):
  counts = collections.Counter(L)
  return counts.most_common(1)[0][0]

__version__ = "0.2"


def round1or0(n):
    g = "%.1f" % n
    if ".0" in g:
        return "%.0f" % n
    return g


def get_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def sizeof_fmt(num, suffix='o', un=1024.0):
    un = float(un)
    pref = ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'] if un == 1024.0 else ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']
    for unit in pref:
        if abs(num) < un:
            return round1or0(num) + " %s%s" % (unit, suffix)
        num /= un
    return round1or0(num) + " %s%s" % ('Yi' if un == 1024.0 else 'Y', suffix)


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


def is_ascii(s):
    return s is not None and all(ord(c) < 128 for c in s)


def loadGenres():
    genres = ["2 Tone", "2-step garage", "A cappella", "Acid blues", "Acid breaks", "Acid house", "Acid jazz",
              "Acid rock", "Acid techno", "Acid trance", "Acidcore", "Adult contemporary", "Afrobeat", "Afropop",
              "Allaoui", "Ambient", "Ambient house", "Ambient jungle", "Ambient techno", "Americana", "Anarcho-punk",
              "Anti-folk", "Arena rock", "Art punk", "Art rock", "Austropop", "Avant-garde jazz", "Avanthop", "Axé",
              "Bachata", "Bachatango", "Baggy", "Baile funk", "Bakersfield sound", "Balearic beat", "Balearic trance",
              "Ballade", "Ballet", "Baltimore club", "Bass music", "Bassline", "Bay Area thrash metal", "Beat", "Bebop",
              "Berceuse", "Big band", "Big beat", "Biguine", "Black metal", "Black metal norvégien",
              "Black metal symphonique", "Bluegrass", "Blues", "Blues africain", "Blues rock", "Blues touareg",
              "Blues traditionnel", "Blues électrique", "Boléro", "Boogaloo", "Boogie-woogie", "Bossa nova",
              "Bounce music", "Brass band", "Breakbeat", "Breakbeat hardcore", "Breakcore", "Britpop", "Broken beat",
              "Brutal death metal", "Bubblegum pop", "C-pop", "C86", "Calypso", "Cantopop", "CCM", "Cello rock",
              "Cha-cha-cha", "Changüí", "Chanson française", "Chant grégorien", "Chaâbi algérien", "Chaâbi marocain",
              "Chicago blues", "Chicago house", "Chillstep", "Chiptune", "Classic rag", "Cloud rap", "Cold wave",
              "College rock", "Concerto", "Contradanza", "Cool jazz", "Country", "Country folk",
              "Country néo traditionnelle", "Country pop", "Country rap", "Country rock", "Country soul", "Cowpunk",
              "Crossover", "Crossover thrash", "Crunk", "Crunk'n'b", "Crunkcore", "Crust punk", "Cumbia", "D-beat",
              "Dance", "Dance-pop", "Dance-punk", "Dance-rock", "Dancehall", "Dangdut", "Danzón", "Dark ambient",
              "Dark metal", "Dark psytrance", "Dark wave", "Dark wave néo-classique", "Darkcore", "Darkstep",
              "Death 'n' roll", "Death metal", "Death metal mélodique", "Death metal technique", "Death rock",
              "Death-doom", "Deathcore", "Deathcountry", "Deathgrind", "Deep house", "Deepkho", "Delta blues",
              "Detroit blues", "Digital hardcore", "Dirty South", "Disco", "Disco house", "Diva house", "Dixieland",
              "Djent", "Doo-wop", "Doom metal", "Downtempo", "Dream pop", "Dream trance", "Drill", "Drill and bass",
              "Drum and bass", "Drumfunk", "Drumstep", "Dub", "Dub poetry", "Dubstep", "Dunedin sound",
              "Early hardcore", "Easycore", "EBM", "Electro", "Electro house", "Electro swing", "Electroclash",
              "Electronic body music", "Electronica", "Electronicore", "Electropop", "Electropunk", "Emo", "Emo pop",
              "Éthio-jazz", "Ethno-jazz", "Euro disco", "Eurobeat", "Eurodance", "Europop", "Extratone", "Fado",
              "Fanfare", "Filin", "Flamenco", "Folk", "Folk metal", "Folk progressif", "Folk psychédélique",
              "Folk rock", "Foxtrot", "Freakbeat", "Free jazz", "Freeform hardcore", "Freestyle", "French touch",
              "Frenchcore", "Fun-punk", "Funk", "Funk metal", "Funk rock", "Funktronica", "Funky house",
              "Future garage", "Future house", "G-funk", "Gabber", "Gaelic punk", "Gangsta rap", "Garage house",
              "Garage punk", "Garage rock", "Geek rock", "Ghetto house", "Ghettotech", "Glam metal", "Glam punk",
              "Glam rock", "Glitch", "Glitch-hop", "Goa", "Goregrind", "Gospel", "Gospel blues", "Gothabilly", "Grebo",
              "Grime", "Grindcore", "Grindie", "Groove metal", "Grunge", "Guajira", "Guaracha", "Gypsy punk", "Handsup",
              "Happy gabber", "Happy hardcore", "Hard bop", "Hard house", "Hard rock", "Hard trance", "Hardbag",
              "Hardcore", "Hardcore chrétien", "Hardcore mélodique", "Hardstep", "Hardstyle", "Hardtechno",
              "Heartland rock", "Heavy metal", "Heavy metal traditionnel", "Hi-NRG", "Hip-hop", "Hip-hop alternatif",
              "Hip-hop chrétien", "Hip-hop expérimental", "Hip-hop orchestral", "Hip-hop psychédélique", "Hip-house",
              "Hiplife", "Hipster-hop", "Honky tonk", "Horror punk", "Horrorcore", "House", "House progressive", "IDM",
              "Illbient", "Indie dance", "Indie folk", "Indie pop", "Industrial hardcore", "Intelligent dance music",
              "Italo dance", "Italo disco", "Italo house", "J-core", "J-pop", "J-rock", "Jangle pop", "Jazz",
              "Jazz afro-cubain", "Jazz blues", "Jazz fusion", "Jazz manouche", "Jazz modal", "Jazz Nouvelle-Orléans",
              "Jazz punk", "Jazz rap", "Jazz vocal", "Jazz West Coast", "Jazz-funk", "Jazz-rock", "Jazzstep",
              "Jump blues", "Jump-up", "Jumpstyle", "Jungle", "K-pop", "Kaneka", "Kansas City blues", "Kizomba",
              "Klezmer", "Kompa", "Krautrock", "Kuduro", "Kwaito", "Latin house", "Latin jazz", "Latin metal",
              "Lento violento", "Liquid funk", "Livetronica", "Lo-fi", "Logobi", "Louisiana blues", "Lounge",
              "Luk thung", "Madchester", "Mainstream", "Mainstream hardcore", "Makina", "Maloya", "Mambo", "Mandopop",
              "Mangue beat", "Marche", "Mashup", "Math rock", "Mathcore", "Mbalax", "Medieval rock", "Memphis blues",
              "Merengue", "Merenhouse", "Metal alternatif", "Metal avant-gardiste", "Metal celtique", "Metal chrétien",
              "Metal extrême", "Metal gothique", "Metal industriel", "Metal néo-classique", "Metal oriental",
              "Metal progressif", "Metal symphonique", "Metalcore", "Metalcore mélodique", "Miami bass", "Microhouse",
              "Midwest rap", "Milonga", "Minneapolis Sound", "Moombahcore", "Moombahton", "Mozambique", "MPB", "Murga",
              "Musette", "Musique 8-bit", "Musique alternative", "Musique bretonne", "Musique bruitiste",
              "Musique cadienne", "Musique celtique", "Musique chrétienne contemporaine", "Musique classique",
              "Musique concrète", "Musique cubaine", "Musique expérimentale", "Musique gothique",
              "Musique industrielle", "Musique instrumentale", "Musique irlandaise", "Musique latine",
              "Musique minimaliste", "Musique post-industrielle", "Musique progressive", "Musique romantique",
              "Musique spectrale", "Musique électroacoustique", "Musique électronique", "Musique émergente",
              "Musiqur Cajun", "Música Popular Brasileira", "Nardcore", "Nashville sound",
              "National socialist black metal", "Nazi punk", "Nederpop", "Negro spiritual", "Neo soul",
              "Neo-psychedelia", "Nerdcore", "Neue Deutsche Härte", "Neue Deutsche Welle", "Neurofunk", "New age",
              "New beat", "New jack swing", "New prog", "New wave", "New Wave of American Heavy Metal",
              "New Wave of British Heavy Metal", "New York blues", "New York hardcore", "Nintendocore", "No wave",
              "Nocturne", "Noise music", "Noise pop", "Noise rock", "Northern soul", "NSBM", "Nu jazz", "Nu metal",
              "Nu-disco", "Nu-NRG", "Nueva Trova", "NWOAHM", "NWOBHM", "Néo-bop", "Néo-classicisme", "Néo-trad",
              "Néofolk", "Oi ", "Old-time", "Opéra", "Opéra-rock", "Oratorio", "Outlaw country", "Pachanga",
              "Paisley Underground", "Paso doble", "Piano blues", "Piano rock", "Piano stride", "Piedmont blues",
              "Pirate metal", "Polonaise", "Pop", "Pop baroque", "Pop latino", "Pop metal", "Pop progressive",
              "Pop psychédélique", "Pop punk", "Pop rock", "Pop-rap", "Pornogrind", "Post-bop", "Post-disco",
              "Post-grunge", "Post-hardcore", "Post-metal", "Post-punk", "Post-rock", "Power ballad", "Power metal",
              "Power pop", "Powerviolence", "Protopunk", "Prélude", "Psychobilly", "Psytrance", "Pub rock",
              "Punk blues", "Punk celtique", "Punk chrétien", "Punk folk", "Punk hardcore", "Punk rock", "Punta rock",
              "Punto guajiro", "Queercore", "Quiet storm", "Rabiz", "RAC", "Raga rock", "Ragga", "Ragtime",
              "Rap East Coast", "Rap hardcore", "Rap metal", "Rap old school", "Rap politique", "Rap rock",
              "Rap West Coast", "Rapcore", "Rave", "Raï", "Raï'n'B", "Rebetiko", "Red Dirt", "Reggae", "Reggae fusion",
              "Reggaecrunk", "Reggaetón", "Rhapsodie", "Rhythm and blues", "RIO", "Riot grrrl", "RnB contemporain",
              "Rock", "Rock 'n' roll", "Rock alternatif", "Rock alternatif latino", "Rock anticommuniste",
              "Rock brésilien", "Rock canadien", "Rock celtique", "Rock chilien", "Rock chinois", "Rock chrétien",
              "Rock communiste", "Rock en espagnol", "Rock expérimental", "Rock gothique", "Rock in Opposition",
              "Rock industriel", "Rock indépendant", "Rock instrumental", "Rock néo-progressif", "Rock progressif",
              "Rock psychédélique", "Rock sudiste", "Rock suédois", "Rock symphonique", "Rock turc", "Rock wagnérien",
              "Rock électronique", "Rockabilly", "Rocksteady", "Rondo", "Roots rock", "Rumba", "Rumba catalane",
              "Rumba congolaise", "Rumba flamenca", "Sadcore", "Saint Louis blues", "Salegy", "Salsa", "Salsa-ragga",
              "Salsaton", "Samba", "Samba rock", "Sambass", "Scherzo", "Schranz", "Screamo", "Seggae", "Semba",
              "Shibuya-kei", "Shock rock", "Shoegazing", "Ska", "Ska punk", "Ska-jazz", "Skate punk", "Slam", "Slow",
              "Slow fox", "Slowcore", "Sludge metal", "Smooth jazz", "Snap", "Soca", "Soft rock", "Son cubain",
              "Sonate", "Songo", "Sophisti-pop", "Soukous", "Soul", "Soul blues", "Soul jazz", "Soul psychédélique",
              "Southern gospel", "Space rock", "Speed garage", "Speed metal", "Speedcore", "Splittercore",
              "Stoner rock", "Street punk", "Sunshine pop", "Surf", "Swamp blues", "Swamp pop", "Swing", "Symphonie",
              "Synthpop", "Synthpunk", "Synthwave", "Séga", "T-pop", "Tango", "Taqwacore", "Tarentelle", "Tech house",
              "Tech trance", "Techno", "Techno de Détroit", "Techno hardcore", "Techno minimale", "Technopop",
              "Techstep", "Tecno-brega", "Teen pop", "Terrorcore", "Texas blues", "Thrash metal",
              "Thrash metal allemand", "Thrashcore", "Timba", "Toccata", "Trallpunk", "Trance", "Trance psychédélique",
              "Trance vocale", "Trap", "Tribal house", "Tribe", "Trip hop", "Tropical house", "Tropipop",
              "Tumba francesa", "Twee pop", "UK garage", "UK hardcore", "Unblack metal", "Uplifting trance",
              "Vaporwave", "Viking metal", "Visual kei", "Vocal house", "West Coast blues", "Western Swing",
              "Witch house", "Wizard rock", "Wonky", "Wonky pop", "World music", "Youth crew", "Yéla", "Yéyé", "Zarico",
              "Zeuhl", "Ziglibithy", "Zouglou", "Zouk", "Zumba", "Zydeco"]
    ui.audio_genre.addItems(genres)
    ui.audio_genre.setCurrentIndex(-1)


audiofnames = []


def audioRemoveRows():
    for r in ui.audio_files.selectionModel().selectedRows():
        audiofnames.remove(ui.audio_files.item(r.row(), 8).text())
    audio_updateFiles()

def initUi():
    ui.con_type.currentIndexChanged.connect(lambda index: loadCon(index))
    ui.con_console.currentIndexChanged.connect(lambda index: firmV(ui.con_type.currentIndex() == 2 and index in [2, 4]))
    ui.ebook_format.currentIndexChanged.connect(lambda index: ebookdim(index in [1, 2, 3, 4, 5, 9, 12]))
    ui.app_os.currentIndexChanged.connect(lambda index: setAppGame(index == 4))
    ui.app_swCon.setCurrentIndex(0)

    audiofnames = []
    ui.audio_files.setColumnHidden(8, True)

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

    ui.audio_isVariousArtists.stateChanged.connect(lambda: ui.audio_variousArtists.setEnabled(ui.audio_isVariousArtists.isChecked()))

    ui.audio_files.itemSelectionChanged.connect(lambda: ui.audio_removeRows.setEnabled(len(ui.audio_files.selectedItems()) > 0))

    ui.audio_removeRows.clicked.connect(audioRemoveRows)

    loadGenres()

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
    return os.path.splitext(os.path.basename(path))[0]


def durationToText(dur):
    return repr(dur // 60) + ":" + repr(dur % 60).zfill(2)


def textToDuration(dur):
    spl = dur.split(":")
    return int(spl[0]) * 60 + int(spl[1])


def average(arr, emp=-1):
    if len(arr) == 0: return emp
    return sum(arr) / float(len(arr))


def audio_addFiles():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.ExistingFiles)
    fn = dialog.getOpenFileNames(None, "Fichiers audio", os.path.expanduser("~"),
                                     "Fichiers audio (*.aac *.ac3 *.aif *.alac *.flac *.ape *.m4a *.mp3 *.mpc *.ogg *.wav *.wv *.wma)")[
        0]
    for file in fn:
        if file in audiofnames:
            msg = QMessageBox()
            msg.setWindowTitle("t411 NFO Builder")
            msg.setIcon(QMessageBox.Critical)
            msg.setStyle(DEFAULT_STYLE)
            msg.setWindowIcon(QIcon(":/image/icon.png"))
            msg.setText("Le fichier '" + file + "' a déjà été ajouté.")
            msg.exec_()
        else:
            audiofnames.append(file)
    audio_updateFiles()


class ROTableItem(QTableWidgetItem):
    def __init__(self, __args):
        QTableWidgetItem.__init__(self, __args)
        self.setFlags(self.flags() & ~2)


def audio_updateFiles():
    dSum = 0
    sSum = 0
    codecs = []
    brates = []
    chan = 0
    enc = []
    genres = []
    freqs = []
    year = -1
    while ui.audio_files.rowCount() > 0:
        ui.audio_files.removeRow(0) # Vider le tableau
    for file in audiofnames:
        if (os.path.isfile(file)):
            rowPos = ui.audio_files.rowCount()
            ui.audio_files.insertRow(rowPos)
            ui.audio_files.setItem(rowPos, 8, QTableWidgetItem(file))
            ui.audio_files.setItem(rowPos, 1, QTableWidgetItem(os.path.basename(file)))  # Nom du fichier
            mediaInfo = MediaInfo.parse(file)
            track = mediaInfo.tracks[0]
            audioTrack = mediaInfo.tracks[1]
            freqs.append(audioTrack.sampling_rate)
            chan = audioTrack.channel_s
            codecs.append(audioTrack.other_codec[0])
            lib = track.writing_library
            if is_ascii(lib) and not "=" in lib and len(lib) < 32:
                enc.append(lib)
            itemN = QTableWidgetItem()
            itemN.setData(0, int(track.track_name_position))
            ui.audio_files.setItem(rowPos, 0, itemN)  # N°
            ui.audio_files.setItem(rowPos, 2, QTableWidgetItem(track.track_name))  # Titre
            ui.audio_files.setItem(rowPos, 3, QTableWidgetItem(track.performer))  # Interprète(s)
            ui.audio_files.setItem(rowPos, 4, QTableWidgetItem(track.album))  # Album
            size = os.path.getsize(file)
            sSum += size
            ui.audio_files.setItem(rowPos, 5, ROTableItem(sizeof_fmt(size)))  # Taille
            year = track.recorded_date
            if track.genre is not None: genres.append(track.genre)
            if track.duration is not None:
                duree = track.duration / 1000
                dSum += duree
                ui.audio_files.setItem(rowPos, 6, ROTableItem(durationToText(int(duree))))  # Durée
            brate = track.overall_bit_rate
            if brate is not None:
                brates.append(brate)
                ui.audio_files.setItem(rowPos, 7, ROTableItem(sizeof_fmt(brate, 'bps', 1000)))  # Bitrate
    ui.audio_files.sortByColumn(0, 0)
    ui.audio_totalTime.setText(durationToText(int(dSum)))
    ui.txt_totalSize.setText(sizeof_fmt(sSum))
    if year is not None: ui.audio_year.setValue(int(year))
    ui.audio_codec.setText(", ".join(set(codecs)))
    ui.audio_channel.setText(repr(chan))
    ui.audio_encoder.setText(most_common(enc))
    ui.audio_genre.setCurrentText(", ".join(set(genres)))
    ui.audio_avrBitrate.setText(sizeof_fmt(average(brates), 'bps', 1000))
    ui.audio_freq.setText(sizeof_fmt(most_common(freqs), 'Hz', 1000))


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
    required[ui.txt_totalSize] = "Taille totale"

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
        nfo += getHeader("Infos audio")
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
        nfo += getHeader("Liste des p ")
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