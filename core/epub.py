import os as _os
import datetime as _datetime
import re as _re
import shutil as _shutil
import zipfile as _zipfile
from .uid import uuid

_MEDIA_TYPE = {
    "load": "text/html",
    "123": "application/vnd.lotus-1-2-3",
    "3ds": "image/x-3ds",
    "3g2": "video/3gpp",
    "3ga": "video/3gpp",
    "3gp": "video/3gpp",
    "3gpp": "video/3gpp",
    "602": "application/x-t602",
    "669": "audio/x-mod",
    "7z": "application/x-7z-compressed",
    "a": "application/x-archive",
    "aac": "audio/mp4",
    "abw": "application/x-abiword",
    "abw.crashed": "application/x-abiword",
    "abw.gz": "application/x-abiword",
    "ac3": "audio/ac3",
    "ace": "application/x-ace",
    "adb": "text/x-adasrc",
    "ads": "text/x-adasrc",
    "afm": "application/x-font-afm",
    "ag": "image/x-applix-graphics",
    "ai": "application/illustrator",
    "aif": "audio/x-aiff",
    "aifc": "audio/x-aiff",
    "aiff": "audio/x-aiff",
    "al": "application/x-perl",
    "alz": "application/x-alz",
    "amr": "audio/amr",
    "ani": "application/x-navi-animation",
    "anim[1-9j]": "video/x-anim",
    "anx": "application/annodex",
    "ape": "audio/x-ape",
    "arj": "application/x-arj",
    "arw": "image/x-sony-arw",
    "as": "application/x-applix-spreadsheet",
    "asc": "text/plain",
    "asf": "video/x-ms-asf",
    "asp": "application/x-asp",
    "ass": "text/x-ssa",
    "asx": "audio/x-ms-asx",
    "atom": "application/atom+xml",
    "au": "audio/basic",
    "avi": "video/x-msvideo",
    "aw": "application/x-applix-word",
    "awb": "audio/amr-wb",
    "awk": "application/x-awk",
    "axa": "audio/annodex",
    "axv": "video/annodex",
    "bak": "application/x-trash",
    "bcpio": "application/x-bcpio",
    "bdf": "application/x-font-bdf",
    "bib": "text/x-bibtex",
    "bin": "application/octet-stream",
    "blend": "application/x-blender",
    "blender": "application/x-blender",
    "bmp": "image/bmp",
    "bz": "application/x-bzip",
    "bz2": "application/x-bzip",
    "c": "text/x-csrc",
    "c++": "text/x-c++src",
    "cab": "application/vnd.ms-cab-compressed",
    "cb7": "application/x-cb7",
    "cbr": "application/x-cbr",
    "cbt": "application/x-cbt",
    "cbz": "application/x-cbz",
    "cc": "text/x-c++src",
    "cdf": "application/x-netcdf",
    "cdr": "application/vnd.corel-draw",
    "cer": "application/x-x509-ca-cert",
    "cert": "application/x-x509-ca-cert",
    "cgm": "image/cgm",
    "chm": "application/x-chm",
    "chrt": "application/x-kchart",
    "class": "application/x-java",
    "cls": "text/x-tex",
    "cmake": "text/x-cmake",
    "cpio": "application/x-cpio",
    "cpio.gz": "application/x-cpio-compressed",
    "cpp": "text/x-c++src",
    "cr2": "image/x-canon-cr2",
    "crt": "application/x-x509-ca-cert",
    "crw": "image/x-canon-crw",
    "cs": "text/x-csharp",
    "csh": "application/x-csh",
    "css": "text/css",
    "cssl": "text/css",
    "csv": "text/csv",
    "cue": "application/x-cue",
    "cur": "image/x-win-bitmap",
    "cxx": "text/x-c++src",
    "d": "text/x-dsrc",
    "dar": "application/x-dar",
    "dbf": "application/x-dbf",
    "dc": "application/x-dc-rom",
    "dcl": "text/x-dcl",
    "dcm": "application/dicom",
    "dcr": "image/x-kodak-dcr",
    "dds": "image/x-dds",
    "deb": "application/x-deb",
    "der": "application/x-x509-ca-cert",
    "desktop": "application/x-desktop",
    "dia": "application/x-dia-diagram",
    "diff": "text/x-patch",
    "divx": "video/x-msvideo",
    "djv": "image/vnd.djvu",
    "djvu": "image/vnd.djvu",
    "dng": "image/x-adobe-dng",
    "doc": "application/msword",
    "docbook": "application/docbook+xml",
    "docm": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "dot": "text/vnd.graphviz",
    "dsl": "text/x-dsl",
    "dtd": "application/xml-dtd",
    "dtx": "text/x-tex",
    "dv": "video/dv",
    "dvi": "application/x-dvi",
    "dvi.bz2": "application/x-bzdvi",
    "dvi.gz": "application/x-gzdvi",
    "dwg": "image/vnd.dwg",
    "dxf": "image/vnd.dxf",
    "e": "text/x-eiffel",
    "egon": "application/x-egon",
    "eif": "text/x-eiffel",
    "el": "text/x-emacs-lisp",
    "emf": "image/x-emf",
    "emp": "application/vnd.emusic-emusic_package",
    "ent": "application/xml-external-parsed-entity",
    "eps": "image/x-eps",
    "eps.bz2": "image/x-bzeps",
    "eps.gz": "image/x-gzeps",
    "epsf": "image/x-eps",
    "epsf.bz2": "image/x-bzeps",
    "epsf.gz": "image/x-gzeps",
    "epsi": "image/x-eps",
    "epsi.bz2": "image/x-bzeps",
    "epsi.gz": "image/x-gzeps",
    "epub": "application/epub+zip",
    "erl": "text/x-erlang",
    "es": "application/ecmascript",
    "etheme": "application/x-e-theme",
    "etx": "text/x-setext",
    "exe": "application/x-ms-dos-executable",
    "exr": "image/x-exr",
    "ez": "application/andrew-inset",
    "f": "text/x-fortran",
    "f90": "text/x-fortran",
    "f95": "text/x-fortran",
    "fb2": "application/x-fictionbook+xml",
    "fig": "image/x-xfig",
    "fits": "image/fits",
    "fl": "application/x-fluid",
    "flac": "audio/x-flac",
    "flc": "video/x-flic",
    "fli": "video/x-flic",
    "flv": "video/x-flv",
    "flw": "application/x-kivio",
    "fo": "text/x-xslfo",
    "for": "text/x-fortran",
    "g3": "image/fax-g3",
    "gb": "application/x-gameboy-rom",
    "gba": "application/x-gba-rom",
    "gcrd": "text/directory",
    "ged": "application/x-gedcom",
    "gedcom": "application/x-gedcom",
    "gen": "application/x-genesis-rom",
    "gf": "application/x-tex-gf",
    "gg": "application/x-sms-rom",
    "gif": "image/gif",
    "glade": "application/x-glade",
    "gmo": "application/x-gettext-translation",
    "gnc": "application/x-gnucash",
    "gnd": "application/gnunet-directory",
    "gnucash": "application/x-gnucash",
    "gnumeric": "application/x-gnumeric",
    "gnuplot": "application/x-gnuplot",
    "gp": "application/x-gnuplot",
    "gpg": "application/pgp-encrypted",
    "gplt": "application/x-gnuplot",
    "gra": "application/x-graphite",
    "gsf": "application/x-font-type1",
    "gsm": "audio/x-gsm",
    "gtar": "application/x-tar",
    "gv": "text/vnd.graphviz",
    "gvp": "text/x-google-video-pointer",
    "gz": "application/x-gzip",
    "h": "text/x-chdr",
    "h++": "text/x-c++hdr",
    "hdf": "application/x-hdf",
    "hh": "text/x-c++hdr",
    "hp": "text/x-c++hdr",
    "hpgl": "application/vnd.hp-hpgl",
    "hpp": "text/x-c++hdr",
    "hs": "text/x-haskell",
    #"htm": "text/html",
    #"html": "text/html",
    "htm": "application/xhtml+xml",
    "html": "application/xhtml+xml",
    "hwp": "application/x-hwp",
    "hwt": "application/x-hwt",
    "hxx": "text/x-c++hdr",
    "ica": "application/x-ica",
    "icb": "image/x-tga",
    "icns": "image/x-icns",
    "ico": "image/vnd.microsoft.icon",
    "ics": "text/calendar",
    "idl": "text/x-idl",
    "ief": "image/ief",
    "iff": "image/x-iff",
    "ilbm": "image/x-ilbm",
    "ime": "text/x-imelody",
    "imy": "text/x-imelody",
    "ins": "text/x-tex",
    "iptables": "text/x-iptables",
    "iso": "application/x-cd-image",
    "iso9660": "application/x-cd-image",
    "it": "audio/x-it",
    "j2k": "image/jp2",
    "jad": "text/vnd.sun.j2me.app-descriptor",
    "jar": "application/x-java-archive",
    "java": "text/x-java",
    "jng": "image/x-jng",
    "jnlp": "application/x-java-jnlp-file",
    "jp2": "image/jp2",
    "jpc": "image/jp2",
    "jpe": "image/jpeg",
    "jpeg": "image/jpeg",
    "jpf": "image/jp2",
    "jpg": "image/jpeg",
    "jpr": "application/x-jbuilder-project",
    "jpx": "image/jp2",
    "js": "application/javascript",
    "json": "application/json",
    "jsonp": "application/jsonp",
    "k25": "image/x-kodak-k25",
    "kar": "audio/midi",
    "karbon": "application/x-karbon",
    "kdc": "image/x-kodak-kdc",
    "kdelnk": "application/x-desktop",
    "kexi": "application/x-kexiproject-sqlite3",
    "kexic": "application/x-kexi-connectiondata",
    "kexis": "application/x-kexiproject-shortcut",
    "kfo": "application/x-kformula",
    "kil": "application/x-killustrator",
    "kino": "application/smil",
    "kml": "application/vnd.google-earth.kml+xml",
    "kmz": "application/vnd.google-earth.kmz",
    "kon": "application/x-kontour",
    "kpm": "application/x-kpovmodeler",
    "kpr": "application/x-kpresenter",
    "kpt": "application/x-kpresenter",
    "kra": "application/x-krita",
    "ksp": "application/x-kspread",
    "kud": "application/x-kugar",
    "kwd": "application/x-kword",
    "kwt": "application/x-kword",
    "la": "application/x-shared-library-la",
    "latex": "text/x-tex",
    "ldif": "text/x-ldif",
    "lha": "application/x-lha",
    "lhs": "text/x-literate-haskell",
    "lhz": "application/x-lhz",
    "log": "text/x-log",
    "ltx": "text/x-tex",
    "lua": "text/x-lua",
    "lwo": "image/x-lwo",
    "lwob": "image/x-lwo",
    "lws": "image/x-lws",
    "ly": "text/x-lilypond",
    "lyx": "application/x-lyx",
    "lz": "application/x-lzip",
    "lzh": "application/x-lha",
    "lzma": "application/x-lzma",
    "lzo": "application/x-lzop",
    "m": "text/x-matlab",
    "m15": "audio/x-mod",
    "m2t": "video/mpeg",
    "m3u": "audio/x-mpegurl",
    "m3u8": "audio/x-mpegurl",
    "m4": "application/x-m4",
    "m4a": "audio/mp4",
    "m4b": "audio/x-m4b",
    "m4v": "video/mp4",
    "mab": "application/x-markaby",
    "man": "application/x-troff-man",
    "mbox": "application/mbox",
    "md": "application/x-genesis-rom",
    "mdb": "application/vnd.ms-access",
    "mdi": "image/vnd.ms-modi",
    "me": "text/x-troff-me",
    "med": "audio/x-mod",
    "metalink": "application/metalink+xml",
    "mgp": "application/x-magicpoint",
    "mid": "audio/midi",
    "midi": "audio/midi",
    "mif": "application/x-mif",
    "minipsf": "audio/x-minipsf",
    "mka": "audio/x-matroska",
    "mkv": "video/x-matroska",
    "ml": "text/x-ocaml",
    "mli": "text/x-ocaml",
    "mm": "text/x-troff-mm",
    "mmf": "application/x-smaf",
    "mml": "text/mathml",
    "mng": "video/x-mng",
    "mo": "application/x-gettext-translation",
    "mo3": "audio/x-mo3",
    "moc": "text/x-moc",
    "mod": "audio/x-mod",
    "mof": "text/x-mof",
    "moov": "video/quicktime",
    "mov": "video/quicktime",
    "movie": "video/x-sgi-movie",
    "mp+": "audio/x-musepack",
    "mp2": "video/mpeg",
    "mp3": "audio/mpeg",
    "mp4": "video/mp4",
    "mpc": "audio/x-musepack",
    "mpe": "video/mpeg",
    "mpeg": "video/mpeg",
    "mpg": "video/mpeg",
    "mpga": "audio/mpeg",
    "mpp": "audio/x-musepack",
    "mrl": "text/x-mrml",
    "mrml": "text/x-mrml",
    "mrw": "image/x-minolta-mrw",
    "ms": "text/x-troff-ms",
    "msi": "application/x-msi",
    "msod": "image/x-msod",
    "msx": "application/x-msx-rom",
    "mtm": "audio/x-mod",
    "mup": "text/x-mup",
    "mxf": "application/mxf",
    "n64": "application/x-n64-rom",
    "nb": "application/mathematica",
    "nc": "application/x-netcdf",
    "ncx": "application/x-dtbncx+xml",
    "nds": "application/x-nintendo-ds-rom",
    "nef": "image/x-nikon-nef",
    "nes": "application/x-nes-rom",
    "nfo": "text/x-nfo",
    "not": "text/x-mup",
    "nsc": "application/x-netshow-channel",
    "nsv": "video/x-nsv",
    "o": "application/x-object",
    "obj": "application/x-tgif",
    "ocl": "text/x-ocl",
    "oda": "application/oda",
    "odb": "application/vnd.oasis.opendocument.database",
    "odc": "application/vnd.oasis.opendocument.chart",
    "odf": "application/vnd.oasis.opendocument.formula",
    "odg": "application/vnd.oasis.opendocument.graphics",
    "odi": "application/vnd.oasis.opendocument.image",
    "odm": "application/vnd.oasis.opendocument.text-master",
    "odp": "application/vnd.oasis.opendocument.presentation",
    "ods": "application/vnd.oasis.opendocument.spreadsheet",
    "odt": "application/vnd.oasis.opendocument.text",
    "oga": "audio/ogg",
    "ogg": "video/x-theora+ogg",
    "ogm": "video/x-ogm+ogg",
    "ogv": "video/ogg",
    "ogx": "application/ogg",
    "old": "application/x-trash",
    "oleo": "application/x-oleo",
    "opml": "text/x-opml+xml",
    "ora": "image/openraster",
    "orf": "image/x-olympus-orf",
    "otc": "application/vnd.oasis.opendocument.chart-template",
    "otf": "application/x-font-otf",
    "otg": "application/vnd.oasis.opendocument.graphics-template",
    "oth": "application/vnd.oasis.opendocument.text-web",
    "otp": "application/vnd.oasis.opendocument.presentation-template",
    "ots": "application/vnd.oasis.opendocument.spreadsheet-template",
    "ott": "application/vnd.oasis.opendocument.text-template",
    "owl": "application/rdf+xml",
    "oxt": "application/vnd.openofficeorg.extension",
    "p": "text/x-pascal",
    "p10": "application/pkcs10",
    "p12": "application/x-pkcs12",
    "p7b": "application/x-pkcs7-certificates",
    "p7s": "application/pkcs7-signature",
    "pack": "application/x-java-pack200",
    "pak": "application/x-pak",
    "par2": "application/x-par2",
    "pas": "text/x-pascal",
    "patch": "text/x-patch",
    "pbm": "image/x-portable-bitmap",
    "pcd": "image/x-photo-cd",
    "pcf": "application/x-cisco-vpn-settings",
    "pcf.gz": "application/x-font-pcf",
    "pcf.z": "application/x-font-pcf",
    "pcl": "application/vnd.hp-pcl",
    "pcx": "image/x-pcx",
    "pdb": "chemical/x-pdb",
    "pdc": "application/x-aportisdoc",
    "pdf": "application/pdf",
    "pdf.bz2": "application/x-bzpdf",
    "pdf.gz": "application/x-gzpdf",
    "pef": "image/x-pentax-pef",
    "pem": "application/x-x509-ca-cert",
    "perl": "application/x-perl",
    "pfa": "application/x-font-type1",
    "pfb": "application/x-font-type1",
    "pfx": "application/x-pkcs12",
    "pgm": "image/x-portable-graymap",
    "pgn": "application/x-chess-pgn",
    "pgp": "application/pgp-encrypted",
    "php": "application/x-php",
    "php3": "application/x-php",
    "php4": "application/x-php",
    "pict": "image/x-pict",
    "pict1": "image/x-pict",
    "pict2": "image/x-pict",
    "pickle": "application/python-pickle",
    "pk": "application/x-tex-pk",
    "pkipath": "application/pkix-pkipath",
    "pkr": "application/pgp-keys",
    "pl": "application/x-perl",
    "pla": "audio/x-iriver-pla",
    "pln": "application/x-planperfect",
    "pls": "audio/x-scpls",
    "pm": "application/x-perl",
    "png": "image/png",
    "pnm": "image/x-portable-anymap",
    "pntg": "image/x-macpaint",
    "po": "text/x-gettext-translation",
    "por": "application/x-spss-por",
    "pot": "text/x-gettext-translation-template",
    "ppm": "image/x-portable-pixmap",
    "pps": "application/vnd.ms-powerpoint",
    "ppt": "application/vnd.ms-powerpoint",
    "pptm": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "ppz": "application/vnd.ms-powerpoint",
    "prc": "application/x-palm-database",
    "ps": "application/postscript",
    "ps.bz2": "application/x-bzpostscript",
    "ps.gz": "application/x-gzpostscript",
    "psd": "image/vnd.adobe.photoshop",
    "psf": "audio/x-psf",
    "psf.gz": "application/x-gz-font-linux-psf",
    "psflib": "audio/x-psflib",
    "psid": "audio/prs.sid",
    "psw": "application/x-pocket-word",
    "pw": "application/x-pw",
    "py": "text/x-python",
    "pyc": "application/x-python-bytecode",
    "pyo": "application/x-python-bytecode",
    "qif": "image/x-quicktime",
    "qt": "video/quicktime",
    "qtif": "image/x-quicktime",
    "qtl": "application/x-quicktime-media-link",
    "qtvr": "video/quicktime",
    "ra": "audio/vnd.rn-realaudio",
    "raf": "image/x-fuji-raf",
    "ram": "application/ram",
    "rar": "application/x-rar",
    "ras": "image/x-cmu-raster",
    "raw": "image/x-panasonic-raw",
    "rax": "audio/vnd.rn-realaudio",
    "rb": "application/x-ruby",
    "rdf": "application/rdf+xml",
    "rdfs": "application/rdf+xml",
    "reg": "text/x-ms-regedit",
    "rej": "application/x-reject",
    "rgb": "image/x-rgb",
    "rle": "image/rle",
    "rm": "application/vnd.rn-realmedia",
    "rmj": "application/vnd.rn-realmedia",
    "rmm": "application/vnd.rn-realmedia",
    "rms": "application/vnd.rn-realmedia",
    "rmvb": "application/vnd.rn-realmedia",
    "rmx": "application/vnd.rn-realmedia",
    "roff": "text/troff",
    "rp": "image/vnd.rn-realpix",
    "rpm": "application/x-rpm",
    "rss": "application/rss+xml",
    "rt": "text/vnd.rn-realtext",
    "rtf": "application/rtf",
    "rtx": "text/richtext",
    "rv": "video/vnd.rn-realvideo",
    "rvx": "video/vnd.rn-realvideo",
    "s3m": "audio/x-s3m",
    "sam": "application/x-amipro",
    "sami": "application/x-sami",
    "sav": "application/x-spss-sav",
    "scm": "text/x-scheme",
    "sda": "application/vnd.stardivision.draw",
    "sdc": "application/vnd.stardivision.calc",
    "sdd": "application/vnd.stardivision.impress",
    "sdp": "application/sdp",
    "sds": "application/vnd.stardivision.chart",
    "sdw": "application/vnd.stardivision.writer",
    "sgf": "application/x-go-sgf",
    "sgi": "image/x-sgi",
    "sgl": "application/vnd.stardivision.writer",
    "sgm": "text/sgml",
    "sgml": "text/sgml",
    "sh": "application/x-shellscript",
    "shar": "application/x-shar",
    "shn": "application/x-shorten",
    "siag": "application/x-siag",
    "sid": "audio/prs.sid",
    "sik": "application/x-trash",
    "sis": "application/vnd.symbian.install",
    "sisx": "x-epoc/x-sisx-app",
    "sit": "application/x-stuffit",
    "siv": "application/sieve",
    "sk": "image/x-skencil",
    "sk1": "image/x-skencil",
    "skr": "application/pgp-keys",
    "slk": "text/spreadsheet",
    "smaf": "application/x-smaf",
    "smc": "application/x-snes-rom",
    "smd": "application/vnd.stardivision.mail",
    "smf": "application/vnd.stardivision.math",
    "smi": "application/x-sami",
    "smil": "application/smil",
    "sml": "application/smil",
    "sms": "application/x-sms-rom",
    "snd": "audio/basic",
    "so": "application/x-sharedlib",
    "spc": "application/x-pkcs7-certificates",
    "spd": "application/x-font-speedo",
    "spec": "text/x-rpm-spec",
    "spl": "application/x-shockwave-flash",
    "spx": "audio/x-speex",
    "sql": "text/x-sql",
    "sr2": "image/x-sony-sr2",
    "src": "application/x-wais-source",
    "srf": "image/x-sony-srf",
    "srt": "application/x-subrip",
    "ssa": "text/x-ssa",
    "stc": "application/vnd.sun.xml.calc.template",
    "std": "application/vnd.sun.xml.draw.template",
    "sti": "application/vnd.sun.xml.impress.template",
    "stm": "audio/x-stm",
    "stw": "application/vnd.sun.xml.writer.template",
    "sty": "text/x-tex",
    "sub": "text/x-subviewer",
    "sun": "image/x-sun-raster",
    "sv4cpio": "application/x-sv4cpio",
    "sv4crc": "application/x-sv4crc",
    "svg": "image/svg+xml",
    "svgz": "image/svg+xml-compressed",
    "swf": "application/x-shockwave-flash",
    "sxc": "application/vnd.sun.xml.calc",
    "sxd": "application/vnd.sun.xml.draw",
    "sxg": "application/vnd.sun.xml.writer.global",
    "sxi": "application/vnd.sun.xml.impress",
    "sxm": "application/vnd.sun.xml.math",
    "sxw": "application/vnd.sun.xml.writer",
    "sylk": "text/spreadsheet",
    "t": "text/troff",
    "t2t": "text/x-txt2tags",
    "tar": "application/x-tar",
    "tar.bz": "application/x-bzip-compressed-tar",
    "tar.bz2": "application/x-bzip-compressed-tar",
    "tar.gz": "application/x-compressed-tar",
    "tar.lzma": "application/x-lzma-compressed-tar",
    "tar.lzo": "application/x-tzo",
    "tar.xz": "application/x-xz-compressed-tar",
    "tar.z": "application/x-tarz",
    "tbz": "application/x-bzip-compressed-tar",
    "tbz2": "application/x-bzip-compressed-tar",
    "tcl": "text/x-tcl",
    "tex": "text/x-tex",
    "texi": "text/x-texinfo",
    "texinfo": "text/x-texinfo",
    "tga": "image/x-tga",
    "tgz": "application/x-compressed-tar",
    "theme": "application/x-theme",
    "themepack": "application/x-windows-themepack",
    "tif": "image/tiff",
    "tiff": "image/tiff",
    "tk": "text/x-tcl",
    "tlz": "application/x-lzma-compressed-tar",
    "tnef": "application/vnd.ms-tnef",
    "tnf": "application/vnd.ms-tnef",
    "toc": "application/x-cdrdao-toc",
    "torrent": "application/x-bittorrent",
    "tpic": "image/x-tga",
    "tr": "text/troff",
    "ts": "application/x-linguist",
    "tsv": "text/tab-separated-values",
    "tta": "audio/x-tta",
    "ttc": "application/x-font-ttf",
    "ttf": "application/x-font-ttf",
    "ttx": "application/x-font-ttx",
    "txt": "text/plain",
    "txz": "application/x-xz-compressed-tar",
    "tzo": "application/x-tzo",
    "ufraw": "application/x-ufraw",
    "ui": "application/x-designer",
    "uil": "text/x-uil",
    "ult": "audio/x-mod",
    "uni": "audio/x-mod",
    "uri": "text/x-uri",
    "url": "text/x-uri",
    "ustar": "application/x-ustar",
    "vala": "text/x-vala",
    "vapi": "text/x-vala",
    "vcf": "text/directory",
    "vcs": "text/calendar",
    "vct": "text/directory",
    "vda": "image/x-tga",
    "vhd": "text/x-vhdl",
    "vhdl": "text/x-vhdl",
    "viv": "video/vivo",
    "vivo": "video/vivo",
    "vlc": "audio/x-mpegurl",
    "vob": "video/mpeg",
    "voc": "audio/x-voc",
    "vor": "application/vnd.stardivision.writer",
    "vst": "image/x-tga",
    "wav": "audio/x-wav",
    "wax": "audio/x-ms-asx",
    "wb1": "application/x-quattropro",
    "wb2": "application/x-quattropro",
    "wb3": "application/x-quattropro",
    "wbmp": "image/vnd.wap.wbmp",
    "wcm": "application/vnd.ms-works",
    "wdb": "application/vnd.ms-works",
    "webm": "video/webm",
    "wk1": "application/vnd.lotus-1-2-3",
    "wk3": "application/vnd.lotus-1-2-3",
    "wk4": "application/vnd.lotus-1-2-3",
    "wks": "application/vnd.ms-works",
    "wma": "audio/x-ms-wma",
    "wmf": "image/x-wmf",
    "wml": "text/vnd.wap.wml",
    "wmls": "text/vnd.wap.wmlscript",
    "wmv": "video/x-ms-wmv",
    "wmx": "audio/x-ms-asx",
    "wp": "application/vnd.wordperfect",
    "wp4": "application/vnd.wordperfect",
    "wp5": "application/vnd.wordperfect",
    "wp6": "application/vnd.wordperfect",
    "wpd": "application/vnd.wordperfect",
    "wpg": "application/x-wpg",
    "wpl": "application/vnd.ms-wpl",
    "wpp": "application/vnd.wordperfect",
    "wps": "application/vnd.ms-works",
    "wri": "application/x-mswrite",
    "wrl": "model/vrml",
    "wv": "audio/x-wavpack",
    "wvc": "audio/x-wavpack-correction",
    "wvp": "audio/x-wavpack",
    "wvx": "audio/x-ms-asx",
    "x3f": "image/x-sigma-x3f",
    "xac": "application/x-gnucash",
    "xbel": "application/x-xbel",
    "xbl": "application/xml",
    "xbm": "image/x-xbitmap",
    "xcf": "image/x-xcf",
    "xcf.bz2": "image/x-compressed-xcf",
    "xcf.gz": "image/x-compressed-xcf",
    "xhtml": "application/xhtml+xml",
    "xi": "audio/x-xi",
    "xla": "application/vnd.ms-excel",
    "xlc": "application/vnd.ms-excel",
    "xld": "application/vnd.ms-excel",
    "xlf": "application/x-xliff",
    "xliff": "application/x-xliff",
    "xll": "application/vnd.ms-excel",
    "xlm": "application/vnd.ms-excel",
    "xls": "application/vnd.ms-excel",
    "xlsm": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "xlt": "application/vnd.ms-excel",
    "xlw": "application/vnd.ms-excel",
    "xm": "audio/x-xm",
    "xmf": "audio/x-xmf",
    "xmi": "text/x-xmi",
    "xml": "application/xml",
    "xpm": "image/x-xpixmap",
    "xps": "application/vnd.ms-xpsdocument",
    "xsl": "application/xml",
    "xslfo": "text/x-xslfo",
    "xslt": "application/xml",
    "xspf": "application/xspf+xml",
    "xul": "application/vnd.mozilla.xul+xml",
    "xwd": "image/x-xwindowdump",
    "xyz": "chemical/x-pdb",
    "xz": "application/x-xz",
    "w2p": "application/w2p",
    "z": "application/x-compress",
    "zabw": "application/x-abiword",
    "zip": "application/zip",
}

def _file_escape(s):
    return _re.sub(r'[\t:/\\*?<>|"\']', r'_', s)

def _ext(path: str) -> str:
    """
    To get extension of a file from its path.
    :param path: path of the file
    :return: file extension
    """
    rf = path.rfind(_os.extsep)
    if rf >= 0:
        return path[rf + 1:]
    return ""

def _media_type(file):
    ext = _ext(file)
    return _MEDIA_TYPE.get(ext, None)

media_type = _media_type

class DocItem:
    def __init__(self, name, **kwargs):
        self.__name = name
        self.__items = kwargs
        items = ''.join(map(lambda x: f' opf:{x[0]}="{x[1]}"', self.__items.items()))
        self.__front_str = f'<dc:{self.__name}{items}>'
        self.__back_str = f'</dc:{self.__name}>'
        self.__str_form = self.__front_str + self.__back_str

    @property
    def name(self):
        return self.__name

    @property
    def items(self):
        return self.__items.copy()

    @property
    def front(self):
        return self.__front_str

    @property
    def back(self):
        return self.__back_str

    def __str__(self):
        return self.__str_form

    def __hash__(self):
        return hash(self.__str_form)

    def __eq__(self, other):
        return self.__str_form == str(other)

META_IDENTIFIER_ISBN = DocItem('identifier', scheme='ISBN')
META_CREATOR_AUTHOR = DocItem('creator', role='aut')

class Metadata:
    def __init__(self):
        self.doc_data = {
            DocItem('title'): None,
            META_IDENTIFIER_ISBN: None,
            DocItem('language'): 'zh-CN',
            META_CREATOR_AUTHOR: None,
            DocItem('publisher'): None,
            DocItem('description'): None,
            DocItem('coverage'): None,
            DocItem('source'): None,
            DocItem('date'): None,
            DocItem('rights'): None,
            DocItem('subject'): None,
            DocItem('contributor'): None,
            DocItem('type'): None,
            DocItem('format'): None,
            DocItem('relation'): None,
            DocItem('builder'): None,
            DocItem('builder_version'): None
        }
        self.metadata = {
            'dtb:uid': uuid(),
            'dtb:depth': 1,
            'dtb:totalPageCount': 0,
            'dtb:maxPageNumber': 0,
            'provider': '',
            'builder': '',
            'right': '',
        }
        self.items = []
        self.add_item('main-css', 'css/main.css')
        self.add_item('ncx', 'fb.ncx')
        self.add_item('js', 'js/main.js')
        self.cover_page = None
        self.cover_page_name = None
        self.cover_image = None
        self.doc_title = None
        self.doc_author = None
        self.page_metadata = {
            'provider': '',
            'builder': '',
            'right': '',
        }

    def add_doc_data(self, name, content, **kwargs):
        self.doc_data[DocItem(name, **kwargs)] = content

    def add_item(self, id, href, media_type=None):
        if media_type is None:
            media_type = _media_type(href)
        if media_type is None:
            media_type = ""
        self.items.append((id, href, media_type))

    def ncx(self, pages):
        ncx_meta = '\n'.join(map(lambda x: f'    <meta name="{x[0]}" content="{x[1]}"/>', self.metadata.items()))
        ncx_nav_points = '\n'.join(map(lambda x:f"""<navPoint id="{x[1][0]}" playOrder="{x[0]}">
<navLabel><text>{x[1][1]}</text></navLabel>
<content src="{x[1][2].file}"/>
</navPoint>""", enumerate(pages)))
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC
     "-//NISO//DTD ncx 2005-1//EN"
     "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx version="2005-1"
     xml:lang="en-US"
     xmlns="http://www.daisy.org/z3986/2005/ncx/">
  <head>
    <!-- The following four metadata items are required for all
        NCX documents, including those conforming to the relaxed
        constraints of OPS 2.0 -->
{ncx_meta}
  </head>
<docTitle><text>{"" if self.doc_title is None else self.doc_title}</text></docTitle>
<docAuthor><text>{"" if self.doc_author is None else self.doc_author}</text></docAuthor>
<navMap>
{ncx_nav_points}
</navMap>
</ncx>
"""

    def opf(self, pages):
        doc_data = '\n'.join(map(lambda x: x[0].front + str('' if x[1] is None else x[1]) + x[0].back, self.doc_data.items()))
        page_items = '\n'.join(map(lambda x: f'<item id="{x[0]}" href="{x[2].file}" media-type="application/xhtml+xml"/>', pages))
        items = '\n'.join(map(lambda x: f'<item id="{x[0]}" href="{x[1]}" media-type="{x[2]}"/>', self.items))
        page_nav = '\n'.join(map(lambda x: f'<itemref idref="{x[0]}" linear="yes"/>', pages))
        cover_image = "" if self.cover_image is None else self.cover_image
        cover_image_media_type = _media_type(cover_image)
        cover_image_tag = '' if self.cover_image is None else f'<item id="cover-image" href="{cover_image}" media-type="{cover_image_media_type}"/>\n'
        return f"""<?xml version="1.0" encoding="UTF-8" ?>
<package version="2.0" unique-identifier="PrimaryID" xmlns="http://www.idpf.org/2007/opf">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
{doc_data}
<meta name="cover" content="cover-image"/>
</metadata>
<manifest>
<!-- Content Documents -->
{page_items}
{items}
{cover_image_tag}</manifest>
<spine toc="ncx">
{page_nav}
</spine>
<guide>
<reference type="cover" title="{"Cover" if self.cover_page_name is None else self.cover_page_name}" href="{self.cover_page}"/>
</guide>
</package>
"""

class Page:
    def __init__(self, file, metadata : Metadata, content=None, title=None, css=('css/main.css',), js=('js/main.js',)):
        self.file = file
        self.title = title
        self.metadata = metadata
        self.content = content
        self.css = [*css] if css else []
        self.js = [*js] if js else []

    def __str__(self):
        meta = ''.join(map(lambda x: f'<meta name="{x[0]}" content="{x[1]}"/>\n', self.metadata.page_metadata.items()))
        css = ''.join((f'<link rel="stylesheet" type="text/css" href="{_css}"/>\n' for _css in self.css))
        js = ''.join((f'<script src="{_js}" type="text/javascript"></script>\n' for _js in self.js))
        content = '' if self.content is None else self.content
        return f"""<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
{meta}{css}{js}<title>{'' if self.title is None else self.title}</title>
</head>
<body>
<div>
{content}</div>
</body>
</html>
"""

    @classmethod
    def cover(cls, image_src, file, metadata, title=None):
        content = f'<div style="text-align:center"><img class="cover" src="images/{image_src}"/></div>'
        return cls(file, metadata, content, title)

def _now():
    return _datetime.datetime.now().date().strftime('%Y-%m-%d')

def _pwd():
    return _os.path.abspath(_os.curdir)

def _force_make_parent(dst):
    parent = _os.path.dirname(_os.path.abspath(dst))
    _os.makedirs(parent, exist_ok=True)

class Epub:
    def __init__(self, title=None, author=None, date=None):
        self.metadata = Metadata()
        self.pages = []
        self.title = title
        self.author = author
        self.date = date
        self.others = []
        self.__cover_page = None
        self.__images = {}
        self.__cover = None

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if value is None:
            value = ''
        self.__title = value
        self.metadata.doc_title = value
        self.metadata.add_doc_data('title', value)

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        if value is None:
            value = ''
        self.__author = value
        self.metadata.doc_author = value
        self.metadata.add_doc_data('creator', value, role='aut')

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        if value is None:
            value = _now()
        self.__date = value
        self.metadata.add_doc_data('date', value)

    def add_others(self, src, file, is_path=False, is_binary=False, encoding='utf8'):
        if is_path:
            src = _os.path.abspath(src)
        self.others.append((src, file, is_path, is_binary, encoding))

    def add_page(self, id, title, content, file=None):
        if file is None:
            file = f'{_file_escape(id)}.html'
        if isinstance(content, str):
            content = Page(file, self.metadata, content, title)
        self.pages.append((id, title, content))
        return content

    def add_cover_page(self, id, title, content, file=None):
        if file is None:
            file = f'{_file_escape(id)}.html'
        if isinstance(content, str):
            content = Page(file, self.metadata, content, title)
        self.__cover_page = (id, title, content)
        self.metadata.cover_page = file
        self.metadata.cover_page_name = title
        return content

    def add_image(self, id, src, dst):
        self.metadata.add_item(id, 'images/' + dst)
        self.__images[id] = (src, 'images/' + dst)

    def add_cover(self, src, dst):
        self.metadata.cover_image = 'images/' + dst
        self.__cover = src

    def generate(self, dir, path='out', template='template', encoding='utf8', remove=False):
        curdir = _pwd()
        srcdir = _os.path.abspath(template)
        dstdir = _os.path.abspath(path)

        if self.__cover is not None:
            cover_src = _os.path.abspath(self.__cover)
        else:
            cover_src = None
        images = []
        for template, dst in self.__images.values():
            images.append((_os.path.abspath(template), dst))

        _os.makedirs(dstdir, exist_ok=True)
        _os.chdir(dstdir)
        if _os.path.exists(dir):
            if _os.path.isfile(dir):
                _os.remove(dir)
            else:
                _shutil.rmtree(dir)
        _shutil.copytree(srcdir, _os.path.abspath(dir))
        _os.chdir(dir)
        root_dir = _pwd()

        _os.chdir('OPS')

        # Copy images
        if cover_src is not None:
            _force_make_parent(self.metadata.cover_image)
            _shutil.copyfile(cover_src, _os.path.abspath(self.metadata.cover_image))
        for template, dst in images:
            _force_make_parent(dst)
            _shutil.copyfile(template, _os.path.abspath(dst))

        if self.__cover_page is not None:
            pages = [self.__cover_page] + self.pages
        else:
            pages = self.pages

        # Generate pages
        for id_, title, page in pages:
            _force_make_parent(page.file)
            with open(page.file, 'w', encoding=encoding) as f:
                f.write(str(page))

        # Generate ncx
        ncx_file = 'fb.ncx'
        _force_make_parent(ncx_file)
        with open(ncx_file, 'w', encoding=encoding) as f:
            f.write(self.metadata.ncx(pages))

        # Generate opf
        opf_file = 'fb.opf'
        _force_make_parent(opf_file)
        with open(opf_file, 'w', encoding=encoding) as f:
            f.write(self.metadata.opf(pages))

        # Generate other files
        for _src, file, is_path, is_binary, _encoding in self.others:
            _force_make_parent(file)
            if is_path:
                _shutil.copy(_src, file)
            else:
                if is_binary:
                    f = open(file, 'wb')
                else:
                    f = open(file, 'w', encoding=encoding)
                f.write(_src)
                f.close()

        _os.chdir(root_dir)
        file_list = []
        for top, dirs, files in _os.walk(_os.curdir):
            for file in files:
                file_list.append(top + _os.sep + file)
        zip = _zipfile.ZipFile(f'{_os.path.pardir}{_os.path.sep}{dir}.epub', mode='w')
        for file in file_list:
            zip.write(file)

        if remove:
            _os.chdir(dstdir)
            _shutil.rmtree(_os.path.abspath(dir))

        _os.chdir(curdir)
