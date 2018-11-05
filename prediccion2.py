from __future__ import division
import matplotlib.pyplot as plt

def getMat(matriz1, matriz2):
    matrizResul = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
    suma=0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                suma = suma + (matriz1[i][k]*matriz2[k][j])
            matrizResul[i][j]=suma
            suma=0
    return matrizResul

def mult(matriz1, matriz2):
    matrizResul = [0.0,0.0,0.0]
    suma=0
    for j in range(3):
        for k in range(3):
            suma = suma + (matriz1[k]*matriz2[k][j])
        matrizResul[j]=suma
        suma=0
    return matrizResul

def evaluar(prob):
    if prob[0] > prob[2] and prob[0] > prob[1]:
        est = "C"
    elif prob[2] > prob[0] and prob[2] > prob[1]:
        est = "D"
    else:
        est = "I"
    return est
             
if True:
    estados=[0,0,0]
    years = [1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
    pib = [10667860,9996721,10673824,11404645,11993573,12323822,12932921,12880622,12875490,13061719,13573815,13887073,14511307,14843826,15013578,14219998,14947795,15495334,16059724,16277187,16733655,17283856,17784718,18147787 ]

    fig, ax = plt.subplots()
    ax.plot(years, pib)
    ax.set(xlabel='year', ylabel='PIB', title='La situacion economica a traves del tiempo')
    ax.grid()
    plt.show()
    fig.savefig("fig.png")

    actividad = []
    evalu = ["","","","","","","",""]
    CaC = 0
    CaI = 0
    CaD = 0
    IaC = 0
    IaI = 0
    IaD = 0
    DaC = 0
    DaI = 0
    DaD = 0
    cont = 0
    transiciones = [0 for i in range(9)]
    matrizT = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
    matrizT2 = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
    matrizT3 = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
    matrizT4 = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
    matrizT5 = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
    matrizT6 = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
    totalYears = len(years)
    for i in range(len(years)-1):
        if(pib[i+1] > pib[i]):
            estados[0] += 1
            actividad.append("C")
        elif(pib[i+1] == pib[i]):
            estados[1] += 1
            actividad.append("I")
        else:
            estados[2] += 1
            actividad.append("D")
            print(estados)
            print(actividad)
    for i in range(len(actividad)-1):
        if(actividad[i] == "C" and actividad[i+1] == "C"):
            CaC+=1
            transiciones[0] +=1
        elif(actividad[i] == "C" and actividad[i+1] == "I"):
            CaI+=1
            transiciones[1] +=1
        elif(actividad[i] == "C" and actividad[i+1] == "D"):
            CaD+=1
            transiciones[2] +=1
        elif(actividad[i] == "I" and actividad[i+1] == "C"):
            IaC+=1
            transiciones[3] +=1
        elif(actividad[i] == "I" and actividad[i+1] == "I"):
            IaI+=1
            transiciones[4] +=1
        elif(actividad[i] == "I" and actividad[i+1] == "D"):
            IaD+=1
            transiciones[5] +=1
        elif(actividad[i] == "D" and actividad[i+1] == "C"):
            DaC+=1
            transiciones[6] +=1
        elif(actividad[i] == "D" and actividad[i+1] == "I"):
            DaI+=1
            transiciones[7] +=1
        elif(actividad[i] == "D" and actividad[i+1] == "D"):
            DaD+=1
            transiciones[8] +=1
        else:
            print("Error")
            print(DaC)
            print(transiciones)
    #Generando matriz de transicion
    for i in range(3):
        for j in range(3):
            suma = transiciones[cont+i] + transiciones[cont+i+1] + transiciones[cont+i+2]
            if( suma != 0 ):
                matrizT[i][j] = transiciones[j+cont+i] / (transiciones[cont+i] + transiciones[cont+i+1] + transiciones[cont+i+2])
        cont+=2
    #Generando las siguientes matrices
    print("\n")
    matrizT2 = getMat(matrizT, matrizT)
    matrizT3 = getMat(matrizT, matrizT2)
    matrizT4 = getMat(matrizT, matrizT3)
    matrizT5 = getMat(matrizT, matrizT4)
    matrizT6 = getMat(matrizT, matrizT5)
    #Obteniendo las probabilidades para el siguiente sexenio
    #n=1
    probs=[[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
    for i in range(3):
        probs[0][i] = estados[i] / sum(estados)
    probs[1] = mult(probs[0], matrizT)
    probs[2] = mult(probs[1], matrizT2)
    probs[3] = mult(probs[2], matrizT3)
    probs[4] = mult(probs[3], matrizT4)
    probs[5] = mult(probs[4], matrizT5)
    probs[6] = mult(probs[5], matrizT6)
                
    for i in range(7):
        print("Para el numero "+str(i+1)+" se espera: ")
        evalu[i] = evaluar(probs[i])
        print(evalu[i])
        print("\n")