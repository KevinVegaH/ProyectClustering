import random as rd
import numpy as np
import math
from matplotlib import pyplot as plt


def inercia(centroides, clusters):  # <-- Calcula el costo.
    cost_total = 0
    for i in range(len(clusters)):
        for j in range(len(clusters.get(str(centroides[i])))):
            aux = 0
            for k in range(len(clusters[str(centroides[i])][0])):
                summ = (float(clusters[str(centroides[i])][j][k]) - float(centroides[i][k])) ** 2
                aux += summ
            cost_total += aux

    return cost_total


def update(centroides, clusters):  # <-- Actualiza los centroides.
    for i in range(len(clusters)):
        listAuxi = []
        for j in range(len(clusters[str(centroides[i])][0])):
            sum = 0
            for k in range(len(clusters.get(str(centroides[i])))):
                var = float(clusters[str(centroides[i])][k][j])
                sum = sum + var
            valu = sum / len(clusters.get(str(centroides[i])))
            listAuxi.append(valu)
        centroides[i] = listAuxi

    return centroides


def distancia(centroides, lista):  # <-- Distancia entre los centroides y puntos.
    suma = 0
    for k in range(len(lista)):
        suma = suma + (float(centroides[k]) - float(lista[k])) ** 2
    resultado = math.sqrt(suma)

    return resultado


def centroides_inicial(lista, numero_centroides, iteraciones):
    cost = []
    dictionary_cost = {}
    cont = 0
    for i in lista:  # <--- contamos la cantidad de datos dentro de lista.
        r = cont
        # print(r, i)
        cont += 1

    for M in range(iteraciones):  # <-- Numero de iteraciones.

        centroides = []  # <-- Almacena los centroides.

        while len(centroides) != numero_centroides:  # <-- Determinamos los centroides iniciales, en este caso 10.

            n = rd.randrange(cont)
            if n not in centroides:
                centroides.append(lista[n])  # <-- Tomamos los centroides iniciales elegidos aletatoriamente y los
            # guardamos en una lista centroides

        listDistancias = []
        for i in range(numero_centroides):

            for j in range(len(lista)):
                listDistancias.append(distancia(centroides[i], lista[j]))  # <--- añadimos a una lista las distancias.

        xT = np.array(listDistancias).reshape(numero_centroides, len(lista))  # <-- creamos una matriz de numero de
        # cluster por el tamaño de la lista de datos.

        indix = []  # <-- lista de indices.
        for i in range(len(lista)):
            auxi = []
            for j in range(numero_centroides):
                auxi.append(xT[j][i])

            indix.append(
                auxi.index(min(auxi)))  # <-- tomamos las posiciones de cada clusters y comparamos cual distancia
            # menor entre centroides y almacenamos el indice donde se encuentra la menor distancia.

        clus = {}  # <-- Diccionario de centroides.
        for i in range(numero_centroides):
            n = str(centroides[i])  # <-- Convertimos el centroide en String.
            clus[n] = []  # <-- Asignamos el centroide como una Key dentro del diccionario Clus
            for j in range(len(lista)):
                if i == indix[j]:  # <-- Asginamos los ejemplos a su respectivo centroide mediante el indice.
                    clus[str(centroides[i])].append(lista[j])

        for i in range(numero_centroides):
            print(i, ") ", str(centroides[i]), " - ", clus.get(str(centroides[i])))  # <-- Imprimimos los centroides
            # con sus ejemplos.

        conte = 0
        for i in range(numero_centroides):
            tam = len(clus.get(str(centroides[i])))  # <-- Obtenemos la cantidad de datos de un centroide.
            conte = conte + tam
        print("Total de datos:", conte)

        iner = inercia(centroides, clus)  # <-- Funcion de Costo
        cost.append(iner)  # <-- almacenamos los costos en una lista llamada cost
        dictionary_cost[str(iner)] = [x for x in centroides]  # <-- Este diccionario almacena el costo como una Key
        # y guarda sus respectivos centroides como values.
        print("costo:", iner)  # <-- Muestra el costo en la iteracion.

    minCost = dictionary_cost[min(dictionary_cost.keys())]  # <-- Calculamos el costo minimo.
    return minCost  # <-- retornamos los centroides del costo minimo.


def k_means(lista, numero_centroides, iteraciones):
    cost = []
    centroides = centroides_inicial(lista, numero_centroides, iteraciones)
    print("->", centroides)

    for M in range(iteraciones):  # <-- Numero de iteraciones.

        listDistancias = []
        for i in range(numero_centroides):

            for j in range(len(lista)):
                listDistancias.append(distancia(centroides[i], lista[j]))  # <--- añadimos a una lista las distancias.

        xT = np.array(listDistancias).reshape(numero_centroides, len(lista))  # <-- creamos una matriz de numero de
        # cluster por el tamaño de la lista de datos.

        indix = []
        for i in range(len(lista)):
            auxi = []
            for j in range(numero_centroides):
                auxi.append(xT[j][i])

            indix.append(auxi.index(min(auxi)))

        clus = {}
        for i in range(numero_centroides):
            n = str(centroides[i])
            clus[n] = []
            for j in range(len(lista)):
                if i == indix[j]:
                    clus[str(centroides[i])].append(lista[j])

        for i in range(numero_centroides):
            print(i, ") ", str(centroides[i]), " - ", clus.get(str(centroides[i])))

        conte = 0
        for i in range(numero_centroides):
            tam = len(clus.get(str(centroides[i])))
            conte = conte + tam
        print("Total de datos:", conte)

        iner = inercia(centroides, clus)
        cost.append(iner)
        print("costo:", iner)

        update(centroides, clus) # < -- Actualizamos los Centroides

    return cost # <-- Retonamos una lista de costos.


# >-----------------MAIN------------------< #

print("1) dataset1.txt")
print("2) dataset2.txt")

dataSet = ""
while True:
    op = str(input("¿Cual set de datos desea analizar?"))
    if op == "1" or op == "2":
        dataSet = "dataset"+op+".txt"
        break
    else:
        print("Dato incorrecto, vuelta a intentarlo.")


file = open(dataSet, 'r')  # <--- abrimos el archivo y lo leemos.
datos = file.readlines()  # <--- leemos  el archivo y readlines() devuelve una lista que contiene las líneas.

lista = []
numero_centroides = 10  # <-- se define el numero de centroides a tener.
numero_iteraciones = 10  # <-- se define el numero de iteraciones.

for i in range(len(datos)):  # <-- añadimos los datos del archivo en una lista, desaparecemos '\n' con .strip y
    lista.append(datos[i].strip().split(","))  # convertimos cada linea en una lista con split().
file.close()  # <-- Cerramos el archivo usando .close()

valu = k_means(lista, numero_centroides, numero_iteraciones)

plt.plot([i for i in range(numero_centroides)], valu, marker="o")
plt.title(dataSet+": Cost Vs centroids")
plt.xlabel("centroids")
plt.ylabel("Cost")
plt.show()
