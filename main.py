import config as cfg
import glob, os, sys
from colorama import init
init()

"""TODO
- Sistemare i file di esempio
- Migliorare e testare l'interprete live
"""

#colors
class col:
	HEADER = '\033[95m' * cfg.colors
	CYAN = '\033[96m' * cfg.colors
	GREEN = '\033[92m' * cfg.colors
	WARNING = '\033[93m' * cfg.colors
	FAIL = '\033[91m' * cfg.colors
	ENDC = '\033[0m' * cfg.colors
	BOLD = '\033[1m' * cfg.colors

class vars:
	nIstruzioni = 0
	accumulatore = 0
	linea = 0
	fileInputStrings = []

	def getNextInput():
		try:
			return vars.fileInputStrings.pop(0)
		except IndexError as e:
			print(f"{col.FAIL}ERROE: Il file {cfg.inputFile} non ha abbastanza input{col.ENDC}")
			sys.exit(0)

#n of instructions counter
def incIst():
	vars.nIstruzioni += 1

#i/o instructions
def read():
	incIst()
	if(cfg.useFileInput):
		inp = vars.getNextInput()
	else:
		inp = input(f'{col.CYAN}input > ')
	
	try: #ensures to store an int if the value is a number
		vars.accumulatore = int(inp)
	except:
		vars.accumulatore = inp
	print(col.ENDC, end = '')

def write():
	incIst()
	nastroScr = vars.accumulatore
	print(f'{col.GREEN}output > {nastroScr}')
	print(col.ENDC, end = '')

def load(x):
	incIst()
	vars.accumulatore = memoria[int(x)]

def store(x):
	incIst()
	memoria[int(x)] = vars.accumulatore

#arithmetic instructions
def add(x):
	incIst()
	vars.accumulatore += memoria[int(x)]

def sub(x):
	incIst()
	vars.accumulatore -= memoria[int(x)]

def mult(x):
	incIst()
	vars.accumulatore *= memoria[int(x)]

def div(x):
	incIst()
	vars.accumulatore //= memoria[int(x)]

def loadEq(x):
	incIst()
	vars.accumulatore = x

def addEq(x):
	incIst()
	vars.accumulatore += x

def subEq(x):
	incIst()
	vars.accumulatore -= x

def multEq(x):
	incIst()
	vars.accumulatore *= x

def divEq(x):
	incIst()
	vars.accumulatore //= x

#logic instructions
def br(x): #BRanch (unconditioned)
	incIst()
	vars.linea = int(x)

def beq(x): #BranchEQual (if [ACC] == 0)
	incIst()
	if (vars.accumulatore == 0):
		vars.linea = int(x)

def bge(x): #BranchGreaterEqual (if [ACC] >= 0)
	incIst()
	if (vars.accumulatore >= 0):
		vars.linea = int(x)

def bg(x): #BranchGreater (if [ACC] > 0)
	incIst()
	if (vars.accumulatore > 0):
		vars.linea = int(x)

def ble(x): #BranchLowerEqual (if [ACC] <= 0)
	incIst()
	if (vars.accumulatore <= 0):
		vars.linea = int(x)

def bl(x): #BranchLower (if [ACC] < 0)
	incIst()
	if (vars.accumulatore < 0):
		vars.linea = int(x)

def loadAt(x): #Load [memoria[x]]
	incIst()
	addr = memoria[x]
	load(int(addr))

def storeAt(x): #Store [memoria[x]]
	incIst()
	addr = memoria[x]
	store(int(addr))


def parseLine(line):
	line = line.split(cfg.commentChar, 1)[0] #remove comments (line is string)
	x = line.split() #split string for management (x is list)
	return x

# --- Script Start ---
files = [] #Stores .code dirs
live = False #toggles live interpreter

if(cfg.fileName == ''): #if fileName is blank: look for *.code and ask which to open
	os.chdir("./")
	x = 0
	for file in glob.glob("*.code"):
		files.append(file)
		print(f"[{x}]{file}")
		x+=1

	files.append(0) #Last option is live interpreter
	print(f"{col.CYAN}[{x}] Interprete live{col.ENDC}")

	print("\nQuale file vuoi aprire?")	#Query user for file input !
	res = int(input("[int] > "))
	
	if(res == len(files)-1): #Live interpreter
		live = True
		#print('Live interpreter settings:') COMBAK
	else: #.code file
		cfg.fileName = files[res]

if(cfg.useFileInput and live): #toggles stdin from file/user input
	with open(cfg.inputFile) as f:
		vars.fileInputStrings = f.read().splitlines()

with open(cfg.outputFile, "w") as f: #Resets output file
	f.write('')

#init vars
nastroScr = 0 #stdin
memoria = {}  #ram structure:	memoria{addr: val}

#system vars
rawCode = [] #to be parsed
code = {}	#structure:	code{x: [istr, val]}	(val has int casts for specific use cases)
			#es:	code{0: ['LOAD', '1']}		(eg. mem addr can't be string)

if not live: #if not live -> parse .code file
	#open and read istructions
	with open(cfg.fileName) as f:
		rawCode = f.readlines()

	#separate istructions from arguments, and remove comments
	i = 0
	for line in rawCode:

		x = parseLine(line) #x is list (eg. x -> ['load=', '120'])

		#store commands in dict {row:[cmd, arg]} row always starts at 0
		if(x != []): #if row is not comment
			try: #has args
				code[i] = [x[0].upper(), x[1]] #[cmd, arg]
			except IndexError: #has no args
				code[i] = [x[0].upper()] #[cmd]
		i+=1

	hadLnstrt = 0
	hadEnd = 1
	for x in code:
		if(code[x][0] == 'LNSTRT'):
			cfg.startLine = int(code[x][1])
			hadLnstrt = x
		if(code[x][0] == 'END'):
			hadEnd = 0

	if(hadLnstrt): #if it had LNSTRT delete the dict key containing that instruction
		del code[hadLnstrt]
		del hadLnstrt

	if(hadEnd): #if it had no END instruction add it at the end
		code[len(code)] = ['END']


#execute
while True: #for word in code
	istr = vars.linea
	vars.linea += 1

	if live:
		code[istr] = parseLine(input('[ISTR] > '))

	cmd = code[istr][0] #command x
	try:
		arg = code[istr][1] #arg x
		arg = int(arg)
	except IndexError:
		arg = None


	#debug
	if(cfg.showDebug):
		print(f'  [DEBUG]---------{col.BOLD}istr:{vars.nIstruzioni}{col.ENDC}-------[ln:{istr+cfg.startLine}]')
		print(f'  [ACC]: {vars.accumulatore}')
		print(f'  [MEM]: {memoria}')
		print(f'  cmd:{col.WARNING} {cmd}{col.ENDC}; arg:{col.WARNING} {arg}{col.ENDC}')
	if(not cfg.minimalOutput and cfg.outputFile != ''):
		with open(cfg.outputFile, "a") as f:
			f.write(f'[DEBUG]---------istr:{vars.nIstruzioni}-------[ln:{istr+cfg.startLine}]\n')
			f.write(f'[ACC]: {vars.accumulatore}\n')
			f.write(f'[MEM]: {memoria}\n')
			f.write(f'cmd: {cmd}; arg: {arg}\n')

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
			loadAt(arg)
		elif(cmd == 'STORE@'):
			storeAt(arg)
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
		elif(cmd == 'END'):
			break
		else:
			print(f'{col.FAIL}ERROR, command not found')
			print(f'  ->"{cmd}"')
			print(f'{col.BOLD}  line:{istr+cfg.startLine}{col.ENDC}')
	except KeyError: #Could be triggered by x in: LOAD x; STORE x; LOAD@ x; STORE@ x;
		print(f'{col.FAIL}ERROR, address in memory does not exit')
		print(f'    AT LINE: {istr+cfg.startLine}')
		print(f'    [MEM]: {memoria}')
		print(f'    cmd -> cmd:{col.WARNING} {cmd}{col.FAIL}; arg:{col.WARNING} {arg}{col.ENDC}')
		if not live:
			exit()
	except ZeroDivisionError:
		print(f'{col.FAIL}ERROR, Division by 0')
		print(f'    AT LINE: {istr+cfg.startLine}')
		print(f'    [MEM]: {memoria}')
		print(f'    cmd -> cmd:{col.WARNING} {cmd}{col.FAIL}; arg:{col.WARNING} {arg}{col.ENDC}')
		if not live:
			exit()
	except TypeError:
		print(f'{col.FAIL}ERROR, (probable) InputError')
		print(f"    L'argomento inserito non è valido!")
		print(f'    AT LINE: {istr+cfg.startLine}')
		print(f'    [ACC]: {vars.accumulatore}')
		print(f'    [MEM]: {memoria}')
		print(f'    cmd -> cmd:{col.WARNING} {cmd}{col.FAIL}; arg:{col.WARNING} {arg}{col.ENDC}')
		if not live:
			exit()
		#else
		print(f"{col.WARNING}l'ultima istruzione sarà ignorata, riscrivila correttamente.{col.ENDC}")
		vars.linea -= 1


#print output
print(' -- FINAL OUTPUT --')
print(f'[MEM]: {memoria}')
print(f'tot: {vars.nIstruzioni} istruzioni {col.ENDC}')
print(f'{col.HEADER}{col.BOLD}[ACC]: {vars.accumulatore}{col.GREEN}{col.ENDC}\n')
if(not cfg.minimalOutput and cfg.outputFile != ''):
	with open(cfg.outputFile, "a") as f:
		f.write(' -- FINAL OUTPUT --\n')
		f.write(f'[MEM]: {memoria}\n')
		f.write(f'tot: {vars.nIstruzioni} istruzioni\n')
		f.write(f'[ACC]: {vars.accumulatore}\n')
elif(cfg.outputFile != ''):
	with open(cfg.outputFile, "a") as f:
		f.write(f'{vars.accumulatore}')
sys.exit(1)