import config as cfg
import glob, os, sys
from colorama import init
init()

"""TODO
- implementare utilizzo da linea di comando
- Sistemare i file di esempio
- Esistono 2 funzioni dentro il mainloop (funziona ma meglio cambiare)
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

#script-related
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

		#store commands in dict {row:[istr, arg]} row always starts at 0
		if(x != []): #if row is not comment
			try: #has args
				code[i] = [x[0].upper(), x[1]] #[istr, arg]
			except IndexError: #has no args
				code[i] = [x[0].upper()] #[istr]
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


#mainloop
while True: #until END instruction
	istrLn = vars.linea #si riferisce all'istruzione in linea vars.linea
	vars.linea += 1

	if live:					#[ISTR ln: linea-1 | ACC: acc]
		code[istrLn] = parseLine(input(f'{col.BOLD}{col.GREEN}[ISTR {col.WARNING}ln: {istrLn} | ACC: {vars.accumulatore}{col.GREEN}]{col.ENDC} > '))

	try:
		istr = code[istrLn][0] #command x
	except IndexError:
		istr = None

	try:
		arg = code[istrLn][1] #arg x
		arg = int(arg)
	except IndexError: # arg does not exist
		arg = None
	except ValueError: # arg is not a number
		arg = arg

	def exceptionCatch(): # handles exceptions below
		if live:
			print(f"{col.WARNING}l'ultima istruzione sarà ignorata, riscrivila correttamente.{col.ENDC}")
			vars.linea -= 1
		else:
			exit()
	def printDebug():
		if(cfg.showDebug):
			print(f'  [DEBUG]---------{col.BOLD}istr:{vars.nIstruzioni}{col.ENDC}-------[ln:{istrLn+cfg.startLine}]')
			print(f'  [ACC]: {vars.accumulatore}')
			print(f'  [MEM]: {memoria}')
			print(f'  istr:{col.WARNING} {istr}{col.ENDC}; arg:{col.WARNING} {arg}{col.ENDC}')
		if(not cfg.minimalOutput and cfg.outputFile != ''):
			with open(cfg.outputFile, "a") as f:
				f.write(f'[DEBUG]---------istr:{vars.nIstruzioni}-------[ln:{istrLn+cfg.startLine}]\n')
				f.write(f'[ACC]: {vars.accumulatore}\n')
				f.write(f'[MEM]: {memoria}\n')
				f.write(f'istr: {istr}; arg: {arg}\n')
	
	if(istr == 'READ' or istr == 'WRITE'): #prints debug before READ||WRITE instruction (to avoid confusion)
		printDebug()
	#instructions
	try:
		if(istr == 'READ'):#i/o
			read()
		elif(istr == 'WRITE'):
			write()
		elif(istr == 'LOAD'):#memory
			load(arg)
		elif(istr == 'STORE'): 
			store(arg)
		elif(istr == 'LOAD@'):
			loadAt(arg)
		elif(istr == 'STORE@'):
			storeAt(arg)
		elif(istr == 'ADD'):#arithmetic
			add(arg)
		elif(istr == 'SUB'):
			sub(arg)
		elif(istr == 'MULT'):
			mult(arg)
		elif(istr == 'DIV'):
			div(arg)
		elif(istr == 'LOAD='):
			loadEq(arg)
		elif(istr == 'ADD='):
			addEq(arg)
		elif(istr == 'SUB='):
			subEq(arg)
		elif(istr == 'MULT='):
			multEq(arg)
		elif(istr == 'DIV='):
			divEq(arg)
		elif(istr == 'BR'):#logic
			br(arg-cfg.startLine)
		elif(istr == 'BEQ'):
			beq(arg-cfg.startLine)
		elif(istr == 'BGE'):
			bge(arg-cfg.startLine)
		elif(istr == 'BG'):
			bg(arg-cfg.startLine)
		elif(istr == 'BLE'):
			ble(arg-cfg.startLine)
		elif(istr == 'BL'):
			bl(arg-cfg.startLine)
		elif (istr == 'END'):
			break #exits 'while True'
		else:
			print(f'{col.FAIL}ERROR, command not found')
			print(f'  ->"{istr}"')
			print(f'{col.BOLD}  line:{istrLn+cfg.startLine}{col.ENDC}')

	except KeyError: #Could be triggered by x in: LOAD x; STORE x; LOAD@ x; STORE@ x;
		print(f'{col.FAIL}ERROR, address in memory does not exit')
		print(f'    AT LINE: {istrLn+cfg.startLine}')
		print(f'    [MEM]: {memoria}')
		print(f'    istr -> istr:{col.WARNING} {istr}{col.FAIL}; arg:{col.WARNING} {arg}{col.ENDC}')
		exceptionCatch()

	except ZeroDivisionError:
		print(f'{col.FAIL}ERROR, Division by 0')
		print(f'    AT LINE: {istrLn+cfg.startLine}')
		print(f'    [MEM]: {memoria}')
		print(f'    istr -> istr:{col.WARNING} {istr}{col.FAIL}; arg:{col.WARNING} {arg}{col.ENDC}')
		exceptionCatch()

	except TypeError:
		print(f'{col.FAIL}ERROR, (probabile) InputError')
		print(f"    L'input inserito non è valido!")
		print(f'    AT LINE: {istrLn+cfg.startLine}')
		print(f'    [ACC]: {vars.accumulatore}')
		print(f'    [MEM]: {memoria}')
		print(f'    istr -> istr:{col.WARNING} {istr}{col.FAIL}; arg:{col.WARNING} {arg}{col.ENDC}')
		exceptionCatch()
		
	except ValueError:
		print(f'{col.FAIL}ERROR, (probabile) Invalid Argument')
		print(f"    L'argomento inserito non è valido!")
		print(f'    AT LINE: {istrLn+cfg.startLine}')
		print(f'    [ACC]: {vars.accumulatore}')
		print(f'    [MEM]: {memoria}')
		print(f'    istr -> istr:{col.WARNING} {istr}{col.FAIL}; arg:{col.WARNING} {arg}{col.ENDC}')
		exceptionCatch()
		
	
	#prints debug after instruction if istr is not READ or WRITE (to avoid confusion with instructions like STORE)
	if not(istr == 'READ' or istr == 'WRITE'):
		printDebug()


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