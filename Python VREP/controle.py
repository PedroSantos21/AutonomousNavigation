#coding: utf-8
import time
import vrep
import keras
import math
import localization
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
global v_Left, v_Right, tacoDir, tacoEsq
v_Left = 1
v_Right = 1

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

model =  load_model('Redes/SLP_A.h5')# create the original model
slp_model = Model(inputs=model.input, outputs=model.output)

global padrao
padrao = raw_input('Qual Padrao de ambiente o robo sera inserido? ')

def virar(angulo):
	thetaInicial = localizacao.getOrientacao()
	print thetaInicial
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
        tolerancia = 0.3       
        
        if padrao == 'A':
		xAlvo = 7.3
                yAlvo = 0.8        
        elif padrao == 'B':
		xAlvo = 7.1
                yAlvo = 0.0
        elif padrao == 'C':
		xAlvo = 7.6
                yAlvo = 0.78
	elif padrao == 'D':
        	xAlvo = 0.74
		yAlvo = 3.5
        elif padrao == 'E':
		xAlvo = 0.8
		yAlvo = -3.6	        
	elif padrao == 'F':
		xAlvo = 2.5
		yAlvo = 5.6	
	elif padrao == 'G':
		xAlvo = 6.0
                yAlvo = -2.3	
	elif padrao == 'H':
		xAlvo = 3.58
                yAlvo = 0.2
        elif padrao == 'I':
		xAlvo = 7.85
                yAlvo = 1.79
	  
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


#---------------------------Loop principal ---------------------------------------
while vrep.simxGetConnectionId(clientID) != -1:
	#seta velocidade nos motores
	v_Left = 1
	v_Right = 1
	vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, v_Right, vrep.simx_opmode_streaming)
	vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, v_Left, vrep.simx_opmode_streaming)

	thetaDir = vrep.simxGetJointPosition(clientID, rightMotorHandle, vrep.simx_opmode_streaming)[1]
	thetaEsq = vrep.simxGetJointPosition(clientID, leftMotorHandle, vrep.simx_opmode_streaming)[1]
	
	localizacao.setAngulos(thetaDir, thetaEsq)

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
	
	if(len(dist)==8):
		entradas = []
		#for da PARAMETRIZACAO
		for n in range(len(dist)):
			dist[n] = dist[n]/5.0
			entradas.append(dist[n])
		
		thetaAlvo = getThetaAlvo(thetaRobo, xRobo, yRobo)
		entradas.append(thetaAlvo/(2*math.pi))
		
		#print "x: "+str(xRobo)+" y: "+str(yRobo)+" ThetaRobo: "+str(thetaRobo)
		#print "ThetaAlvo: "+str(math.degrees(thetaAlvo))
		
		output = slp_model.predict(np.array([entradas]), batch_size=1, verbose=0, steps=None)
		virar(output*math.pi*2)
		print math.degrees(output*2*math.pi)
	dist=[]
