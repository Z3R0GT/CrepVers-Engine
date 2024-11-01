#1.0 --- 10/27/2024 || 27/10/2024 By: Z3R0_GT
#DOCUMENTACIÓN VERSION: 1.0
from os import listdir, path, getcwd, chdir, remove, mkdir, system
chdir(getcwd()+"/core")

#CONFIGURACIÓN DEL SISTEMA
BASE_URL = "www.creatureverse.net" #BASE DEL SITIO WEB A IMPORTAR
ROOT_GEN = getcwd()                #DIRECTORIO GENERICO
DEBUG = True                       #MODO (ignora o no archivos)
OUT_NAME_PATH = "out"              #CARPETA DE SALIDA

### CONFIGURACIONES DEL COMPILADOR
## CONFIGURACIÓN DE SINTAXIS
#CONFIGURACIÓN DE CABEZERA
WORDS_MUST     = ["KIND"]                                 #palabras obligatorias
WORDS_OPTIONAL = ["GEN", "PATH", WORDS_MUST[0], "AUTHOR"] #palabras opcionales
#CONFIGURACIÓN DE SECCIÓN
WORDS_RESERVED_GEN = ["DIALOG", "CHOICE"] #palabras reservadas genericas
WORDS_RESERVED_DIA = ["#SFW", "#NSFW"]    #palabras reservadas dentro de DIALOG

#### UTILIDADES GENERICAS
def get_file_extends(files:list[str], extension:str) -> list[str]:
    """Obtiene los archivos que cumplan con la extensión indicada 

    Args:
        files (list[str]): Archivos
        extension (str): extensiones

    Returns:
        list[str]: archivos que cumplan con la extensión
    """
    return [i for i in files if i[-len(extension):] == extension]

def get_name(info:list[str]) -> dict[str, list[str]]:
    """Obtiene la versión de diccionario con base al = de una lista con STR dada (soporta listas para valores duplicados)

    Args:
        info (list[str]): Lineas de base

    Returns:
        dict[str, list[str]]: diccionario de nombres parseados
    """
    base:dict[str, list[str]] = {}
    
    for name in info:
        name = name.split("=")
        data = name[1].split(",") if len(name[1].split(",")) > 1 else name[1]
        name = name[0].lower()
        if not base.__contains__(name):
            base[name] = data
        elif hasattr(data, "append"):
            base[name] += data if len(data) > 1 else base[name].append(data)
        else:
            base[name] = [base[name], data]
    
    return base

def get_count(base:list[str], names:list[str]) -> bool:
    """Verifica si existe o no una serie de nombre con base dada

    Args:
        base (list[str]): lista base
        names (list[str]): nombres a verificar

    Returns:
        bool: representación de existencia
    """
    a:list[bool] = []
    for i in names:
        if base.count(i) != 0:
            a.append(False)
        else:
            a.append(True)
            
    return True if a.count(False) != 0 else False

def get_key(base:dict[str], variant:str, need_pres:bool=False)->str:
    base:list = list(base.keys())
    zone = base.index(variant)
    try:
        return base[zone] if need_pres == True else base[zone+1]
    except IndexError:
        return base[zone]
    
def del_jump(lines:list[str]) -> list[str]:
    """Elimina caracter de salto de linea de la lista actual

    Args:
        lines (list[str]): base

    Returns:
        list[str]: misma base pero sin el salto de linea
    """
    c=0
    for line in lines:
        if line[-1:] == "\n":
            lines[c] = line.replace("\n", "")
        c+=1
    try:
        while True:
            del lines[lines.index("")]
    except ValueError:
        return lines

def mk_dir(root:str, name:str) -> str:
    """Crea una carpeta dentro de una ruta data ya aceptando el error FileExistsError

    Args:
        root (str): Base
        name (str): carpeta objetivo

    Returns:
        str: dirección resultante
    """
    try:
        mkdir(root+"/"+name)
    except FileExistsError:
        pass
    return root+"/"+name

def mk_str(base:list[str])->str:
    """Transforma una lista a un str 

    Args:
        base (list[str]): lista base

    Returns:
        str: misma lista pero ahora como str
    """
    a = ""
    for i in base:
        a+=i
    return a

def mk_str_under(absolute:str, variant:str, default="") -> str:
    return f"/{absolute}_{variant}" if variant.replace(" ","") != "" else f"/{absolute}" if default == "" else f"/{absolute}_{default}"

#### CUSTOM
def check_count(base:list[str], names:list[str]) -> bool:
    """Verifica si la base aún existe una secuencia

    Args:
        base (list[str]): base
        names (list[str]): nombres en secuencia

    Returns:
        bool: representación de la existencia
    """
    base = base.copy()
    names = names.copy()
    try:
        while get_count(base, names):
            for i in names:
                del base[base.index(i)]
        return True
    except ValueError:
        return False

def check_secuence(base:list[str], secuence:list[str]) -> bool:
    """Verifica si una secuencia existe dentro de la base actual

    Args:
        base (list[str]): base
        secuence (list[str]): secuencia de nombres

    Raises:
        ValueError: Lanzado cuando una secuencia no es valida
        
    Returns
        bool : representación de existencia
    """
    base = base.copy()
    normal = secuence.copy()
    invert = secuence.copy()
    invert.reverse()
    
    try:
        while get_count(base, secuence):
            if base[:len(secuence)] == normal or base[:len(secuence)] == invert:
                for i in secuence:
                    del base[base.index(i)]
            else:
                raise ValueError
        return True
    except ValueError:
        return False    

def check_all(base:list[str], secuence:list[str]):
    """Hace una verificación de la secuencia y el contador 

    Args:
        base (list[str]): base
        const (list[str]): secuencia de nombres

    Raises:
        TypeError: contador fallido
        TypeError: secuencia erronea
    """
    if not check_count(base, secuence):
        raise TypeError(f"No existe la cantidad correcta de {secuence} esperada")
    if not check_secuence(base, secuence):
        raise TypeError(f"Secuencia invalida, verificar... se debe seguir de la siguiente forma: {secuence}")

def get_text_rgn(base:str, secuence:list[str]) -> tuple[str, int, int]:
    """obtiene el rango desde/hasta con base a un rango de texto

    Args:
        base (str): base
        secuence (list[str]): secuencia de datos

    Returns:
        tuple[bool, int, int]: 0 ->  [1, 2] -> lugares donde aparecen
    """
    a = base.index(secuence[0])+1
    b = base.index(secuence[1])
    c =  base[a:b]
    return c, a, b

#### PROCCES
def compiler(file:list[str]) -> list[dict[str, list[str]]]:
    """Extrae la información de una serie de archivos bajo el formato RTC

    Args:
        file (list[str]): lista de archivos

    Raises:
        TypeError: lanzado cuando no existen dialogos
        TypeError: lanzado cuando los nombres no concuerdan o no existen
        TypeError: lanzado cuando no existe un "Kind" declarado
        TypeError: lanzado cuando los existen nombre de dialogo con el mismo nombre
        TypeError: lanzado cuando un dialogo no tiene el tabulador correcto

    Returns:
        list[dict[str, list[str]]]: información de los archivos extraidos y dividos por nombre de dialogo para la extración
    """
    info  = {}
    TAB = 4
    del_jump(file)
    
    ### PRE ESCANEO
    #1->verifica si existen la cantidad correcta de DIALOG y CHOICE
    #2->verifica si cada DIALOG tiene un CHOICE
    check_all([i.split(" ")[0] for i in file if i.split(" ")[0] in WORDS_RESERVED_GEN], WORDS_RESERVED_GEN)
    
    ### EJECUCIÓN
    dialog = [file.index(i) for i in file if i.split(" ")[0] in WORDS_RESERVED_GEN]
    if len(dialog) == 0:
        raise TypeError("No existen 'DIALOG' declarados... ¡DECLARARLOS!")
    #2->verifica que no existan nombres repetidos DENTRO DEL ARCHIVO
    for i in range(0, len(dialog), 2):
        if file[dialog[i]].split(" ")[1] != file[dialog[i+1]].split(" ")[1]:
            raise TypeError(f"Nombres diferente o equivocados, linea dialog: {dialog[i]} linea choice: {dialog[i+1]} (aproximadamente)")
        else:
            info[file[dialog[i]].split(" ")[1] ] = {"dialog":[],
                                                    "choice":[],}
    #3->Verifica que existan las palabras obligatorias
    parser = get_name(file[:dialog[0]])
    for i in WORDS_MUST:
        if not parser.__contains__(i.lower()):
            raise TypeError("TIENE QUE EXISTIR UN 'TIPO' PARA QUE ESTO FUNCIONE")  
    #El tabulador es creado EN LA PRIMERA SECCIÓN/dialogo de todo el archivo
    for i in range(dialog[0]+1, dialog[1]):
        c = 0
        for ch in file[i]:
            if ch == " ":
                c+=1
            else:
                break
            
        if file[i][:c].count(" ") >= TAB:
            TAB = file[i][:c].count(" ")
            
    ### PROCESAMIENTO
    dialog.append(dialog[-1]+(len(file)-dialog[-1]))
    for section in range(0, len(dialog)-1, 2):
        #wtf?
        line_eval:list[str] = file[dialog[section]:dialog[section+1]+(dialog[section+2]-dialog[section+1])] #LLAMEN A DIOS SI ESTO FALLA xD
        try:
            nam = line_eval[0].split(" ")[1]    
        except:
            raise TypeError("NO PUEDEN EXISTIR DOS DIALOGOS CON EL MISMO NOMBRE")
        
        if line_eval[1].replace(" ", "") != "#SFW":
            line_eval.insert(1, " "*TAB+"#SFW")
        
        s = [i.replace(" ", "") for i in line_eval if i.replace(" ", "") in WORDS_RESERVED_DIA]
        
        #ESTA SECCIÓN ANULA EL PRIMERO CHECKEO... no se que hacer para
        # solucionarlo
        if s[-1] == "#SFW":
            s.append("#NSFW")
            
        #verifica la secuencia con base a WORDS_RESERVED_DIA
        if len(s) != 1 and not (check_count(s, WORDS_RESERVED_DIA) or check_secuence(s, WORDS_RESERVED_DIA)):
            check_all(s, WORDS_RESERVED_DIA)

        # establece los dialogos por sección para su posterior procesamiento
        limit = [line_eval.index(i) for i in line_eval if i.split(" ")[0] in WORDS_RESERVED_GEN]
        limit.append(len(line_eval))
        
        for i in range(len(limit)):
            if not limit[i]+1 <= limit[-1]:
                break
            
            #GENERICO COMO MIERDA, en caso quieras programar
            # especificos, usa un match con:
            #     line_eval[limit[i]].split(" ")[0].lower()
            # y en casos los escribes MANUALMENTE.
            # el proceso de abajo es generico, metelo dentro de un
            #     case choice if choice in [NOMBRES GENERICOS]
            # suerte!
            for line in line_eval[limit[i]+1:limit[i+1]]:
                if line.count(" ") < TAB:
                    raise TypeError(F"Tabulador incorrecto detectado, tiene que ser {TAB}")
                line = line[TAB:]
                if len(line) == 0:
                    continue
                info[nam][line_eval[limit[i]].split(" ")[0].lower()].append(line)

    return [parser, info]
        
def eval_secret(line:list[str]) -> list[str]:
    """Verifica si a una linea dada entra dentro de "secrets" por palabra reservada

    Args:
        line (list[str]): linea de texto

    Returns:
        list[str]: misma linea pero con el formato esperado
    """
    for text in line:
        #se asegura que no existan secuencias de []() dentro del actual archivo (para que no se confunda)
        while text.count("[") != 0:
            text_to = get_text_rgn(text, "[]")
            label   = get_text_rgn(text, "()")
            
            #en caso ya no existan más..... "más"
            try:
                paste = f'<a href="secret/{label[0].replace("-", "/")+".html"}" class="hidden-link"> {text_to[0]} </a>'
                bef =  line[line.index(text)][:text_to[1]-1]
                aft =  line[line.index(text)][label[2]+1:len(line[line.index(text)])]
                final = bef+paste+aft
                line[line.index(text)] = final
                text = final
            except ValueError:
                break
            
    return [i+"<br>" for i in line]

def compiled(info_generic:dict[str, list[str]], 
            to_paste:dict[str, list[str]]
            ) -> dict[list[str]]:
    """Usa la información transferida desde compiler para pegar dentro de la plantilla BASE_STO

    Args:
        info_generic (dict[str, list[str]]): información meta del archivo
        to_paste (dict[str, list[str]]): infromación para pegar

    Raises:
        TypeError: lanzando cuando un CHOICE no tiene un literal DIALOG propocionado dentro del mismo archivo
        TypeError: no se cumple la secuencia []()

    Returns:
        dict[list[str]]: representación POR ARCHIVO a guardar como HTML
    """
    all_files:dict[list[str]] = {}
    for name in to_paste:
        ###################################
        # HEADER
        ###################################
        base_c = BASE_STO.copy()
        
        base_c[base_c.index("TITLE_HERE")] = f"<title> {[info_generic["path"] if not "secret" in info_generic["path"] else info_generic["path"][1]][0] if info_generic.__contains__("path") else info_generic["kind"]} </title>"
        base_c[base_c.index("NAME_AUTHOR_HERE")] = f"<i>Author(s): {mk_str([i+", " for i in info_generic["author"]])}</i>\n"    
        
        ###################################
        # BASE ZONE
        ###################################
        
        dialog = to_paste[name]["dialog"]
        
        #NOTE: esta sección puede ser un poco más dinamica para que en caso
        # del futuro sea necesirio, soporte otra clase de "etiquetas" (# + text)
        # para que la variable WORDS_RESERVED_DIA sea más logica en su función
        
        try:
            text_sfw =  eval_secret([i for i in dialog[:dialog.index("#NSFW")] if i != "#SFW"])
            text_nsfw = eval_secret([i for i in dialog[dialog.index("#NSFW"):] if i != "#NSFW"])
        except ValueError:
            text_sfw  = eval_secret([i for i in dialog if i != "#SFW"])
            text_nsfw = []

        sfw = base_c.index("SFW_TEXT_HERE")
        for i in range(len(text_sfw)):
            base_c.insert(sfw+i+1, text_sfw[i])
        del base_c[sfw]
                
        nsfw = base_c.index("NSFW_TEXT_HERE")
        for i in range(len(text_nsfw)):
            base_c.insert(nsfw+i+1, text_nsfw[i])
        del base_c[nsfw]
        
        ###################################
        # CHOICE ZONE
        ###################################
        #NOTE: esta sección puede ser extrapolada a su propia
        # función en el futuro
        tmp = []
        for i in to_paste[name]["choice"]:
            a = [l for l in i if l in ["[", "]"]]
            b = [l for l in i if l in ["(", ")"]]
            if not len(a) >= 2 or not len(b) >= 2:
                raise TypeError(f"No se encontraron las conexiones en el choice de {name}")
            if not (check_secuence(a, ["[", "]"]) or check_secuence(b, ["(", ")"])):
                raise TypeError(f"No se encuentra la secuencia []() esperada en {name}")

            text = get_text_rgn(i, "[]")[0]
            labe = get_text_rgn(i, "()")[0].replace("-", "/")
            #NOTE: aqui se pueden extender para agregar más botones/palabras
            # reservadas
            btn_c = BASE_BTN[1].copy()
            match labe:
                case "SOON":
                    btn_c = BASE_BTN[2].copy()
                case "RICK":
                    btn_c[btn_c.index("LINK_HERE")] = f'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
                case "EXIT":
                    btn_c[btn_c.index("LINK_HERE")] = f"https://{BASE_URL}/data/species.html"
                case _:
                    btn_c[btn_c.index("LINK_HERE")] = f'"{labe}.html"'
            
            btn_c[btn_c.index("TEXT_HERE")] = text
            tmp.append(mk_str(btn_c)+"\n")
        #################################
        
        base_c[base_c.index("BUTTON_HERE")] = mk_str(tmp)
        base_c[base_c.index("BACK_HERE")] = mk_str(BASE_BTN[0].copy())
        all_files[name] = base_c
        del base_c, sfw, nsfw, text_sfw, text_nsfw, dialog
        
    return all_files
        
        
#### CONFIGURACIÓN DE PLANTILLAS
BASE_GEN = del_jump(open(ROOT_GEN+"/template/base_general.rth", "rt").readlines())
BASE_STO = del_jump(open(ROOT_GEN+"/template/base_story.rth", "rt").readlines())

for i in range(BASE_GEN.count("BASE_HERE")):
    BASE_GEN[BASE_GEN.index("BASE_HERE")] = BASE_URL
for i in range(BASE_STO.count("BASE_HERE")):
    BASE_STO[BASE_STO.index("BASE_HERE")] = BASE_URL

BASE_BTN = [del_jump(open(ROOT_GEN+f"/template/btn/{i}").readlines()) for i in ["back.rth", "base.rth", "soon.rth"]]
BASE_TXT = [del_jump(open(ROOT_GEN+f"/template/text/{i}").readlines()) for i in ["base.rth"]]


#### COMPILADOR
## CONFIGURACIÓN DE COMPILADOR
chdir(ROOT_GEN+"/data")
FL_TO_COMPILE = list(filter(path.isdir, listdir()))
def init() -> dict[str]:
    """Función para empezar el programa
    Returns:
        dict[str]: representación por archivo a guardar
    """
    main:dict[dict[str]] = {}
    
    #lista todos los archivos actuales dentro de DATA
    for to_compile in FL_TO_COMPILE:
        if to_compile[0] == "_":
            to_compile = to_compile[1:]
        main[to_compile] = {}
        
        chdir(getcwd()+"/"+to_compile)
        all_files = list(filter(path.isfile, listdir()))
        if not "base.info" in all_files:
            open(getcwd()+"/base.info", "w").writelines(["VERSION=1.0", "AUTHOR=Anonymus"])
            
        info = get_name(del_jump(open(getcwd()+"/"+get_file_extends(all_files, "info")[0], "rt").readlines()))
        
        #ignora :v
        if ".ignore" in all_files and info["version"] == del_jump(open(getcwd()+"/.ignore", "rt").readlines())[0]:
            if not DEBUG:
                chdir(ROOT_GEN+"/data")
                continue
        
        #establecemos el orden 
        file_order = [i[:-4] for i in get_file_extends(all_files, "rtc")]
        for file_name in [i for i in file_order if len(i.split("-")) == 1]:
            del file_order[file_order.index(file_name)]
            file_order.insert(0, file_name+"-00")
        
        GAME_ROOT = getcwd()
        for file in file_order:
            info_file, data_file = compiler(open(GAME_ROOT+"/"+file.replace("-00", "")+".rtc", "rt").readlines())       
            ## AUTORES     
            if info_file.__contains__("author"):
                aut = [name for name in info_file["author"] if not name in info["author"]]
                aut+=info["author"]
                aut.reverse()
                info_file["author"] = aut
            else:
                info_file["author"] = [info["author"]]
            
            files_to_paste = compiled(info_file, data_file)
            
            #NOTE: apartir de este punto, se asume que ya el archivo
            # a sido compilado, ahora viene solo pegar toda la información
            chdir(mk_dir(ROOT_GEN, OUT_NAME_PATH))
            chdir(mk_dir(getcwd(), to_compile))
            chdir(mk_dir(getcwd(), file.split("-")[0]))
            
            #EN CASO TENGA GENERO
            if info_file.__contains__("gen"):
                chdir(mk_dir(getcwd(), info_file["gen"]))
            chdir(mk_dir(getcwd(), info_file["kind"]))
            #En caso exista un path
            if info_file.__contains__("path"):
                if type(info_file["path"]) == type(""):
                    info_file["path"] = [info_file["path"]]
                if info_file["path"][0] == "secret":
                    chdir(mk_dir(getcwd(), "secret"))
                    del info_file["path"][0]
                    
                for name in info_file["path"]:
                    chdir(mk_dir(getcwd(), name))
            #crea el nombre el archivo
            main[to_compile][name if info_file.__contains__("path") else info_file["kind"]] = list(files_to_paste.keys())[0]
            
            for mn in files_to_paste:
                open(getcwd()+"/"+mn+".html", "w").writelines(files_to_paste[mn])
            
            chdir(GAME_ROOT)
            
        open(getcwd()+"/.ignore", "w").write(info["version"])
        
        chdir(ROOT_GEN+"/data")
    return main

#MAINLY_ARCH:dict[str] = init()
#LINKER
#

from random import randint
BAN = ["child", "adult", "young"]
BAM = ["mainBase", "pather", "uw"]
MAIN:dict[dict[str]] = {}

for i in FL_TO_COMPILE:
    if i[0] == "_":
        i = i[1:]
    MAIN[i] = {}
    for im in BAN:
        MAIN[i][im] = BAM[randint(0, len(BAM)-1)]
        

def parser_file(files:list[str],
                title:str,
                desc:str,
                variant_file:str|list[str], 
                variant:str="",
                variant_main:dict[str]=...,
                variant_base:dict[str]=...):
    base_c = BASE_GEN.copy()
    base_msg = BASE_TXT[0].copy()
    base_c[base_c.index("TITLE_HERE")] = f"<title>{title}?</title>"
    
    base_msg[base_msg.index("TEXT_HERE")] = desc
    base_c[base_c.index("TEXT_HERE")]  = mk_str(base_msg)
    
    info_connt = []
    info_text  = []
    name = mk_str_under(title, variant)+".html"
    buttons_tmp = []
    c=0
    for buttons in files:
        if not buttons[0] == "_":
            btn_c = BASE_BTN[1].copy()
            if buttons[:3] == "def":
                txt = "default"
                nam = buttons[3:]
            else:
                txt = f"{variant_file if type(variant_file) != type([]) else variant_file[c]} {buttons}"            
                nam = buttons
            btn_c[btn_c.index("TEXT_HERE")] = txt

            if variant_main != ... and nam in variant_main:
                lnk = f'"{nam}/{variant_main[nam]}'
                
            elif type(variant_file) == type([]):
                sel = variant_file[c]
                lnk = f'"{buttons}{mk_str_under(buttons, get_key(variant_base, sel) if variant_base != ... else sel, "choice")}'
                c+=1
            
            else:
                lnk = f'"{buttons}{mk_str_under(buttons, get_key(variant_base, variant_file) if variant_base != ... else variant_file, "choice")}'

            lnk +='.html"'
            info_connt.append(lnk)
            btn_c[btn_c.index("LINK_HERE")] = lnk
        else:
            btn_c = BASE_BTN[2].copy()
            txt = buttons[1:]
            btn_c[btn_c.index("TEXT_HERE")] = txt
        
        info_text.append(txt)

        buttons_tmp.append(mk_str(btn_c)+"\n")

    base_c[base_c.index("BUTTON_HERE")] = mk_str(buttons_tmp)
    base_c[base_c.index("BACK_HERE")]   = mk_str(BASE_BTN[0].copy())
    
    
    #print("END FILE = ", name)
    #print("DESC FILE = ", desc)
    #print("CONNECTIONS = ", info_connt)
    #print("TEXT = ", info_text)
    
    try:
        remove(getcwd()+name)
        pass
    except FileNotFoundError:
        pass
    #print("PATH TO SAVE= ",getcwd()+name)
    open(getcwd()+"/"+name, "w").writelines(base_c)
    
def ch_start(level:dict[str], absolute:str, opt:dict[str], num:int, press:bool=False, original:dict[str, dict[str]]=...) -> int:
    try:
        variant = list(level.keys())[num]
    except IndexError:
        return
    
    if press and absolute in list(filter(path.isdir, listdir())):
        base_buttons = [i for i in original if type(original[i]) == type({})]
        base_variant = [list(original[i].keys())[0] for i in base_buttons]
        bs = getcwd().split("\\")[-1]
        
        base_buttons.append("def"+bs)
        parser_file(base_buttons, "Path choice", "chooce a path", base_variant, variant_main=opt)
        opt[bs] = "Path choice"
        t = getcwd()
        
        chdir("..")
        key = [i.replace(".html", "") for i in list(filter(path.isfile, listdir())) if i.split("_")[0] == getcwd().split("\\")[-1]][0]
        var = key.split("_")[1]
        parser_file(list(filter(path.isdir, listdir())), key, original[var], var, variant_main=opt)
        
        chdir(t)
        
    chdir(getcwd()+"/"+absolute) 
    tlt = list(filter(path.isdir, listdir()))
    
    
    for i in range(len(tlt)):
        starter(absolute+"_"+variant, level[variant], variant, opt, level)
        ch_start(level, tlt[i], opt, num+1)
    
    chdir("..")
    return
    
def starter(key:str, desc:dict[str]|str, var:str, main:dict[str], ot):
    if type(desc) == type({}):
        ch_start(desc, key.split("_")[1], main, 0, True, ot)
    elif type(desc) == type(""):
        file = list(filter(path.isdir, listdir()))
        parser_file(file, key, desc, var, variant_main=main, variant_base=ot)

chdir(ROOT_GEN+"/out")
from json import load
parser_file(FL_TO_COMPILE, "specie", "chooce", "choice", )
for specie in FL_TO_COMPILE:
    base_info = load(open(ROOT_GEN+"/data/"+specie+"/desc.json", "r"))
    ch_start(base_info, specie, MAIN[specie], 0)
    break

print(getcwd())