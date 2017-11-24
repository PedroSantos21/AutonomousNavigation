#coding: utf-8
import time
import vrep
import keras
import math
import localization
import blending
import numpy as np
from keras.models import Model
from keras.models import load_model

serverIP = "127.0.0.1"
serverPort = 19999
#---------------------Conecta no servidor---------------------------------
clientID = vrep.simxStart(serverIP, serverPort, True, True, 2000, 5)
nomeSensor = []
sensorHandle = []
dist = []
leftMotorHandle = 0
rightMotorHandle = 0
global v_Left, v_Right, tacoDir, tacoEsq, path_lenght, colisao, atingiu, oscilacoes
v_Left =0.5
v_Right = 0.5
colisao = False
atingiu = False
oscilacoes = 0

if (clientID!=-1):
	print ("Servidor Conectado!")

#------------------------------Inicializa Sensores ----------------------------
	for i in range(0,8):
		nomeSensor.append("sensor" + str(i+1))

		res, handle = vrep.simxGetObjectHandle(clientID, nomeSensor[i], vrep.simx_opmode_oneshot_wait)

		if(res != vrep.simx_return_ok):
			print (nomeSensor[i] + " nao conectado")
		else:
			print (nomeSensor[i] + " conectado")
			sensorHandle.append(handle)

#------------------------------Inicializa Motores ----------------------------
	resLeft, leftMotorHandle = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_leftMotor", vrep.simx_opmode_oneshot_wait)
	if(resLeft != vrep.simx_return_ok):
		print("Motor Esquerdo : Handle nao encontrado!")
	else:
		print("Motor Esquerdo: Conectado")

	resRight, rightMotorHandle = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_rightMotor", vrep.simx_opmode_oneshot_wait)
	if(resRight != vrep.simx_return_ok):
		print("Motor Direito: Handle nao encontrado!")
	else:
		print("Motor Direito: Conectado")
else:
	print ("Servidor nao conectado!")

#-----------------Inicializa localizacao------------------
localizacao = localization.localizacao()
localization.iniciar(clientID)
blending = blending.blending()

#model = load_model('Redes/MLP_I.h5')# create the original model
#slp_model = Model(inputs=model.input, outputs=model.output)
#layer = slp_model.get_layer(name=None, index=1)
#print layer.get_weights()

global padrao, posInicial
padrao = raw_input('Qual Padrao de ambiente o robo sera inserido? ')
posInicial = raw_input('Qual a posicao inicial do robo? ')

global model

model = []
model.append(load_model('Redes/SLP_A.h5'))
model.append(load_model('Redes/SLP_B.h5'))
model.append(load_model('Redes/SLP_C.h5'))
model.append(load_model('Redes/SLP_D.h5'))
model.append(load_model('Redes/SLP_E.h5'))
model.append(load_model('Redes/SLP_F.h5'))
model.append(load_model('Redes/SLP_G.h5'))
model.append(load_model('Redes/SLP_H.h5'))
model.append(load_model('Redes/SLP_I.h5'))
model.append(load_model('Redes/SLP_A.h5'))


def calcula_saida(pesos_blending, entradas):
    global model
    indice2rede = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'H']
    saida = 0
    output = 0
    filtro = 1
    entrada_rede = []

    for i in range(len(pesos_blending)):
	
        #se há um peso, calcula o output
        if pesos_blending[i] != 0:
            #excecoes de entradas de algumas redes
            if indice2rede[i] == 'A':
                entrada_rede.append(entradas[8])
            elif indice2rede[i] == 'C':
                filtro = 0.3
                for j in range(len(entradas)):
                    if j != 1 and j != 6:
                        entrada_rede.append(entrada[j])
            elif indice2rede[i] == 'F':
                filtro = 0.4
            elif indice2rede[i] == 'G':
                for j in range(len(entradas)):
                    if j != 2 and j != 5:
                        entrada_rede.append(entrada[j])
            else:
                for entrada in entradas:
                    entrada_rede.append(entrada)
	     
            slp_model = Model(inputs=model[i].input, outputs=model[i].output)    
            output = slp_model.predict(np.array([entrada_rede]), batch_size=1, verbose=0, steps=None)
            #print "Saida da rede ", indice2rede[i]," = ", math.degrees(output*math.pi)
            #print "Filtro = ", filtro
            if (abs(math.degrees(output*math.pi)) > filtro):
                saida = saida + output

            filtro = 1
    return saida

def virar(angulo):
	thetaInicial = localizacao.getOrientacao()
	#print thetaInicial
	if(angulo > 0):
		#motorDir.rotate((int) (ang * (DISTANCIA_RODAS / RAIO_RODA)));
		v_Left = -0.5
		v_Right = 0.5
		while(abs(thetaInicial - localizacao.getOrientacao()) < abs(angulo)):
			vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, v_Right, vrep.simx_opmode_streaming)
			vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, v_Left, vrep.simx_opmode_streaming)

			thetaDir = vrep.simxGetJointPosition(clientID, rightMotorHandle, vrep.simx_opmode_streaming)[1]
			thetaEsq = vrep.simxGetJointPosition(clientID, leftMotorHandle, vrep.simx_opmode_streaming)[1]

			localizacao.setAngulos(thetaDir, thetaEsq)
	else:
		v_Left = 0.5
		v_Right = -0.5
		while(abs(thetaInicial - localizacao.getOrientacao()) < abs(angulo)):
			vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, v_Right, vrep.simx_opmode_streaming)
			vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, v_Left, vrep.simx_opmode_streaming)

			thetaDir = vrep.simxGetJointPosition(clientID, rightMotorHandle, vrep.simx_opmode_streaming)[1]
			thetaEsq = vrep.simxGetJointPosition(clientID, leftMotorHandle, vrep.simx_opmode_streaming)[1]

			localizacao.setAngulos(thetaDir, thetaEsq)

def getThetaAlvo(thetaRobo, xRobo, yRobo):
	xAlvo = 0
	yAlvo = 0
	tolerancia = 0.5

	if padrao == 'A':
	# ------------- Posicao1 --------------
		if posInicial == '1':
			xAlvo = 7.3
			yAlvo = 0.8

		# ------------- Posicao2 --------------
		elif posInicial == '2':
			xAlvo = 5.4
			yAlvo = -0.5
		# ------------- Posicao3 --------------
		elif posInicial == '3':
			xAlvo = 6.8
			yAlvo = 2.5
		# ------------- Posicao4 --------------
		elif posInicial == '4':
			xAlvo = 2.8
			yAlvo = 2.2

		# ------------- Posicao5 --------------
		elif posInicial == '5':
			xAlvo = 7.2
			yAlvo = -1.6

		# ------------- Posicao6 --------------
		elif posInicial == '6':
			xAlvo = 2.0
			yAlvo = -2.3

	elif padrao == 'B':
		if posInicial == '1':
			xAlvo = 7.1
			yAlvo = 0.0
	elif padrao == 'C':
		if posInicial == '1':
			xAlvo = 7.6
			yAlvo = 0.78
	elif padrao == 'D':
		if posInicial == '1':
			xAlvo = 0.74
			yAlvo = 3.5
	elif padrao == 'E':
		if posInicial == '1':
			xAlvo = 0.6
			yAlvo = -3.2
	elif padrao == 'F':
		if posInicial == '1':
			xAlvo = 2.5
			yAlvo = 5.6
	elif padrao == 'G':
		if posInicial == '1':
			xAlvo = 6.0
			yAlvo = -2.3
	elif padrao == 'H':
		if posInicial == '1':
			xAlvo = 2.5
			yAlvo = 0.0
	elif padrao == 'I':
		if posInicial == '1':
			xAlvo = 4.9
			yAlvo = 0.0

	if(xAlvo > xRobo):
		thetaAlvo =  - thetaRobo + math.atan((yAlvo - yRobo)/(xAlvo - xRobo))
	else:
		if(yAlvo > yRobo):
			thetaAlvo = -thetaRobo + math.pi + math.atan((yAlvo - yRobo)/(xAlvo - xRobo))
		else:
			thetaAlvo = -thetaRobo - math.pi + math.atan((yAlvo - yRobo)/(xAlvo - xRobo))

	#thetaAlvo = math.atan((yAlvo - yRobo)/(xAlvo - xRobo))


	if (abs(xRobo - xAlvo) < tolerancia) and (abs(yRobo - yAlvo) < tolerancia):
		thetaAlvo = 0
	return thetaAlvo

leituras = []
saidas = []
inicio = time.time()
clearance = 0
#---------------------------Loop principal ---------------------------------------
while vrep.simxGetConnectionId(clientID) != -1:

	#seta velocidade nos motores
	vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, v_Right, vrep.simx_opmode_streaming)
	vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, v_Left, vrep.simx_opmode_streaming)

	thetaDir = vrep.simxGetJointPosition(clientID, rightMotorHandle, vrep.simx_opmode_streaming)[1]
	thetaEsq = vrep.simxGetJointPosition(clientID, leftMotorHandle, vrep.simx_opmode_streaming)[1]
	localizacao.setAngulos(thetaDir, thetaEsq)

	path_lenght = localizacao.getPathLenght() #atributo Lng

	#Lê sensores
	for i in range(0,8):
		returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, sensorHandle[i], vrep.simx_opmode_streaming)
		if (returnCode == vrep.simx_return_ok):
			if(detectionState != 0):
				dist.append(detectedPoint[2])
			else:
				dist.append(5.0)
		#print math.degrees(thetaRobo-getThetaAlvo(thetaRobo, xRobo, yRobo))
		time.sleep(0.01)


	thetaRobo = localizacao.getOrientacao()
	xRobo, yRobo = localizacao.getPosicao()

	if(len(dist) == 8):
		entradas = []
		#for da PARAMETRIZACAO
		for n in range(len(dist)):
			dist[n] = dist[n]/5.0
			#if n == 2 or n == 5 or n == 7:
			entradas.append(dist[n])
			if(dist[n] <= 0.01):
				colisao = True

		#if min(dist) < 0.05:
		#	clearance = clearance + 1.0 - min(dist)/(sum(dist)/len(dist))

		blending.setLeituras(entradas)
		padrao_blending = blending.definePadrao()
		pesos_blending = blending.calculaPesos(padrao_blending)

		thetaAlvo = getThetaAlvo(thetaRobo, xRobo, yRobo)
		#print math.degrees(thetaAlvo)
		if(thetaAlvo == 0.0):
		    v_Left = 0.0
		    v_Right = 0.0
		    atingiu = True
		    #print "clr: ", clearance
		    #print "oscilacoes: ", oscilacoes
		else:
		    v_Left = 0.5
		    v_Right = 0.5

		entradas.append(thetaAlvo/(math.pi))
		#print "x: "+str(xRobo)+" y: "+str(yRobo)+" ThetaRobo: "+str(thetaRobo)
		print "ThetaAlvo: "+str(math.degrees(thetaAlvo))

		output = calcula_saida(pesos_blending, entradas)
		saidas.append(output)
		#if abs(math.degrees(output*math.pi)) > 1:
		virar(output*math.pi)

		if len(saidas) > 2:
			if (saidas[len(saidas)-1] > 0 and saidas[len(saidas)-2] < 0 and saidas[len(saidas)-3] > 0) or (saidas[len(saidas)-1] < 0 and saidas[len(saidas)-2] > 0 and saidas[len(saidas)-3] < 0):
				oscilacoes = oscilacoes+1

		print "Saida: ", math.degrees(output*math.pi)

		if ((time.time() - inicio) > 200) and not atingiu:
			#v_Left = 0.0
			#v_Right = 0.0
			print "TIMEOUT"

        #--------------RETORNAR VALORES PRO EP----------------
	dist=[]
