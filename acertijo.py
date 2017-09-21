#-*- coding: utf-8 -*-

"""
RESOLUCIÓN DE UN ACERTIJO CON BÚSQUEDA DE RESULTADOS EN LA RAE
	Version: 1.0
	Creador: Jesús Moncada Ramírez
	Email: jemonra@gmail.com
	Web: elinternetdemiscosas.blogspot.com
	
	Requisitos:
		- bs4
		- lxml
		- requests
		
Para la búsqueda de palabras en la RAE se utiliza la librería pyrae de Angel Carmona https://github.com/angelcarmona/pyrae
"""

from datetime import datetime	# Para saber la hora
import pyrae 					# Para buscar palabras en la RAE

abecedario = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
abecedario_prohibido = [] # Listado de letras que no aparecen en el acertijo

vocales = [['a', 'e', 'i', 'o', 'u'], ['á', 'é', 'í', 'ó', 'ú']] # Vocales sin y con tilde

gran_palabra = ['', '', '', '', ''] # Palara que analizará el bucle

# Acertijo en sí
deduccion = [[['R', 'E', 'T', 'A', 'L'] ,[0, 0]], #Fila 1
			 [['M', 'O', 'R', 'S', 'A'] ,[2, 1]], #Fila 2
			 [['C', 'E', 'N', 'I', 'T'] ,[2, 1]], #Fila 3
			 [['A', 'R', 'D', 'U', 'O'] ,[2, 1]], #Fila 4
			 [['T', 'U', 'M', 'B', 'A'] ,[2, 1]]] #Fila 5

encontradas = [] # Lista de las palabras que coinciden las normas del acertijo
encontradasRAE = [] # Lista de las palabras que además de seguir las normas del acertijo están en la RAE

def prit(mensaje): # Similar a print pero que además muestra la hora, una especie de log
	ahora = datetime.now()
	print('{0}:{1}:{2} | {3} '.format(ahora.hour, ahora.minute, ahora.second, mensaje))
	
def creaAbcProhib(): # Crea el abecedario prohibido
	
	abecedario_prohibido = list(abecedario)
	
	for fila in deduccion: # Por cada fila
		for letra in fila[0]: # Por cada letra
			# Elimina la letra del abecedario prohibido
			if letra in abecedario_prohibido:
				abecedario_prohibido.remove(letra)
	
	#prit(abecedario_prohibido)

def comprobarRestricciones(palabra): # Filtrado de restricciones que las palabras deben cumplir, son las reglas del acertijo
	
	# Comprobar si la palabra contiene letras prohibidas
	for letra_pro in abecedario_prohibido:
		if letra_pro in palabra:
			return False
	
	# Comprobar si tiene deduccion[x][1][0] letras por cada fila
	for fila in deduccion:
		contador = 0
		for letra in fila[0]:
			if palabra.count(letra)>=1:
				contador += 1
		if contador != fila[1][0]:
			return False
	
	# Comprobar si tiene deduccion[x][1][1] letras fijas por cada fila
	for fila in deduccion:
		contador = 0
		for num_letra in range(len(fila[0])):
			if palabra[num_letra] == fila[0][num_letra]:
				contador += 1
		if contador != fila[1][1]:
			return False
	
	# Finalmente, si ninguna restricción ha saltado, devuelve True
	return True
	
rae = pyrae.DLE() # Creamos el diccionario RAE (Se necesita conexión a internet)

def comprobarRae(palabra): # Busca una palabra la RAE y devuelve True si existe y False si no
	r = rae.exact(palabra)
	
	if r == [] or r == None:
		return False
	else:
		prit('PALABRA ENCONTRADA EN RAE!!! "{0}"'.format(palabra))
		return True
	
def replace_index(text, index=0, replacement=''): # Remplaza un caracter en una cadena por su index
    return '{0}{1}{2}'.format(text[:index],replacement,text[index+1:])

def list_to_str(lista): # Pasa una lista a str
	devolver = ''
	for letra in lista:
		devolver += letra
	return devolver

def es_vocal(letra): # Comprueba si una letra es vocal
	return letra in vocales[0]

def informe(): # Muestra un informe de las palabras encontradas (al final del programa)
	prit(
    """Fin del programa:
	Palabras encontradas {0}
	Palabras encontradas en la RAE {1}""".format(encontradas, encontradasRAE))

# Inicio del programa 

try:

	prit('Inicio del programa, descifrando el acertijo...')

	creaAbcProhib() # Crea el abecedario prohibido
	
	# Empiezan el bucle que genera todas las palabras posibles con 5 letras
	for letra in abecedario: #1 caracter
		gran_palabra[0] = letra
	
		for letra in abecedario: #2 caracter
			gran_palabra[1] = letra
		
			for letra in abecedario: #3 caracter
				gran_palabra[2] = letra
			
				for letra in abecedario: #4 caracter
					gran_palabra[3] = letra
				
					for letra in abecedario: #5 caracter
						gran_palabra[4] = letra
					
						if comprobarRestricciones(gran_palabra): 
							##Si ha superado las restricciones es una de las palabras!!!##
							prit('PALABRA ENCONTRADA!!! {0}'.format(list_to_str(gran_palabra)))
							
							encontradas.append(list_to_str(gran_palabra))
							
							# Pasa la palabra a str
							gran_palabra_str = list_to_str(gran_palabra).lower()
							
							# Comprueba la palabra en el RAE
							if comprobarRae(gran_palabra_str):
								encontradasRAE.append(gran_palabra_str)
							
							else: # Si no está en la RAE se acentúan una por una las vocales que tenga y se repite la comprobación en la RAE
								
								for num_letra in range(len(gran_palabra_str)): # Por cada letra (index) de la str de la palabra
									
									gran_palabra_str_mod = gran_palabra_str # Palabra modificable
									
									letra = gran_palabra_str_mod[num_letra] # Letra de la palabra	
									
									if es_vocal(letra): # Si la letra es una vocal
										
										remplazo = vocales[1][vocales[0].index(letra)] # El remplazo con tilde tiene el index de la vocal en vocales[0]
										
										gran_palabra_str_mod = replace_index(gran_palabra_str_mod, num_letra, remplazo) # Remplaza la palabra sustituyendo la vocal por su acentuada
										
										if comprobarRae(gran_palabra_str_mod): # Comprueba esa nueva palabra acentuada en la RAE
											encontradasRAE.append(gran_palabra_str_mod)
						
						#else:
						#	prit('NADA con la palabra {0}'.format(gran_palabra))
	
	informe()
	
except KeyboardInterrupt:
	
	informe()
