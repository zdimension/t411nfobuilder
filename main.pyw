import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from tnb_gui import Ui_MainWindow
import os
import datetime
import collections
import textwrap
from pymediainfo import MediaInfo
from collections import OrderedDict
import re


# http://stackoverflow.com/a/1520716/2196124
def most_common(L):
    if len(L) == 0: return None
    counts = collections.Counter(L)
    return counts.most_common(1)[0][0]


__version__ = "0.6"
uiInitialized = False

ws_save = {}

languages = {"aa": "Afar",
             "ab": "Abkhaze",
             "af": "Afrikaans",
             "ak": "Akan",
             "sq": "Albanais",
             "am": "Amharique",
             "ar": "Arabe",
             "an": "Aragonais",
             "hy": "Arménien",
             "as": "Assamais",
             "av": "Avar",
             "ae": "Avestique",
             "ay": "Aymara",
             "az": "Azéri",
             "ba": "Bachkir",
             "bm": "Bambara",
             "eu": "Basque",
             "be": "Biélorusse",
             "bn": "Bengali",
             "bh": "Langues Biharis",
             "bi": "Bichlamar",
             "bs": "Bosniaque",
             "br": "Breton",
             "bg": "Bulgare",
             "my": "Birman",
             "ca": "Catalan",
             "ch": "Chamorro",
             "ce": "Tchétchène",
             "zh": "Chinois",
             "cu": "Slavon d'église",
             "cv": "Tchouvache",
             "kw": "Cornique",
             "co": "Corse",
             "cr": "Cree",
             "cs": "Tchèque",
             "da": "Danois",
             "dv": "Maldivien",
             "nl": "Néerlandais",
             "dz": "Dzongkha",
             "en": "Anglais",
             "eo": "Espéranto",
             "et": "Estonien",
             "ee": "Éwé",
             "fo": "Féroïen",
             "fj": "Fidjien",
             "fi": "Finnois",
             "fr": "Français",
             "fy": "Frison occidental",
             "ff": "Peul",
             "ka": "Géorgien",
             "de": "Allemand",
             "gd": "Gaélique",
             "ga": "Irlandais",
             "gl": "Galicien",
             "gv": "Mannois",
             "el": "Grec",
             "gn": "Guarani",
             "gu": "Goudjrati",
             "ht": "Créole haïtien",
             "ha": "Haoussa",
             "he": "Hébreu",
             "hz": "Herero",
             "hi": "Hindi",
             "ho": "Hiri Motu",
             "hr": "Croate",
             "hu": "Hongrois",
             "ig": "Igbo",
             "is": "Islandais",
             "io": "Ido",
             "ii": "Yi de Sichuan",
             "iu": "Inuktitut",
             "ie": "Interlingue",
             "ia": "Interlingua (Langue auxiliaire internationale)",
             "id": "Indonésien",
             "ik": "Inupiaq",
             "it": "Italien",
             "jv": "Javanais",
             "ja": "Japonais",
             "kl": "Groenlandais",
             "kn": "Kannada",
             "ks": "Kashmiri",
             "kr": "Kanouri",
             "kk": "Kazakh",
             "km": "Khmer central",
             "ki": "Kikuyu",
             "rw": "Rwanda",
             "ky": "Kirghiz",
             "kv": "Kom",
             "kg": "Kongo",
             "ko": "Coréen",
             "kj": "Kuanyama",
             "ku": "Kurde",
             "lo": "Lao",
             "la": "Latin",
             "lv": "Letton",
             "li": "Limbourgeois",
             "ln": "Lingala",
             "lt": "Lituanien",
             "lb": "Luxembourgeois",
             "lu": "Luba-Katanga",
             "lg": "Ganda",
             "mk": "Macédonien",
             "mh": "Marshall",
             "ml": "Malayalam",
             "mi": "Maori",
             "mr": "Marathe",
             "ms": "Malais",
             "mg": "Malgache",
             "mt": "Maltais",
             "mn": "Mongol",
             "na": "Nauruan",
             "nv": "Navaho",
             "nr": "Ndébélé du sud",
             "nd": "Ndébélé du nord",
             "ng": "Ndonga",
             "ne": "Népalais",
             "nn": "Norvégien Nynorsk",
             "nb": "Norvégien Bokmål",
             "no": "Norvégien",
             "ny": "Chichewa",
             "oc": "Occitan",
             "oj": "Ojibwa",
             "or": "Oriya",
             "om": "Galla",
             "os": "Ossète",
             "pa": "Pendjabi",
             "fa": "Persan",
             "pi": "Pali",
             "pl": "Polonais",
             "pt": "Portugais",
             "ps": "Pachto",
             "qu": "Quechua",
             "rm": "Romanche",
             "ro": "Roumain",
             "rn": "Rundi",
             "ru": "Russe",
             "sg": "Sango",
             "sa": "Sanskrit",
             "si": "Singhalais",
             "sk": "Slovaque",
             "sl": "Slovène",
             "se": "Sami du nord",
             "sm": "Samoan",
             "sn": "Shona",
             "sd": "Sindhi",
             "so": "Somali",
             "st": "Sotho du sud",
             "es": "Espagnol",
             "sc": "Sarde",
             "sr": "Serbe",
             "ss": "Swati",
             "su": "Soundanais",
             "sw": "Swahili",
             "sv": "Suédois",
             "ty": "Tahitien",
             "ta": "Tamoul",
             "tt": "Tatar",
             "te": "Télougou",
             "tg": "Tadjik",
             "tl": "Tagalog",
             "th": "Thaï",
             "bo": "Tibétain",
             "ti": "Tigrigna",
             "to": "Tongan",
             "tn": "Tswana",
             "ts": "Tsonga",
             "tk": "Turkmène",
             "tr": "Turc",
             "tw": "Twi",
             "ug": "Ouïgour",
             "uk": "Ukrainien",
             "ur": "Ourdou",
             "uz": "Ouszbek",
             "ve": "Venda",
             "vi": "Vietnamien",
             "vo": "Volapük",
             "cy": "Gallois",
             "wa": "Wallon",
             "wo": "Wolof",
             "xh": "Xhosa",
             "yi": "Yiddish",
             "yo": "Yoruba",
             "za": "Zhuang",
             "zu": "Zoulou"}


def getLanguage(lang):
    if not lang:
        return "<Langue inconnue>"
    if lang in languages:
        return languages[lang]
    return lang


def getThemedBox():
    msg = QMessageBox()
    msg.setWindowTitle("t411 NFO Builder")
    msg.setStyle(DEFAULT_STYLE)
    msg.setWindowIcon(QIcon(":/image/icon.png"))
    return msg


def checkArch(f):
    if os.path.splitext(f)[1].lower() in [".zip", ".rar", ".7z"]:
        msg = getThemedBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(
            "<h2>Attention !</h2><p>Les <b>fichiers archives</b> sont <b><font color='red'>interdits</font></b>.</p>")
        msg.exec_()
        return True
    return False


def round1or0(n):
    g = "%.1f" % n
    if ".0" in g:
        return "%.0f" % n
    return g


def orValue(l, v):
    try:
        return l()
    except:
        return v


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


consoles = OrderedDict([
    ("Microsoft", ["Xbox", "Xbox 360", "Xbox One"]),
    ("Nintendo", ["3DS", "DS", "GameCube", "Wii", "Wii U"]),
    ("Sony",
     ["PlayStation", "PlayStation 2", "PlayStation 3", "PlayStation 4", "PlayStation Portable", "PlayStation Vita"])
])

consoles_retro = OrderedDict([
    ("Amstrad", ["CPC", "GX-5000", "PCX"]),
    ("Apple", ["I", "II", "III", "Macintosh", "PowerMac"]),
    ("Atari", ["2600", "7800", "Falcon", "Jaguar", "Jaguar II", "Lynx", "Lynx II", "ST", "TT"]),
    ("Coleco", ["Arcade", "Colecovision", "Colecovision Adam", "Gemini", "PlayPal", "Quiz Wiz"]),
    ("Commodore", ["128", "64", "Amiga", "Amiga CD32", "Amiga CDTV", "C64"]),
    ("GamePark", ["GP2X", "GP32", "GPI", "XGP"]),
    ("Magnavox/Philips", ["CD-i", "Videopac"]),
    ("Milton Bradley", ["Microvision", "Vectrex"]),
    ("MSX", ["MSX"]),
    ("NEC", ["CoreGrafX", "PC-Engine", "PC-FX", "SuperGrafX", "TurboGrafx"]),
    ("Nintendo", ["Game Boy", "Game Boy Advance", "NES", "N64", "Super Nintendo", "Virtual Boy"]),
    ("Nokia", ["N-Gage", "N-Gage QD"]),
    ("Oric", ["Atmos", "Oric"]),
    ("Origin", ["2000"]),
    ("Sega", ["Dreamcast", "Game Gear", "Master System", "Megadrive", "Saturn"]),
    ("Sinclair", ["ZX Spectrum", "ZX80", "ZX81"]),
    ("SNK", ["Neo-Geo", "Neo-Geo Pocket"]),
    ("The DO Company", ["DO"]),
    ("Thomson", ["MO5", "TO16", "TO7", "TO8", "TO9"]),
    ("VTech", ["V.Smile", "V.Smile Pocket"])
])


def loadCon():
    ui.con_console.clear()
    ui.con_console.addItems(consoles[ui.con_type.currentText()])
    ui.con_console.setCurrentIndex(-1)


def loadRetroCon():
    ui.retro_console.clear()
    ui.retro_console.addItems(consoles_retro[ui.retro_type.currentText()])
    ui.retro_console.setCurrentIndex(-1)


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
        ui.widget_12.show()
    else:
        ui.con_firmw.hide()
        ui.con_firmw.setText("")
        ui.con_lblFirmw.hide()
        ui.widget_12.hide()
        ui.formLayout_10.removeWidget(ui.con_firmw)
        ui.formLayout_10.removeWidget(ui.con_lblFirmw)


class myMainWindow(QMainWindow):
    def closeEvent(self, event):
        if ui.stackedWidget.currentIndex() == 0:
            event.accept()
            return
        msg = getThemedBox()
        msg.setIcon(QMessageBox.Question)
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
audiofdata = {}
videofnames = []
videofdata = {}


def audioRemoveRows():
    for r in ui.audio_files.selectionModel().selectedRows():
        audiofnames.remove(audiofdata[r.row()]['file'])
    audio_updateFiles()


def videoRemoveRows():
    for r in ui.film_files.selectionModel().selectedRows():
        videofnames.remove(videofdata[r.row()]['file'])
    video_updateFiles()


def setNMR(nmr):
    ui.audio_ripper.setEnabled(not nmr)
    ui.audio_cdmodel.setEnabled(not nmr)
    ui.audio_source.setEnabled(not nmr)
    if nmr:
        ui.audio_ripper.setText("")
        ui.audio_cdmodel.setText("")
        ui.audio_source.setCurrentIndex(-1)


def getCurPage():
    return ui.pages.currentIndex()


def setAppGame(id):
    ok = id in [4, 5]
    if ok:
        ui.app_confMin.setEnabled(False)
        ui.app_install.setEnabled(False)
        if id == 4:
            ui.con_type.setEnabled(True)
            ui.con_console.setEnabled(True)
            ui.con_firmw.setEnabled(True)
            ui.retro_type.setEnabled(False)
            ui.retro_console.setEnabled(False)
            ui.app_swCon.setCurrentIndex(1)
        else:
            ui.retro_type.setEnabled(True)
            ui.retro_console.setEnabled(True)
            ui.con_type.setEnabled(False)
            ui.con_console.setEnabled(False)
            ui.con_firmw.setEnabled(False)
            ui.app_swCon.setCurrentIndex(2)
    else:
        ui.app_confMin.setEnabled(True)
        ui.app_install.setEnabled(True)
        ui.retro_type.setEnabled(False)
        ui.retro_console.setEnabled(False)
        ui.con_type.setEnabled(False)
        ui.con_console.setEnabled(False)
        ui.con_firmw.setEnabled(False)
        ui.app_swCon.setCurrentIndex(0)


def saveWindowState():
    global ws_save
    ws_save = {}
    ws_save['geom'] = window.saveGeometry()
    ws_save['state'] = window.saveState()
    ws_save['max'] = window.isMaximized()
    if not ws_save['max']:
        ws_save['pos'] = window.pos()
        ws_save['size'] = window.size()


def restoreWindowState():
    global ws_save
    window.restoreState(ws_save['state'])
    if ws_save['max']:
        window.setWindowState(Qt.WindowNoState)
        window.show()
        window.setWindowState(Qt.WindowMaximized)
    else:
        window.restoreGeometry(ws_save['geom'])
        window.move(ws_save['pos'])
        window.resize(ws_save['size'])
    ws_save = {}


def initUi():
    window.hide()
    geom = None
    isFullScreen = False
    if uiInitialized:
        geom = window.saveGeometry()
        isFullScreen = window.isMaximized()
    ui.setupUi(window)
    if geom is not None and not window.isMaximized():
        window.restoreGeometry(geom)
    window.show()
    if isFullScreen: window.setWindowState(Qt.WindowMaximized)
    # window.move(QApplication.desktop().screen().rect().center() - window.rect().center())
    # window.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, window.size(), QApplication.desktop().availableGeometry()))
    ui.con_type.addItems(consoles.keys())
    ui.con_type.setCurrentIndex(-1)
    ui.retro_type.addItems(consoles_retro.keys())
    ui.retro_type.setCurrentIndex(-1)
    ui.con_type.currentIndexChanged.connect(loadCon)
    ui.retro_type.currentIndexChanged.connect(loadRetroCon)
    ui.con_console.currentIndexChanged.connect(lambda index: firmV(ui.con_type.currentIndex() == 2 and index in [2, 4]))
    ui.ebook_format.currentIndexChanged.connect(lambda index: ebookdim(index in [1, 2, 3, 4, 5, 9, 12]))
    ui.app_os.currentIndexChanged.connect(lambda index: setAppGame(index))
    ui.app_swCon.setCurrentIndex(0)

    audiofnames = []
    audiofdata = {}
    videofnames = []
    videofdata = {}

    ui.btnAppli.clicked.connect(lambda: goto(4, "Application"))
    ui.btnAudio.clicked.connect(lambda: goto(0, "Audio"))
    ui.btnEBook.clicked.connect(lambda: goto(1, "eBook"))
    ui.btnEBooks.clicked.connect(lambda: goto(2, "eBooks"))
    ui.btnJeu.clicked.connect(lambda: goto(4, "Jeu"))
    ui.btnVideo.clicked.connect(lambda: goto(3, "Vidéo"))
    ui.btnGoHome.clicked.connect(lambda: goto(-1))
    ui.audio_addFiles.clicked.connect(lambda: audio_addFiles())
    ui.film_addFiles.clicked.connect(lambda: video_addFiles())
    ui.jeu_browseFile.clicked.connect(lambda: app_browse())

    ui.final_genNFO.clicked.connect(lambda: saveNFO())

    ui.btnGenNfo.clicked.connect(lambda: genNFO())

    ui.final_goBack.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(1))

    ui.audio_files.itemSelectionChanged.connect(
        lambda: ui.audio_removeRows.setEnabled(len(ui.audio_files.selectedItems()) > 0))
    ui.film_files.itemSelectionChanged.connect(
        lambda: ui.film_removeRows.setEnabled(len(ui.film_files.selectedItems()) > 0))

    ui.audio_removeRows.clicked.connect(audioRemoveRows)
    ui.film_removeRows.clicked.connect(videoRemoveRows)

    ui.audio_notMyRip.stateChanged.connect(lambda: setNMR(ui.audio_notMyRip.isChecked()))

    loadGenres()

    ebookdim(False)

    firmV(False)
    ui.stackedWidget.setCurrentIndex(0)
    window.setWindowTitle("t411 NFO Builder " + __version__)
    ui.label.setText("t411 NFO Builder " + __version__)


def goto(id, name=""):
    if id == -1:
        msg = getThemedBox()
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setText(
            "Voulez-vous vraiment retourner à l'accueil ?\nToutes les modifications non sauvegardées seront perdues.")
        if msg.exec_() == QMessageBox.Yes:
            saveWindowState()
            initUi()
            restoreWindowState()
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


def durationToText(dur, sec=True):
    hours, rem = divmod(dur, 3600)
    minutes, seconds = divmod(rem, 60)
    sec = repr(seconds) + "s" if seconds != 0 and sec else ""
    min = "" if minutes == 0 else repr(minutes) + "mn"
    h = "" if hours == 0 else repr(hours) + "h"
    return " ".join(a for a in [h, min, sec] if a)
    # return repr(dur // 60) + ":" + repr(dur % 60).zfill(2)


def textToDuration(dur):
    h = re.search("([\d]+)*h", dur)
    min = re.search("([\d]+)*mn", dur)
    sec = re.search("([\d]+)*s", dur)
    return (int(h.group(1)) * 3600 if h else 0) + (int(min.group(1)) * 60 if min else 0) + (
        int(sec.group(1)) if sec else 0)
    # spl = dur.split(":")
    # return int(spl[0]) * 60 + int(spl[1])


def average(arr, emp=-1):
    if len(arr) == 0: return emp
    return sum(arr) / float(len(arr))


def audio_addFiles():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.ExistingFiles)
    fn = dialog.getOpenFileNames(None, "Fichiers audio", os.path.expanduser("~"),
                                 "Fichiers audio (*.ac3 *.aif *.aiff *.alac *.ape *.flac *.m4a *.mp3 *.mpc *.oga *.ogg *.wav *.wma *.wv);;" +
                                 "Fichiers audio compressés (*.ac3 *.m4a *.mp3 *.mpc *.ogg *.oga *.wma *.wv);;" +
                                 "Fichiers audio compressés sans perte (*.alac *.ape *.flac *.wma *.wv);;" +
                                 "Fichiers audio non compressés (*.aif *.aiff *.wav)")[
        0]
    if len(fn) == 0: return
    for file in fn:
        if checkArch(file):
            continue
        if file in audiofnames:
            msg = getThemedBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Le fichier '" + file + "' a déjà été ajouté.")
            msg.exec_()
        else:
            audiofnames.append(file)
    audio_updateFiles()


def video_addFiles():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.ExistingFiles)
    fn = dialog.getOpenFileNames(None, "Fichiers vidéo", os.path.expanduser("~"),
                                 "Fichiers vidéo (*.avi *.m2ts *.m4v *.mkv *.mp4 *.mpg *.mpeg *.ogm *.ogv *.wmv)")[
        0]
    if len(fn) == 0: return
    warnShown1 = False
    warnShown2 = False
    for file in fn:
        if checkArch(file):
            continue
        if os.path.splitext(file)[1].lower() == ".m4v" and not warnShown1:
            msg = getThemedBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "<h2>Attention !</h2><p>Les fichiers <b>.m4v</b> ne sont <b><font color=red>acceptés</font></b> que pour les catégories <b>iOS</b> et <b>PSP</b>.</p>")
            msg.exec_()
            warnShown1 = True
        if os.path.splitext(file)[1].lower() == ".wmv" and not warnShown2:
            msg = getThemedBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "<h2>Attention !</h2><p>Les fichiers <b>.wmv</b> ne sont <b><font color=red>acceptés</font></b> que pour le <b>porno</b>.</p>")
            msg.exec_()
            warnShown2 = True
        if file in videofnames:
            msg = getThemedBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Le fichier '" + file + "' a déjà été ajouté.")
            msg.exec_()
        else:
            videofnames.append(file)
    video_updateFiles()


class ROTableItem(QTableWidgetItem):
    def __init__(self, __args):
        QTableWidgetItem.__init__(self, __args)
        self.setFlags(self.flags() & ~2)


def chanTxt(ch):
    c = int(ch)
    if c == 2:
        return "2 (Stéréo)"
    elif c == 4:
        return "4 (Quadriphonie"
    elif c == 6:
        return "6 (Surround 5.1"
    elif c == 8:
        return "8 (Surround 7.1)"
    elif c == 10:
        return "10 (Surround 9.1"
    return ch


def audio_updateFiles():
    dSum = 0
    sSum = 0
    codecs = []
    brates = []
    chan = 0
    enc = []
    genres = []
    freqs = []
    exts = []
    year = -1
    while ui.audio_files.rowCount() > 0:
        ui.audio_files.removeRow(0)  # Vider le tableau
    audiofdata.clear()
    if len(audiofnames) == 0:
        # Tout vider
        ui.audio_totalTime.setText("")
        ui.txt_totalSize.setText("")
        ui.audio_year.setValue(-1)
        ui.audio_codec.setText("")
        ui.audio_channel.setText("")
        ui.audio_encoder.setText("")
        ui.audio_genre.setCurrentIndex(-1)
        ui.audio_avrBitrate.setText("")
        ui.audio_freq.setText("")
        return

    for file in audiofnames:
        if (os.path.isfile(file)):
            rowPos = ui.audio_files.rowCount()
            ui.audio_files.insertRow(rowPos)
            audiofdata[rowPos] = {}
            audiofdata[rowPos]['file'] = file
            ui.audio_files.setItem(rowPos, 1, ROTableItem(os.path.basename(file)))  # Nom du fichier
            mediaInfo = MediaInfo.parse(file)
            track = mediaInfo.tracks[0]
            audioTrack = mediaInfo.tracks[1]
            freqs.append(audioTrack.sampling_rate)
            exts.append(os.path.splitext(file)[1])
            chan = audioTrack.channel_s
            codecs.append(audioTrack.other_codec[0])
            lib = track.writing_library
            if is_ascii(lib) and not "=" in lib and len(lib) < 32:
                enc.append(lib)
            titre = path_leaf(file) if track.track_name is None else track.track_name
            itemN = QTableWidgetItem()
            if track.track_name_position is not None:
                itemN.setData(0, int(track.track_name_position))
            else:
                rx = re.match("(?: *)(\d+)(?: *)(?:[-:]*)(?: *)(.*)(?: *)", titre)
                if rx is not None and len(rx.groups()) == 2:
                    itemN.setData(0, int(rx.group(1)))
                    titre = rx.group(2)
            ui.audio_files.setItem(rowPos, 2, QTableWidgetItem(titre))  # Titre
            ui.audio_files.setItem(rowPos, 0, itemN)  # N°
            ui.audio_files.setItem(rowPos, 3, QTableWidgetItem(
                "[Inconnu]" if track.performer is None else track.performer))  # Interprète(s)
            ui.audio_files.setItem(rowPos, 4,
                                   QTableWidgetItem("[Inconnu]" if track.album is None else track.album))  # Album
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
            brates.append(brate)
            audiofdata[rowPos]['bitrate'] = brate
            ui.audio_files.setItem(rowPos, 7, ROTableItem(sizeof_fmt(brate, 'bps', 1000)))  # Bitrate

    albums = set([ui.audio_files.item(r, 4).text() for r in range(0, ui.audio_files.rowCount())])
    if len(albums) == 2 and "[Inconnu]" in albums:
        other = [a for a in albums if a != "[Inconnu]"][0]
        for r in range(0, ui.audio_files.rowCount()):
            ui.audio_files.setItem(r, 4, QTableWidgetItem(other))
    performers = set([ui.audio_files.item(r, 3).text() for r in range(0, ui.audio_files.rowCount())])
    if len(albums) == 2 and "[Inconnu]" in albums:
        other = [a for a in performers if a != "[Inconnu]"][0]
        for r in range(0, ui.audio_files.rowCount()):
            ui.audio_files.setItem(r, 3, QTableWidgetItem(other))

    # Vérifier multi-bitrate
    for al in albums:
        abrates = [ui.audio_files.item(r, 7).text() for r in range(0, ui.audio_files.rowCount()) if
                   ui.audio_files.item(r, 4).text() == al]
        if len([b for b in abrates if b != abrates[0]]) > 0:
            msg = getThemedBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(
                "<h2>Attention !</h2><p>Le <b>multi-bitrate</b> est <b><font color='red'>interdit</font></b> pour un même album (" + al + ").<br/>Exemple : mélange de 128 Kbps et de 256 Kbps</p>")
            msg.exec_()

    # Vérifier multi-format
    if len([ext for ext in exts if ext != exts[0]]) > 0:
        msg = getThemedBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(
            "<h2>Attention !</h2><p>Le <b>multi-format</b> est <b><font color='red'>interdit</font></b>.<br/>Exemple : mélange de MP3 et de Flac dans un <b>même torrent</b></p>")
        msg.exec_()

    ui.audio_files.sortByColumn(0, 0)
    ui.audio_totalTime.setText(durationToText(int(dSum)))
    ui.txt_totalSize.setText(sizeof_fmt(sSum))
    if year is not None: ui.audio_year.setValue(int(year))
    ui.audio_codec.setText(", ".join(set(codecs)))
    ui.audio_channel.setText(chanTxt(chan))
    ui.audio_encoder.setText(most_common(enc))
    ui.audio_genre.setCurrentText(", ".join(set(genres)))
    ui.audio_avrBitrate.setText(sizeof_fmt(average(brates), 'bps', 1000))
    ui.audio_freq.setText(sizeof_fmt(most_common(freqs), 'Hz', 1000))


def video_updateFiles():
    dSum = 0
    sSum = 0
    exts = []

    while ui.film_files.rowCount() > 0:
        ui.film_files.removeRow(0)  # Vider le tableau
    if len(videofnames) == 0:
        # Tout vider
        ui.txt_totalSize.setText("")
        ui.film_format.setCurrentIndex(-1)
        ui.film_totalTime.setText("")
        return
    videofdata.clear()
    for file in videofnames:
        if (os.path.isfile(file)):
            mediaInfo = MediaInfo.parse(file)
            trackGeneral = mediaInfo.tracks[0]
            tracksVideo = [t for t in mediaInfo.tracks if t.track_type == 'Video']
            if not tracksVideo:
                msg = getThemedBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(
                    "<h2>Attention !</h2><p>Aucune piste vidéo détectée. Fichier ignoré.</p>")
                msg.exec_()
                continue

            trackVideo = tracksVideo[0]
            tracksAudio = [t for t in mediaInfo.tracks if t.track_type == 'Audio']
            tracksText = [t for t in mediaInfo.tracks if t.track_type == 'Text']

            if trackVideo.width < 624 or trackVideo.height < 352:
                msg = getThemedBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(
                    "<h2>Attention !</h2><p>La résolution minimale pour une vidéo est de <b>624x352</b> (ici : {0}x{1}).</p>".format(
                        trackVideo.width, trackVideo.height))
                msg.exec_()
                continue

            exts.append(os.path.splitext(file)[1])
            rowPos = ui.film_files.rowCount()
            ui.film_files.insertRow(rowPos)
            videofdata[rowPos] = {}
            videofdata[rowPos]['file'] = file
            ui.film_files.setItem(rowPos, 0, QTableWidgetItem(os.path.basename(file)))  # Nom du fichier
            ui.film_files.setItem(rowPos, 1,
                                  ROTableItem("{0}x{1}".format(trackVideo.width, trackVideo.height)))  # Résolution
            duree = trackGeneral.duration / 1000
            dSum += duree
            ui.film_files.setItem(rowPos, 2, ROTableItem(durationToText(int(duree), False)))  # Durée
            sSum += trackGeneral.file_size
            ui.film_files.setItem(rowPos, 3, ROTableItem(sizeof_fmt(trackGeneral.file_size)))  # Taille
            ui.film_files.setItem(rowPos, 4, ROTableItem("{0} fps".format(trackVideo.frame_rate)))  # Framerate
            ui.film_files.setItem(rowPos, 5, ROTableItem(sizeof_fmt(trackVideo.bit_rate, "bps",
                                                                    1000) if trackVideo.bit_rate else "<Bitrate inconnu>"))  # Bitrate vidéo
            videofdata[rowPos]['audio'] = \
                [
                    {'id': int(t.stream_identifier) + 1,
                     'lang': getLanguage(t.language),
                     'sampling': t.sampling_rate,
                     'bitrate': t.bit_rate,
                     'channels': t.channel_s,
                     'format': t.format + (" (" + t.format_info + ")" if t.format_info else "")}
                    for t in tracksAudio
                    ]
            videofdata[rowPos]['subtitles'] = \
                [
                    {'id': int(t.stream_identifier) + 1,
                     'lang': getLanguage(t.language),
                     'format': t.format,
                     'title': t.title,
                     'display': (t.title + " (" + getLanguage(t.language) + ")" if t.title and t.title != getLanguage(
                         t.language) else getLanguage(t.language))}
                    for t in tracksText
                    ]
            ui.film_files.setItem(rowPos, 6, ROTableItem(
                str(len(tracksAudio)) if all(x.language == None for x in tracksAudio) else ", ".join(
                    getLanguage(t.language) for t in tracksAudio)))  # Pistes audio
            ui.film_files.setItem(rowPos, 7, ROTableItem("Aucune" if not tracksText else
                                                         str(len(tracksText)) if all(
                                                             x.language == None for x in tracksText) else ", ".join(
                                                             t['display'] for t in
                                                             videofdata[rowPos]['subtitles'])))  # Sous-titres

    # Vérifier multi-format
    if len([ext for ext in exts if ext != exts[0]]) > 0:
        msg = getThemedBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(
            "<h2>Attention !</h2><p>Le <b>multi-format</b> est <b><font color='red'>interdit</font></b>.<br/>Exemple : mélange d'AVI et de MP4 dans un <b>même torrent</b></p>")
        msg.exec_()

    ui.film_files.sortByColumn(0, 0)
    ui.film_totalTime.setText(durationToText(int(dSum), False))
    ui.txt_totalSize.setText(sizeof_fmt(sSum))


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
    if fn != '':
        f = open(fn, "w")
        f.write(ui.plainTextEdit.toPlainText())
        f.close()


def centerStr(str, length):
    import math
    pos = math.ceil(length / 2 - len(str) / 2)
    return " " * pos + str + " " * (length - pos - len(str))


def getHeader(str, sym="-", add=0):
    return sym * (92 + add) + "\n" + centerStr(str, 92 + add) + "\n" + sym * (92 + add) + "\n\n"


def getFields(fields, pad=3, sym=".", fix=-1, removeEmpty=True, noNewLine=False):
    maxl = 21 + pad
    ret = ""
    for f, v in fields.items():
        if removeEmpty and isEmpty(v): continue
        cur = f + sym * (maxl - len(f)) + ": "
        curl = len(cur)
        rem = 92 - curl

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
    if not noNewLine: ret += "\n"
    return ret


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
        msg = getThemedBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Les champs suivants sont requis :<b><ul>" + ''.join(req) + "</ul></b>")
        msg.exec_()
        return False

    return True


def genNFO():
    if not validate(): return

    nfoTop = ""
    nfoTop += "+--------------------------------------------------------------------------------------------------+\n"
    nfoTop += "|*+----------------------------------------------------------------------------------------------+*|\n"
    nfoTop += "|*|                                                                                              |*|\n"

    nfo = ""
    nfo += getHeader(ui.txt_relName.text(), "*", 2)

    cur = getCurPage()

    if cur == 0:  # Audio
        nfo += getHeader("Infos audio")
        nfo += getFields(OrderedDict([
            ("Interprète(s)",
             " ; ".join(set([ui.audio_files.item(r, 3).text() for r in range(0, ui.audio_files.rowCount())]))),
            ("Album(s)", "Discographie" if ui.audio_discographie.isChecked() else " ; ".join(
                set([ui.audio_files.item(r, 4).text() for r in range(0, ui.audio_files.rowCount())]))),
            ("Codec", ui.audio_codec.text()),
            ("Fréquence", ui.audio_freq.text()),
            ("Canaux", ui.audio_channel.text()),
            ("Encodeur", ui.audio_encoder.text()),
            ("Bitrate moyen", ui.audio_avrBitrate.text()),
            ("Genre", ui.audio_genre.currentText()),
            ("Durée totale", ui.audio_totalTime.text()),
            ("Année", ui.audio_year.text()),
            ("Tag ID3 1", ui.audio_id3tag_1.text()),
            ("Tag ID3 2", ui.audio_id3tag_2.text()),
            ("Tag APE", ui.audio_apeTag.text()),
            ("Tag Vorbis", ui.audio_vorbisTag.text()),
            ("Rippeur", "Not My Rip (Pas Mon Rip)" if ui.audio_notMyRip.isChecked() else ui.audio_ripper.text()),
            ("Lecteur", ui.audio_cdmodel.text()),
            ("Source", ui.audio_source.currentText()),
        ]))

        nfo += getHeader("Liste des pistes")
        albums = set([ui.audio_files.item(r, 4).text() for r in range(0, ui.audio_files.rowCount())])
        grouped = [(al, [r for r in range(0, ui.audio_files.rowCount()) if ui.audio_files.item(r, 4).text() == al]) for
                   al in albums]

        for album in grouped:
            nfo += textwrap.fill(
                album[0] + " [" + sizeof_fmt(average([float(audiofdata[r]['bitrate']) for r in album[1]]),
                                             "bps", 1000) + "]", width=76, replace_whitespace=False) + "\n\n"
            lastNum = 0
            for rowID in album[1]:
                tmp = ui.audio_files.item(rowID, 0).text()
                lastNum = orValue(lambda: int(tmp), lastNum + 1)
                h = (str(lastNum) + ". ").rjust(6)
                v = ui.audio_files.item(rowID, 2).text()
                curl = len(h)
                rem = 92 - curl - 15

                spc = " " * curl
                nfo += h
                i = 0
                j = 0
                v = v.ljust(rem)
                dur = ui.audio_files.item(rowID, 6).text().rjust(11)
                for c in v:
                    if c == "\n" or i == rem:
                        if j == 0:
                            nfo += " [" + dur + "]"
                        j = 1
                        nfo += "\n"
                        nfo += spc
                        if c != "\n": nfo += c
                        i = -1
                    else:
                        nfo += c
                    i += 1
                if j == 0:
                    nfo += " [" + dur + "]"
                nfo += "\n"
            nfo += "\n"

        nfo += "\n"

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
        nfo += getHeader("Infos vidéo")
        nfo += getFields(OrderedDict([
            ("Durée totale", ui.film_totalTime.text()),
            ("Format", ui.film_format.currentText())
        ]))

        nfo += getHeader("Liste des fichiers")

        for r in range(0, ui.film_files.rowCount()):
            nfo += ui.film_files.item(r, 0).text() + "\n"
            nfo += "  Durée : " + ui.film_files.item(r, 2).text() + "\n"
            nfo += "  Taille : " + ui.film_files.item(r, 3).text() + "\n"

            # Pistes audio
            audio = videofdata[r]['audio']
            nfo += "  Pistes audio :\n"
            if audio:
                for s in audio:
                    h = (str(s['id']) + ". ").rjust(7)
                    v = ", ".join(
                        [s['lang'], sizeof_fmt(s['bitrate'], "bps", 1000) if s['bitrate'] else "Bitrate inconnu",
                         sizeof_fmt(s['sampling'], "Hz", 1000), str(s['channels']) + " canaux", s['format']])
                    curl = len(h)
                    rem = 91 - curl

                    spc = " " * curl
                    nfo += h
                    i = 0
                    v = v.ljust(rem)
                    for c in v:
                        if c == "\n" or i == rem:
                            nfo += "\n"
                            nfo += spc
                            if c != "\n": nfo += c
                            i = -1
                        else:
                            nfo += c
                        i += 1
                    nfo += "\n"
            else:
                nfo += "    Aucune\n"

            # Pistes sous-titres
            sub = videofdata[r]['subtitles']
            if sub:
                nfo += "  Pistes sous-titres :\n"
                for s in sub:
                    h = (str(s['id']) + ". ").rjust(7)
                    v = s['display'] + ", " + s['format']
                    curl = len(h)
                    rem = 91 - curl

                    spc = " " * curl
                    nfo += h
                    i = 0
                    v = v.ljust(rem)
                    for c in v:
                        if c == "\n" or i == rem:
                            nfo += "\n"
                            nfo += spc
                            if c != "\n": nfo += c
                            i = -1
                        else:
                            nfo += c
                        i += 1
                    nfo += "\n"

            nfo += "\n"

        nfo += "\n"
    elif cur == 4:  # Appli / Jeu
        nfo += getFields(
            {
                "Nom": ui.app_nom.text(),
                "Langue": ui.app_langue.currentText()
            }
            , noNewLine=False)
        if ui.app_swCon.currentIndex() == 0:
            nfo += getFields(
                {
                    "Plateforme": ui.app_os.currentText(),
                    "Config. minimum": ui.app_confMin.toPlainText(),
                    "Étapes d'installation": ui.app_install.toPlainText()
                }
            )
        elif ui.app_swCon.currentIndex() == 1:
            nfo += getFields(
                {
                    "Console": ui.con_type.currentText() + " " + ui.con_console.currentText(),
                    "Firmware": ui.con_firmw.text()
                }
            )
        elif ui.app_swCon.currentIndex() == 2:
            nfo += getFields(
                {
                    "Console": ui.retro_type.currentText() + " " + ui.retro_console.currentText()
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
    nfoBottom += "|*|                                                                                              |*|\n"
    nfoBottom += "|*|                                                                                              |*|\n"
    nfoBottom += "|*|      |--------------------------------------------------------------------------------|      |*|\n"
    nfoBottom += "|*+------|                        NFO créé avec t411nfobuilder X.X                        |------+*|\n".replace(
        "X.X", __version__)
    nfoBottom += "+--------|                  https://github.com/zdimension/t411nfobuilder                  |--------+\n"
    nfoBottom += "         |--------------------------------------------------------------------------------|         \n"
    nfo = nfoTop + "\n".join(["|*|" + x.ljust(93).rjust(94) + "|*|" for x in nfo.split("\n")]) + nfoBottom

    ui.plainTextEdit.setPlainText(nfo)
    ui.stackedWidget.setCurrentIndex(2)


app = QApplication(sys.argv)
DEFAULT_STYLE = QStyleFactory.create(app.style().objectName())
app.setStyle(QStyleFactory.create("Fusion"))
window = myMainWindow()
ui = Ui_MainWindow()
initUi()
uiInitialized = True
# window.show()
exitCode = app.exec_()
sys.exit(exitCode)
