#!/usr/bin/env python3
import sys
import heapq
from collections import Counter
import pickle
import json

#funcion para calcular las probabilidades de aparecer de cada caracter
def probs(frase):
    total = len(frase) + 1 # Agregamos uno por el caracter FINAL
    c = Counter(frase)
    res = {}
    for char,count in c.items():
        res[char] = float(count)/total #se forma la tupla
    res['end'] = 1.0/total
    #print(res)
    
    return res

#funcion para obtener el árbol binario
def arbol(probs):
    cola = []
    for char,prob in probs.items():
        # La fila de prioridad está ordenada por prioridad y PROFUNDIDAD
        heapq.heappush(cola,(prob,0,char))

    while len(cola) > 1:
        e1 = heapq.heappop(cola)
        e2 = heapq.heappop(cola)
        nw_e = (e1[0]+e2[0],max(e1[1],e2[1])+1,[e1,e2])
        heapq.heappush(cola,nw_e)
    return cola[0]

#función para crear el diccionario con los codigos binarios de cada byte
def diccionario(arbol):
    res = {}
    buscar = []
    buscar.append(arbol+("",)) # El último elemento de la lista es el prefijo!
    while len(buscar) > 0:
        e = buscar.pop()
        if type(e[2]) == list:
            pre = e[-1]
            buscar.append(e[2][1]+(pre+"0",))
            buscar.append(e[2][0]+(pre+"1",))
            continue
        else:
            res[e[2]] = e[-1]
        pass
    return res

#función para codificar 
def codificar(dic,cont):
    
    res = ""
    for char in cont:
        code = dic[char]
        res = res + code
    res = '1' + res + dic['end'] # Agregamos el caracter final y el 1 inicial
    res = res + (len(res) % 8 * "0") # Agregamos ceros para convertir en multiplo de 8
    print (res)
    
    return int(res,2)

#funcion para guardar

def store(data,dic,outfile):
    # Lo guardamos en un archivo
    outf = open(outfile,'wb')
    pickle.dump(codigo,outf)
    outf.close()

    # Guardamos el diccionario en otro archivo
    outf = open(outfile+".dic",'w')
    json.dump(dic,outf)
    outf.close()
    pass


if __name__ == "__main__":
    usage = """Usage: ./Main.py fichero_de_entrada fichero_de_salida"""

    if len(sys.argv) < 3:
        print(usage)
        sys.exit(1)

    #leer archivo de entrada
    inf = open(sys.argv[1])
    frase = inf.read()
    inf.close()
    #calcular probabilidad
    probabilidad = probs(frase)
    #crear arbol
    arbol1=arbol(probabilidad)
    #diccionario
    dic=diccionario(arbol1)
    #codidicar
    codigo =codificar(dic,frase)
    #almacenar
    store(codigo,dic,sys.argv[2])
    print("Archivo comprimido!")