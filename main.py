from os import getcwd, mkdir, path, remove, mkdir, listdir, chdir, system, rename
from shutil import rmtree
from argparse import ArgumentParser

from typing_extensions import Literal, Any
from functools import singledispatch

__version__ = "1.0.3.0"
"""Version del actualizador"""
__features__ = "all"
"""es comico tener eso XD"""
__can_edit__ = False
"""Usado para controlar si el programa puede manipular archivo (solo usado para pruebas)"""
__autors__ = ("Z3R0_GT", "OFFZ3R0")
"""Autores que han intervenido en el programa hasta ahora"""
__company__ = "None"
"""¿por que no tener uno de igual forma? XD"""
__contac_info__ = (
    "MAIL:contac.es.z3r0.gt@gmail.com",
    "GITHUB:https://github.com/Z3R0GT",
)
__lang__ = "Spanish"

# ZONE -> BEHAVIOR
########################
# CONSTANTS -> PROGRAM
########################
DEFAULT_BASE_URL = "www.creatureverse.net"

DEFAULT_OUT_PATH: str
DEFAULT_INP_PATH: str

DEFAULT_EXTEND_SUPPORT = ("rtc", "rth", "ignore", "html")
"""Formatos que usa el programa"""

DEFAULT_TAB: int
"""Tabs usados para indicar los tabs de TODOS los archivos de renpy"""

DEFAULT_BASE_NAMES = ("base", "desc")  # usado por el programa
"""Nombres de archivos de configuración usados por el programa (son de alta prioridad en ejecución)"""

DEFAULT_FILES_OWN = [f"{i}.{DEFAULT_EXTEND_SUPPORT[0]}" for i in DEFAULT_BASE_NAMES]
"""Nombres de archivos con extensión"""

DEFAULT_BASE = {"author": "Anonymus", "version": "1.0"}
"""Información por defecto a usar del programa"""

DEFAULT_LANG_KEYWORDS_MUST = (
    "KIND",  # Configura el tipo de archivo a tratar
    "DIALOG",  # Configura el inicio de un archivo HTML
    "CHOICE",  # Configura los botones de un arhivo HTML
)
"""Palabras reservadas que si o si tienen que ir en el los archivos RTC"""
DEFAULT_LANG_KEYWORDS_PROSS = (
    "a",  # No tiene proceso concreto
    "s",  # Secuencia (solo dos)
)
DEFAULT_LANG_KEYWORDS_OPT = (
    "GEN",  # Configura una sub carpeta del actual archivo
    "PATH",  # Configura una sub carpeta del actual archivo
    "MODE-s",  # Especifica el modo, tiene que ser en secuencia
    "AUTHOR",  # Configura los autores del actual archivo
    "VERSION",  # Configura la version del actual archivo
)
"""Palabras opcionales que pueden ir dentro de los archivos RTC"""

########################
# SKIP -> PROGRAM
########################
# NOTE: pueden ser cambiados desde consola
SKIP_SYMBOLS: list[str] = ["_"]
"""Determina los simbolos al inicio de todo archivo a ser omitidos"""
SKIP_GEN_NAMES: list[str] = []
"""Nombres genericos para ser omitidos"""
SKIP_FILE_NAME: list[str] = []
"""Nombres de archivos para ser omitidos"""
SKIP_FOL_NAMES: list[str] = []
"""Nomrbe de carpetas para ser omitidos"""
SKIP_PKG_NAMES: list[str] = []
"""Nomrbe de paquetes para ser omitidos"""

# CONSTANTS -> PROCCESING
# NOTE: los siguientes archivos podran ser skipeados o borrados según la necesidad del momento
RESERVED_GENERIC_FILE_NAMES = ("base", "desc")
"""Nombres de archivos usados por el programa"""
RESERVED_GENERIC_FOLD_NAMES = ("template", "data", "core")
"""Nombres de carpetas usadas por el programa"""
RESERVED_PKG_END = "end"
"""Usado por el programa para determinar el final de cada instrucción"""

########################
# INDICATORS -> BEHAVIOR
########################
# NOTE: muchas de estas variables son usadas para modificar el comportamiento y
# procesamiento de imagenes/archivos, por lo que son MUY delicadas
IS_SCAN_DISABLE: bool
IS_FILE_DISABLE: bool

def run():
    parser = ArgumentParser(
        description="This tool was designed specificly to compile RTC file intro HTML using templates"
        ", this was design by OFFZ3R0/Z3R0_GT for CreatureVerse"
    )

    # NOTE: comportamiento del programa
    parser.add_argument(
        "-exept", "-e", nargs="+", help="Add skip packages", default=[], metavar="NAMES"
    )

    parser.add_argument(
        "-add-skip",
        "-add-sk",
        nargs="+",
        help="Skip the specific name",
        default=[],
        metavar="NAMES",
    )

    parser.add_argument(
        "-add-skip-folder",
        "-add-sk-f",
        nargs="+",
        help="Skip specific those folder's name",
        default=[],
        metavar="FOLDER'S NAMES",
    )

    parser.add_argument(
        "-add-skip-file",
        "-add-sk-fi",
        nargs="+",
        help="Skip specific those file's name",
        default=[],
        metavar="FILE'S NAMES",
    )

    parser.add_argument(
        "--input",
        "-in",
        default=getcwd() + "/core/data",
        help="configure the data directory of the files to compile",
        metavar="PATH",
    )

    parser.add_argument(
        "--output",
        "-out",
        default=getcwd() + "/core/out",
        help="configure the output directory to save the compile files",
        metavar="PATH",
    )

    parser.add_argument(
        "--set-tab",
        "-s-tab",
        default=4,
        help="configure the default tab spaces",
        metavar="INT",
    )

    parser.add_argument(
        "--disable-scan-rtc",
        "-dis-rtc",
        action="store_false",
        help="configure if the compiles will 'compile' the rtc files",
        default=True,
    )

    parser.add_argument(
        "--disable-scan-out",
        "-dis-scan",
        action="store_false",
        help="configure if the compiles will 'scane' the output folder",
        default=True,
    )

    # NOTE: Información y meta
    parser.add_argument(
        "-v", "--version", action="version", version=f"CrepVerse version {__version__}"
    )

    parser.add_argument(
        "-a",
        "--authors",
        action="version",
        version=f"Currently, under develop by {mkstr(__autors__, ", ")}",
        help="show the currently author/developers of this tool and exit",
    )

    parser.add_argument(
        "-c",
        "--company",
        action="version",
        version=f"Developed for {__company__}",
        help="shows the current company for which this tool was developed and exit",
    )

    parser.add_argument(
        "-i",
        "-info",
        action="version",
        version=f"Contact info (developer/s): \n {mkstr(__contac_info__, ".\n")}",
        help="show info to contact the developer(s) and exit",
    )

    parser.add_argument(
        "--lang",
        "-l",
        choices=["spanish", "english"],
        default="spanish",
        help="configure the current language in case the program gets a error",
    )

    args = parser.parse_args()

    def assign_args(base: list[str], form: list[str]):
        if len(base) != 0:
            for names in form:
                if len(names) == 1:
                    SKIP_SYMBOLS.append(names)
                else:
                    form.append(names)

    global DEFAULT_TAB, SKIP_FILE_NAME, SKIP_FOL_NAMES, SKIP_GEN_NAMES, SKIP_PKG_NAMES, SKIP_SYMBOLS, IS_FILE_DISABLE, IS_SCAN_DISABLE, DEFAULT_OUT_PATH, DEFAULT_INP_PATH

    IS_FILE_DISABLE = args.disable_scan_rtc
    IS_SCAN_DISABLE = args.disable_scan_out
    DEFAULT_TAB = int(args.set_tab)

    DEFAULT_OUT_PATH = args.output
    DEFAULT_INP_PATH = args.input

    assign_args(args.add_skip, SKIP_FILE_NAME)
    assign_args(args.add_skip_folder, SKIP_FOL_NAMES)
    assign_args(args.add_skip_file, SKIP_FILE_NAME)



if __name__ == "__main__":
    run()
