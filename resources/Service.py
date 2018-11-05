from flask_restful import Resource
from flask import request, send_file, jsonify
import json
import matplotlib.pyplot as plt
import random


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

class Service(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No se enviaron datos'}
        res2 = json.loads(json_data)
        print(res2['data'][0]["year"])
        datos = res2['data']
        years = [0 for i in range(len(datos))]
        pibs = [0 for i in range(len(datos))]
        for year in range(len(datos)):
            years[year] = datos[year]["year"]
            pibs[year] = int(datos[year]["pib"])
        ##Generando grafica
        fig, ax = plt.subplots()
        ax.plot(years, pibs)
        ax.set(xlabel='year', ylabel='PIB', title='La situacion economica a traves del tiempo')
        ax.grid()
        name = "i" + str(random.randint(10000,99999))
        fig.savefig("fig.png")
        ##Proceso
        estados=[0,0,0]
        actividad = []
        evalu = ["","","","","","",""]
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
            if(pibs[i+1] > pibs[i]):
                estados[0] += 1
                actividad.append("C")
            elif(pibs[i+1] == pibs[i]):
                estados[1] += 1
                actividad.append("I")
            else:
                estados[2] += 1
                actividad.append("D")
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
        #Generando matriz de transicion
        for i in range(3):
            for j in range(3):
                suma = transiciones[cont+i] + transiciones[cont+i+1] + transiciones[cont+i+2]
                if( suma != 0 ):
                    matrizT[i][j] = transiciones[j+cont+i] / (transiciones[cont+i] + transiciones[cont+i+1] + transiciones[cont+i+2])
            cont+=2
        #Generando las siguientes matrices
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
        print(actividad)
        for i in range(7):
            print("Para el numero "+str(i+1)+" se espera: ")
            evalu[i] = evaluar(probs[i])
            print(evalu[i])
            print("\n")
        resp = '{ "predicciones": '+ json.dumps(evalu) + '}'
        print(resp)
        ##Retorno de Datos
        return resp,201
class Service2(Resource):
    def get(self):
        return send_file('fig.png',mimetype='image/png')
        ##{'message':'Hiciste un GET!'}