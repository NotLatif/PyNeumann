#TODO
# migliora con le classi
# cambia la directory del codice da leggere
# possibilità di scegliere il metodo di lettura DEBUG
# maybe? aggiungi un menu
# aggiungi commenti

class col:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def incIst():
    global nIstruzioni
    nIstruzioni += 1

def read():
    incIst()
    global accumulatore
    inp = input(f'{col.CYAN}input> ')
    try:
        accumulatore = int(inp)
    except:
        accumulatore = inp
    print(col.ENDC, end = '')

def write():
    incIst()
    nastroScr = accumulatore
    print(f'{col.GREEN}Nastro Scrittura > {nastroScr}')
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

def storeEq(x):
    incIst()
    pass #Instruction not defined

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

def br(x):
    incIst()
    global linea
    linea = int(x)

def beq(x):
    incIst()
    global linea
    if (accumulatore == 0):
        linea = x

def bge(x):
    incIst()
    global linea
    if (accumulatore >= 0):
        linea = x

def bg(x):
    incIst()
    global linea
    if (accumulatore > 0):
        linea = x

def ble(x):
    incIst()
    global linea
    if (accumulatore <= 0):
        linea = x

def bl(x):
    incIst()
    global linea
    if (accumulatore < 0):
        linea = x

def loadAt(x):
    incIst()
    pos = memoria[x]
    load(x)

def storeAt(x):
    incIst()
    pos = memoria[x]
    store(x)



if(__name__=='__main__'):
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
    with open('c:/Users/Latif/Desktop/Programmazione/PyProjects/Van Neumann/code.neumann') as f:
        rawCode = f.readlines()

    #separate code from arguments, and remove comments
    i = 0
    for word in rawCode:
        x = word.split()
        try:
            code[i] = [x[0].upper(), x[1]]
        except IndexError:
            code[i] = [x[0].upper()]
        i+=1
    
    if(code[len(code)-1] != 'END'):
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
        print(f'  [DEBUG]---------{col.BOLD}row:{istr}{col.ENDC}-------[]')
        print(f'  cmd:{col.WARNING} {cmd}{col.ENDC}; arg:{col.WARNING} {arg}{col.ENDC}')
        print(f'  [ACC]: {accumulatore}')
        print(f'  [MEM]: {memoria}')

        if(cmd == 'READ'):
            read()
        elif(cmd == 'WRITE'):
            write()
        elif(cmd == 'LOAD'):
            load(arg)
        elif(cmd == 'STORE'): 
            store(arg)
        elif(cmd == 'ADD'):
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
        elif(cmd == 'BR'):
            br(arg)
        elif(cmd == 'BEQ'):
            beq(arg)
        elif(cmd == 'BGE'):
            bge(arg)
        elif(cmd == 'BG'):
            bg(arg)
        elif(cmd == 'BLE'):
            ble(arg)
        elif(cmd == 'BL'):
            bl(arg)
        elif(cmd == 'LOAD@'):
            loadAt(arg)
        elif(cmd == 'STORE@'):
            storeAt(arg)
        elif(cmd == 'END'):
            break
        else:
            print(f'{col.FAIL}ERROR, command not found')
            print(f'  ->"{cmd}"')
            print(f'{col.BOLD}  row:{istr}{col.ENDC}')
    
print(f'{col.GREEN}{col.BOLD}[ACC]: {accumulatore}')
print(f'[MEM]: {memoria}')
print(f'tot: {nIstruzioni} istruzioni {col.ENDC}')
