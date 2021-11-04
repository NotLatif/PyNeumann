# PyNeumann
Un simulatore delle istruzioni di Von Neumann (made by NotLatif)

## La macchina di Von Neumann  
La [macchina di Von Neumann](https://it.wikipedia.org/wiki/Architettura_di_von_Neumann) è costituita da quattro elementi fondamentali:

- l'unità di elaborazione (CPU)
- la memoria centrale (RAM)
- le periferiche (interfaccia I/O)
- il bus di sistema

## Le istruzioni
 #### I/O
- `READ`: legge dal nastro di input
- `WRITE`: scrive sul nastro di output
 #### Memoria
- `LOAD x`: Il contenuto della cella x viene trasferito all'accumulatore
- `STORE x`: Il contenuto dell'accumulatore viene trasferito alla cella x
- `LOAD@ x`: Viene trasferito all'accumulatore il contenuto della cella il cui indirizzo è contenuto nella cella x
- `STORE@ x`: Viene immagazzinato in memoria il contenuto della dell'accumulatore all'indirizzo contenuto nella cella x
 #### Aritmetica
- Il risultato delle operazioni viene immagazzinato nell'accumulatore
- `ADD x`: Addizione tra accumulatore e contenuto della cella x
- `SUB x`: Sottrazione tra accumulatore e contenuto della cella x
- `MULT x`: moltiplicazione tra accumulatore e contenuto della cella x
- `DIV x`: divisione intera tra accumulatore e contenuto della cella x
- `ADD= n`: viene sommato il valore n all'accumulatore
- `SUB= n`: viene sottratto il valore n all'accumulatore
- `MULT= n`: viene moltiplicato il valore n all'accumulatore
- `DIV= n`: viene effettuata la divisione intera tra l'accumulatore e il valore n
#### Logica
- `BR x`: (branch) salta incondizionatamente alla riga x del codice
- `BEQ x`: (branch equal) salta alla riga x se il valore dell'accumulatore è = a 0
- `BGE x`: (branch greater equal) salta alla riga x se il valore dell'accumulatore è >= di 0
- `BG x`: (branch greater) salta alla riga x se il valore dell'accumulatore è > di 0
- `BLE x`: (branch lower equal) salta alla riga x se il valore dell'accumulatore è <= di 0
- `BL x`: (branch lower) salta alla riga x se il valore dell'accumulatore è < di 0
#### Misc
- `END`: definisce la fine del programma
- `$LNSTRT x`: definisce il numero della prima riga di codice (va usato dopo l'istruzione `END`)
- `#`: può essere usato in qualsiasi punto per definire un commento in riga (eg. LOAD= 0 #CARICA IL VALORE 0 NELL'ACCUMULATORE)

## Funzionamento del codice

##### `main.py`
Il programma principale: `main.py` apre il file `config.filename` e lo legge riga per riga eseguendo le istruzioni di Von Neumann senza badare di maiuscole e minuscole (non è case sensitive). Alla fine da come output il contentuto della memoria `[MEM]` in numero totale di istruzioni ed il contenuto dell'accumulatore `[ACC]`

##### `config.py`
Questo è il file di configurazione che contiene alcuni parametri modificabili dall'utente:
- `showDebug` (`bool`) -> [`True`] da come output l'esecuzione del programma istruzione per istruzione mentre viene interpretato; altrimenti [`False`] restituisce solo il risultato finale
- `startLine` (`int`) -> definisce la linea da cui si vuole iniziare a contare. Normalmente nel linguaggio di Von Neumann la prima riga è la riga `0`, però per facilità di scrittura del codice attraverso editor di testo che iniziano a contare le righe da `1`, il valore si può impostare ad 1
- `commentChar`(`char`) -> permette di cambiare il carattere scelto per i commenti (default: `#`)
- `filename` (`string`) -> definisce il file da leggere dal simulatore, può essere lasciato vuoto
 
####   ATTENZIONE
Il valore di `config.startLine` causerà problemi a codici scritti avendo in mente un valore diverso, per questo dopo l'istruzione `END`si può usare l'istruzone `$LNSTRT x` per sovrascrivere il valore di `config.startLine` con il valore `x`  

Se `config.filename` viene lasciato vuoto (`''`) il programma chiederà quale dei file `*.code` presenti nella stessa directory aprire 

## TODO
- la lista di cose da fare è presente all'inizio del file `main.py`
