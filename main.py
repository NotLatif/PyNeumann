# TODO
# try casting and not casting int() when using arithmetics
# aggiorna il file README
# aggiungi impostazioni personalizzabili come istruzioni
# eg.
#   lnstrt x <- lineStart = x
#

import config as cfg
import glob, os

#colors
class col:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

#n of instructions counter
def incIst():
    global nIstruzioni
    nIstruzioni += 1

#i/o instructions
def read():
    incIst()
    global accumulatore
    inp = input(f'{col.CYAN}input > ')
    try:
        accumulatore = int(inp)
    except:
        accumulatore = inp
    print(col.ENDC, end = '')

def write():
    incIst()
    nastroScr = accumulatore
    print(f'{col.GREEN}output > {nastroScr}')
    print(col.ENDC, end = '')

def load(x):
    incIst()
    global accumulatore
    global memoria
    accumulatore = memoria[x]

def store(x):
    incIst()
    global accumulatore
    global memoria
    memoria[x] = accumulatore

#arithmetic instructions
def add(x):
    incIst()
    global accumulatore
    accumulatore += memoria[x]

def sub(x):
    incIst()
    global accumulatore
    accumulatore -= memoria[x]

def mult(x):
    incIst()
    global accumulatore
    accumulatore *= memoria[x]

def div(x):
    incIst()
    global accumulatore
    accumulatore //= memoria[x]

def loadEq(x):
    incIst()
    global accumulatore
    accumulatore = x

def addEq(x):
    incIst()
    global accumulatore
    accumulatore += x

def subEq(x):
    incIst()
    global accumulatore
    accumulatore -= x

def multEq(x):
    incIst()
    global accumulatore
    accumulatore *= x

def divEq(x):
    incIst()
    global accumulatore
    accumulatore //= x

#logic instructions
def br(x): #BRanch (unconditioned)
    incIst()
    global linea
    linea = int(x)

def beq(x): #BranchEQual (if [ACC] == 0)
    incIst()
    global linea
    if (accumulatore == 0):
        linea = x

def bge(x): #BranchGreaterEqual (if [ACC] >= 0)
    incIst()
    global linea
    if (accumulatore >= 0):
        linea = x

def bg(x): #BranchGreater (if [ACC] > 0)
    incIst()
    global linea
    if (accumulatore > 0):
        linea = x

def ble(x): #BranchLowerEqual (if [ACC] <= 0)
    incIst()
    global linea
    if (accumulatore <= 0):
        linea = x

def bl(x): #BranchLower (if [ACC] < 0)
    incIst()
    global linea
    if (accumulatore < 0):
        linea = x

def loadAt(x): #Load [x]
    incIst()
    pos = memoria[x]
    load(x)

def storeAt(x): #Store [x]
    incIst()
    pos = memoria[x]
    store(x)


#Script Start
if(__name__=='__main__'):

    files = []
    if(cfg.fileName == ''): #if fileName is blank: look for *.code and ask which to open
        os.chdir("./")
        x = 0
        for file in glob.glob("*.code"):
            files.append(file)
            print(f"[{x}]{file}")
            x+=1

        print("Quale file vuoi aprire?")
        cfg.fileName = files[int(input("[int] > "))]
    
    #init vars
    nastroScr = 0
    accumulatore = 0
    memoria = {}
    linea = 0
    
    #system vars
    nIstruzioni = 0
    rawCode = []
    code = {}
    #open and read code
    with open(cfg.fileName) as f:
        rawCode = f.readlines()

    #separate code from arguments, and remove comments
    i = 0
    for word in rawCode:
        word = word.split(cfg.commentChar, 1)[0] #remove comments
        x = word.split() #split string for management

        #store commands in dict {row:[cmd, arg]}
        if(x != []): #if row is not comment
            try: #has args
                code[i] = [x[0].upper(), x[1]] #[cmd, arg]
            except IndexError: #has no args
                code[i] = [x[0].upper()] #[cmd]

        i+=1
    
    if(code[len(code)-1] != 'END'): #if end instruction is missing add one at the end
        code[len(code)] = ['END']

    #execute
    while True: #for word in code
        istr = linea
        linea += 1

        cmd = code[istr][0] #command x
        try:
            arg = code[istr][1] #arg x
            arg = int(arg)
        except IndexError:
            arg = None

        #debug
        if(cfg.show_debug):
            print(f'  [DEBUG]---------{col.BOLD}row:{istr}{col.ENDC}-------[{istr+cfg.startLine}]')
            print(f'  [ACC]: {accumulatore}')
            print(f'  [MEM]: {memoria}')
            print(f'  cmd:{col.WARNING} {cmd}{col.ENDC}; arg:{col.WARNING} {arg}{col.ENDC}')

        #instructions
        try:
            if(cmd == 'READ'):#i/o
                read()
            elif(cmd == 'WRITE'):
                write()
            elif(cmd == 'LOAD'):#memory
                load(arg)
            elif(cmd == 'STORE'): 
                store(arg)
            elif(cmd == 'LOAD@'):
                loadAt(arg-cfg.startLine)
            elif(cmd == 'STORE@'):
                storeAt(arg-cfg.startLine)
            elif(cmd == 'ADD'):#arithmetic
                add(arg)
            elif(cmd == 'SUB'):
                sub(arg)
            elif(cmd == 'MULT'):
                mult(arg)
            elif(cmd == 'DIV'):
                div(arg)
            elif(cmd == 'LOAD='):
                loadEq(arg)
            elif(cmd == 'ADD='):
                addEq(arg)
            elif(cmd == 'SUB='):
                subEq(arg)
            elif(cmd == 'MULT='):
                multEq(arg)
            elif(cmd == 'DIV='):
                divEq(arg)
            elif(cmd == 'BR'):#logic
                br(arg-cfg.startLine)
            elif(cmd == 'BEQ'):
                beq(arg-cfg.startLine)
            elif(cmd == 'BGE'):
                bge(arg-cfg.startLine)
            elif(cmd == 'BG'):
                bg(arg-cfg.startLine)
            elif(cmd == 'BLE'):
                ble(arg-cfg.startLine)
            elif(cmd == 'BL'):
                bl(arg-cfg.startLine)
            elif(cmd == 'LNSTRT'):#misc
                cfg.startLine = arg
            elif(cmd == 'END'):
                break
            else:
                print(f'{col.FAIL}ERROR, command not found')
                print(f'  ->"{cmd}"')
                print(f'{col.BOLD}  row:{istr}{col.ENDC}')
        except KeyError: #Could be triggered by: LOAD STORE LOAD@ STORE@
            print(f'{col.FAIL}ERROR, address in memory does not exit')
            print(f'    AT ROW: row:{istr} (line: {istr+cfg.startLine})')
            print(f'    [MEM]: {memoria}')
            print(f'    cmd -> cmd:{col.WARNING} {cmd}{col.FAIL}; arg:{col.WARNING} {arg}{col.ENDC}')
    
#print output
print(' -- FINAL OUTPUT --')
print(f'[MEM]: {memoria}')
print(f'tot: {nIstruzioni} istruzioni {col.ENDC}')
print(f'{col.HEADER}{col.BOLD}[ACC]: {accumulatore}{col.GREEN}{col.ENDC}\n')
