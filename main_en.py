#1.0 --- 10/27/2024 || 27/10/2024 By: Z3R0_GT
#DOCUMENTATION VERSION (in fron of spanish): 1.0
from os import listdir, path, getcwd, chdir, remove, mkdir
chdir(getcwd()+"/core")

#SYSTEM CONFIGURATION
BASE_URL = "www.creatureverse.net" #BASE OF THE WEBSITE TO IMPORT
ROOT_GEN = getcwd()                #GENERIC DIRECTORY
DEBUG = True                       #MODE (ignore or not ignore files)
OUT_NAME_PATH = "out"              #OUT FOLDER (literal)

### COMPILER SETTINGS
## SYNTAX SETTINGS
#HEADER CONFIGURATION
WORDS_MUST     = ["KIND"]                                 #mandatory words
WORDS_OPTIONAL = ["GEN", "PATH", WORDS_MUST[0], "AUTHOR"] #optional words
#SECTION SETUP
WORDS_RESERVED_GEN = ["DIALOG", "CHOICE"] #generic reserved words
WORDS_RESERVED_DIA = ["#SFW", "#NSFW"]    #reserved words within DIALOG

#### GENERIC UTILITIES
def get_file_extends(files:list[str], extension:str) -> list[str]:
    """Gets the files that meet the indicated extension

    Args:
        files (list[str]): files
        extension (str): extends

    Returns:
        list[str]: files that meet the extension
    """
    return [i for i in files if i[-len(extension):] == extension]

def get_name(info:list[str]) -> dict[str, list[str]]:
    """Gets the dictionary version based on = of a list with given STR (supports lists for duplicate values)
    Args:
        info (list[str]): base line

    Returns:
        dict[str, list[str]]: dictionary of parsed names
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
    """Checks whether a name series with a given base exists or not

    Args:
        base (list[str]): base list
        names (list[str]): names to verify

    Returns:
        bool: representation of existence
    """
    a:list[bool] = []
    for i in names:
        if base.count(i) != 0:
            a.append(False)
        else:
            a.append(True)
            
    return True if a.count(False) != 0 else False
    
def del_jump(lines:list[str]) -> list[str]:
    """Removes newline character from the current list

    Args:
        lines (list[str]): base

    Returns:
        list[str]: Same base but without the line break
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
    """Create a folder inside a data path and accept the FileExistsError error
    Args:
        root (str): Base
        name (str): objective folder

    Returns:
        str: resulting address
    """
    try:
        mkdir(root+"/"+name)
    except FileExistsError:
        pass
    return root+"/"+name

def mk_str(base:list[str])->str:
    """Transforms a list to a str
    Args:
        base (list[str]): base list

    Returns:
        str: same list but now as str
    """
    a = ""
    for i in base:
        a+=i
    return a

#### CUSTOM
def check_count(base:list[str], names:list[str]) -> bool:
    """Check if the base sequence still exists
    Args:
        base (list[str]): base
        names (list[str]): names in sequence
    Returns:
        bool: representation of existence
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
    """Checks if a sequence exists within the current database
    Args:
        base (list[str]): base
        secuence (list[str]): ssequence of names
    Raises:
        ValueError: Thrown when a sequence is invalid
    Returns
        bool : representation of existence
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
    """Performs a check of the sequence and the counter
    Args:
        base (list[str]): base
        secuence (list[str]): sequence of names
    Raises:
        TypeError: counter failed
        TypeError: bad sequence
    """
    if not check_count(base, secuence):
        raise TypeError(f"There is not the correct amount of {secuence} expected")
    if not check_secuence(base, secuence):
        raise TypeError(f"Invalid sequence, check... must be followed as follows: {secuence}")

def get_text_rgn(base:str, secuence:list[str]) -> tuple[str, int, int]:
    """Gets the range from/to based on a text range
    Args:
        base (str): base
        secuence (list[str]): data stream
    Returns:
        tuple[bool, int, int]: 0 ->  [1, 2] -> places where they appear
    """
    a = base.index(secuence[0])+1
    b = base.index(secuence[1])
    c =  base[a:b]
    return c, a, b

#### PROCCES
def compiler(file:list[str]) -> list[dict[str, list[str]]]:
    """Extracts information from a series of files in the RTC format
    Args:
        file (list[str]): file list

    Raises:
        TypeError: thrown when there are no dialogs
        TypeError: thrown when names do not match or do not exist
        TypeError: thrown when there is no declared "Kind"
        TypeError: thrown when there are dialog names with the same name
        TypeError: thrown when a dialog does not have the correct tab
    Returns:
        list[dict[str, list[str]]]: information of the extracted files and divided by dialog name for extraction
    """
    info  = {}
    TAB = 4
    del_jump(file)
    
    ### PRE SCAN
    #1->Check if there are the correct amount of DIALOG and CHOICE
    #2->Check if each DIALOG has a CHOICE
    check_all([i.split(" ")[0] for i in file if i.split(" ")[0] in WORDS_RESERVED_GEN], WORDS_RESERVED_GEN)
    
    ### EXECUTION
    dialog = [file.index(i) for i in file if i.split(" ")[0] in WORDS_RESERVED_GEN]
    if len(dialog) == 0:
        raise TypeError("There are no declared 'DIALOG's... DECLARE THEM!")
    #2->Check that there are no duplicate names WITHIN THE FILE
    for i in range(0, len(dialog), 2):
        if file[dialog[i]].split(" ")[1] != file[dialog[i+1]].split(" ")[1]:
            raise TypeError(f"Nombres diferente o equivocados, linea dialog: {dialog[i]} linea choice: {dialog[i+1]} (aproximadamente)")
        else:
            info[file[dialog[i]].split(" ")[1] ] = {"dialog":[],
                                                     "choice":[],}
    #3->Check that the required words exist
    parser = get_name(file[:dialog[0]])
    for i in WORDS_MUST:
        if not parser.__contains__(i.lower()):
            raise TypeError("THERE HAS TO BE A 'KIND' FOR THIS TO WORK")  
    #The tab is created IN THE FIRST SECTION/dialog of the entire file
    for i in range(dialog[0]+1, dialog[1]):
        c = 0
        for ch in file[i]:
            if ch == " ":
                c+=1
            else:
                break
            
        if file[i][:c].count(" ") >= TAB:
            TAB = file[i][:c].count(" ")
            
    ### PROSECUTION
    dialog.append(dialog[-1]+(len(file)-dialog[-1]))
    for section in range(0, len(dialog)-1, 2):
        #wtf?
        line_eval:list[str] = file[dialog[section]:dialog[section+1]+(dialog[section+2]-dialog[section+1])] #LLAMEN A DIOS SI ESTO FALLA xD
        try:
            nam = line_eval[0].split(" ")[1]    
        except:
            raise TypeError("THERE CANNOT BE TWO DIALOGUES WITH THE SAME NAME")
        
        if line_eval[1].replace(" ", "") != "#SFW":
            line_eval.insert(1, " "*TAB+"#SFW")
        
        s = [i.replace(" ", "") for i in line_eval if i.replace(" ", "") in WORDS_RESERVED_DIA]
        
        #THIS SECTION CANCELS THE FIRST CHECK... I don't know what to do to fix it
        if s[-1] == "#SFW":
            s.append("#NSFW")
            
        #Check the sequence based on WORDS_RESERVED_DIA
        if len(s) != 1 and not (check_count(s, WORDS_RESERVED_DIA) or check_secuence(s, WORDS_RESERVED_DIA)):
            check_all(s, WORDS_RESERVED_DIA)

        # Sets the dialogs by section for further processing
        limit = [line_eval.index(i) for i in line_eval if i.split(" ")[0] in WORDS_RESERVED_GEN]
        limit.append(len(line_eval))
        
        for i in range(len(limit)):
            if not limit[i]+1 <= limit[-1]:
                break
            
        #GENERIC AS CRAP, in case you want to program
        # specific ones, use a match with:
        # line_eval[limit[i]].split(" ")[0].lower()
        # and in cases you write them MANUALLY.
        # the process below is generic, put it inside a
        # case choice if choice in [GENERIC NAMES]
        # good luck!
            for line in line_eval[limit[i]+1:limit[i+1]]:
                if line.count(" ") < TAB:
                    raise TypeError(F"Bad tab detected, should be {TAB}")
                line = line[TAB:]
                if len(line) == 0:
                    continue
                info[nam][line_eval[limit[i]].split(" ")[0].lower()].append(line)

    return [parser, info]
        
def eval_secret(line:list[str]) -> list[str]:
    """Check if a given line falls within "secrets" for reserved word
    Args:
        line (list[str]): line of text
    Returns:
        list[str]: Same line but with the expected format
    """
    for text in line:
        #makes sure that there are no sequences of []() inside the current file (so that it doesn't get confused)
        while text.count("[") != 0:
            text_to = get_text_rgn(text, "[]")
            label   = get_text_rgn(text, "()")
            
            #in case there are no more..... "more"
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
    """Use the information passed from compiler to paste into the BASE_STO template
    Args:
        info_generic (dict[str, list[str]]): meta file information
        to_paste (dict[str, list[str]]): information to paste

    Raises:
        TypeError: Throwing when a CHOICE does not have a DIALOG literal provided within the same file
        TypeError: []() sequence not met

    Returns:
        dict[list[str]]: representation BY FILE to save as HTML
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
        
        #NOTE: this section can be a little more dynamic so that if necessary
        # in the future, it supports another kind of "tags" (# + text)
        # so that the variable WORDS_RESERVED_DIA is more logical in its function
        
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
        #NOTE: This section may be extrapolated to your own
        # function in the future
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
            #NOTE: here you can extend to add more buttons/words
            # reserved
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
        
        
#### TEMPLATE SETUP
BASE_GEN = del_jump(open(ROOT_GEN+"/template/base_general.rth", "rt").readlines())
BASE_STO = del_jump(open(ROOT_GEN+"/template/base_story.rth", "rt").readlines())

for i in range(BASE_GEN.count("BASE_HERE")):
    BASE_GEN[BASE_GEN.index("BASE_HERE")] = BASE_URL
for i in range(BASE_STO.count("BASE_HERE")):
    BASE_STO[BASE_STO.index("BASE_HERE")] = BASE_URL

BASE_BTN = [del_jump(open(ROOT_GEN+f"/template/btn/{i}").readlines()) for i in ["back.rth", "base.rth", "soon.rth"]]
BASE_TXT = [del_jump(open(ROOT_GEN+f"/template/text/{i}").readlines()) for i in ["base.rth"]]


#### COMPILER
## COMPILER CONFIGURATION
chdir(ROOT_GEN+"/data")

def init() -> dict[str]:
    """Function to start the program
    Returns:
        dict[str]: representation per file to save
    """
    main:dict[str] = {}
    
    #list all current files within DATA
    for to_compile in list(filter(path.isdir, listdir())):
        chdir(getcwd()+"/"+to_compile)
        all_files = list(filter(path.isfile, listdir()))
        
        info = get_name(del_jump(open(getcwd()+"/"+get_file_extends(all_files, "info")[0], "rt").readlines()))
        #ignora :v
        if ".ignore" in all_files and info["version"] == del_jump(open(getcwd()+"/.ignore", "rt").readlines())[0]:
            if not DEBUG:
                chdir(ROOT_GEN+"/data")
                continue
        
        #We establish the order
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
            
            #NOTE: from this point on, it is assumed that the file has already been
            # compiled, now just paste all the information
            chdir(mk_dir(ROOT_GEN, OUT_NAME_PATH))

            chdir(mk_dir(getcwd(), to_compile))
            chdir(mk_dir(getcwd(), file.split("-")[0]))
            
            #IN CASE YOU HAVE GENDER
            if info_file.__contains__("gen"):
                chdir(mk_dir(getcwd(), info_file["gen"]))
            chdir(mk_dir(getcwd(), info_file["kind"]))
            #In case there is a path
            if info_file.__contains__("path"):
                if type(info_file["path"]) == type(""):
                    info_file["path"] = [info_file["path"]]
                if info_file["path"][0] == "secret":
                    chdir(mk_dir(getcwd(), "secret"))
                    del info_file["path"][0]
                    
                for name in info_file["path"]:
                    chdir(mk_dir(getcwd(), name))
            # (ok, those before are SUPER GENERIC... XD)
            #create the name of the file
            main[name if info_file.__contains__("path") else info_file["kind"]] = list(files_to_paste.keys())[0]
            
            for mn in files_to_paste:
                open(getcwd()+"/"+mn+".html", "w").writelines(files_to_paste[mn])
            
            chdir(GAME_ROOT)
            
        open(getcwd()+"/.ignore", "w").write(info["version"])
        
        chdir(ROOT_GEN+"/data")
    return main

MAINLY_ARCH:dict[str] = init()
#LINKER
chdir(ROOT_GEN+"/"+OUT_NAME_PATH)
def pather(files:list[str], 
            title:str,
            msg:str,
            abosolute:str,
            variant:str="choice",
            info:dict[str]=...):
    """create file... in theory

    Args:
        files (list[str]): list of files
        title (str): central text
        msg (str): message
        abosolute (str): absolute name
        variant (str, optional): name that appears after _ . Defaults to "choice".
        info (dict[str], optional): what is it for?. Defaults to ....
    """
    base_c = BASE_GEN.copy()
    base_c[base_c.index("TITLE_HERE")] = f"<title>{title} {variant}?</title>"
    base_msg = BASE_TXT[0].copy()
    base_msg[base_msg.index("TEXT_HERE")] = msg
    base_c[base_c.index("TEXT_HERE")]  = mk_str(base_msg)
        
        
    tmp = []
    for name in files:
        if name[0] == "_":
            btn_c = BASE_BTN[2].copy()
            btn_c[btn_c.index("TEXT_HERE")] = name[1:]
        else:
            btn_c = BASE_BTN[1].copy()
            btn_c[btn_c.index("TEXT_HERE")] = f"{variant} {name}"
            if name in MAINLY_ARCH:
                lnk = f'"{name}/{MAINLY_ARCH[name]}'
            else:
                lnk = f'"{name}/{name}_{variant}'
                        
            lnk+='.html"'
            btn_c[btn_c.index("LINK_HERE")] = lnk
        tmp.append(mk_str(btn_c)+"\n")
        
    base_c[base_c.index("BUTTON_HERE")] = mk_str(tmp)
    base_c[base_c.index("BACK_HERE")] = mk_str(BASE_BTN[0].copy())
    if not info == ...:
        try:
            n = list(info.keys()).index(variant)-1
            if n < 0:
                n = 0
            v = list(info.keys())[n]
        except IndexError:
            v = variant
    else:
        v = variant
        
    try:
        remove(getcwd()+f"/{abosolute}_{v}.html")
    except FileNotFoundError:
        pass
        
    open(getcwd()+f"/{abosolute}_{v}.html", "w").writelines(base_c)

def create_path(key, info:dict[str, dict[str]], 
                name_absolute:str, file_name:str):
    """does it create directories? maybe... it's recursive and complex

    Args:
        key (_type_): name of the menu
        info (dict[str, dict[str]]): general list of names for the menu
        name_absolute (str): absolute name (species)
        file_name (str): name of file to create
    """
    if type(info[key]) == type(""):
        pather(list(filter(path.isdir, listdir())), name_absolute, info[key], file_name, key, info)
    elif type(info[key]) == type({}):
        chdir("..")
        c = getcwd()
        chdir(c+"/"+key)
        create_path(list(info[key].keys())[0], info[key], name_absolute, key)
        chdir(c+"/"+file_name)
        return

    try:
        nxt_key = list(info.keys())[list(info.keys()).index(key)+1]
        if type(info[nxt_key]) == type({}):
            files = [nxt_key]
        else:
            files = list(filter(path.isdir, listdir()))
                
        for i in files:
            if i in list(filter(path.isdir, listdir())):
                chdir(getcwd()+"/"+i)
                create_path(nxt_key, info, name_absolute, i)
                chdir("..")
    except IndexError:
        chdir("..")
        return 
                

def saver():
    """Function to generate the species and choice menus (described in desc.json)
    """
    from json import load
    info:dict[str, dict[str]] = load(open(ROOT_GEN+"/data/desc.json", "r"))

    #esto es opcional
    pather([i for i in list(filter(path.isdir, listdir())) if i in info], list(info.keys())[0], info[list(info.keys())[0]], list(info.keys())[0])
    del info[list(info.keys())[0]]

    for names in info:
        chdir(getcwd()+"/"+names)
        create_path(list(info[names].keys())[0] ,info[names], names, names)
        chdir("..")
        
saver()
        
print(getcwd())