#coding: utf-8
import time
import vrep
import keras
import math
import localization
import numpy as np
import thread
import keras.backend as K
from keras.models import Model
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from pynput import keyboard

def init():
	global clientID, nomeSensor, sensorHandle, dist, leftMotorHandle, rightMotorHandle, serverIP, serverPort
	serverIP = "127.0.0.1"
	serverPort = 19997
	#---------------------Conecta no servidor---------------------------------
	clientID = vrep.simxStart(serverIP, serverPort, True, True, 2000, 5)
	nomeSensor = []
	sensorHandle = []
	dist = []
	leftMotorHandle = 0
	rightMotorHandle = 0
	thread.start_new_thread(listen_keyboard,())

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

	#model =  load_model('Redes/SLP_D.h5')# create the original model
	#slp_model = Model(inputs=model.input, outputs=model.output)
	#layer = slp_model.get_layer(name=None, index=1)
	#print layer.get_weights()

def reset():
	global v_Left, v_Right, clientID
	v_Left = 0
	v_Right = 0
	if vrep.simxGetConnectionId(clientID) != -1:
		vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
		time.sleep(0.5)

def getPesosIniciais(rede):
	global slp_model
	if rede == 'A':
		model =  load_model('Redes/SLP_A.h5')

	elif rede == 'B':
		model =  load_model('Redes/SLP_B.h5')

	elif rede == 'C':
		model =  load_model('Redes/SLP_C.h5')

	elif rede == 'D':
		model =  load_model('Redes/SLP_D.h5')

	elif rede == 'E':
		model =  load_model('Redes/SLP_E.h5')

	elif rede == 'F':
		model =  load_model('Redes/SLP_F.h5')

	elif rede == 'G':
		model =  load_model('Redes/SLP_G.h5')

	elif rede == 'H':
		model =  load_model('Redes/SLP_H.h5')

	elif rede == 'I':
		model =  load_model('Redes/SLP_I.h5')

	slp_model = Model(inputs=model.input, outputs=model.output)
	layer = slp_model.get_layer(name=None, index=1)
	return layer.get_weights()

def generate_model(pesos):
	model = Sequential()
	model.add(Dense(units=1, activation='tanh', input_dim=9, use_bias=True, bias_initializer='zeros'))
	#sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
	#model.compile(loss='mean_squared_error', optimizer= sgd, metrics=['accuracy'])

	#layer = model.get_layer(name=None, index=1)
	model.set_weights(np.array([pesos]))

	return model

def getParametros(ambiente, posicao, pesos):
	global v_Left, v_Right, dist, colisao, oscilacoes, path_lenght, atingiu, clearance
	global padrao, posInicial, clientID, localizacao
	pesos_rede = []
	for i in range(len(pesos)):
		if(i < len(pesos)/2):
			continue
		pesos_rede.append(pesos[i])

	slp_model = generate_model(pesos_rede)
	if vrep.simxGetConnectionId(clientID) != -1:
		e = vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)
		#print "Start ", e
		time.sleep(0.5)
		#-----------------Inicializa localizacao------------------
		localizacao = localization.localizacao()
		localization.iniciar(clientID)
		v_Left = 1
		v_Right = 1
		colisao = False
		atingiu = False
		oscilacoes = 0
		clearance = 0

		padrao = ambiente
		posInicial = posicao
		#posRoboVrep = vrep.simxGetObjectPosition(clientID, handle_robo, -1, vrep.simx_opmode_streaming)[1]
		#posRoboVrep = [-1.7445, 1.2500, 0.1388]
		#print "POSICAO VREP: ", posRoboVrep
		leituras = []
		saidas = []
		inicio = time.time()
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

			if(len(dist)==8):
				entradas = []
				#for da PARAMETRIZACAO
				for n in range(len(dist)):
					dist[n] = dist[n]/5.0
					entradas.append(dist[n])
					if(dist[n] <= 0.01):
						colisao = True

				if min(dist) < 0.05:
					clearance = clearance + 1.0 - min(dist)/(sum(dist)/len(dist))

				thetaAlvo = getThetaAlvo(thetaRobo, xRobo, yRobo)
				#print math.degrees(thetaAlvo)
				if(thetaAlvo == 0.0):
					atingiu = True
					reset()
					return colisao, oscilacoes, path_lenght, atingiu, clearance

					#print "clr: ", clearance
					#print "oscilacoes: ", oscilacoes
					#--------------RETORNAR VALORES PRO EP----------------
				else:
					v_Left = 1
					v_Right = 1
				entradas.append(thetaAlvo/(math.pi))

				#print "x: "+str(xRobo)+" y: "+str(yRobo)+" ThetaRobo: "+str(thetaRobo)
				print "ThetaAlvo: "+str(math.degrees(thetaAlvo))

				output = slp_model.predict(np.array([entradas]), batch_size=1, verbose=0, steps=None)
				saidas.append(output)
				if abs(math.degrees(output*math.pi)) > 1:
					virar(output*math.pi)

				if len(saidas) > 2:
					if (saidas[len(saidas)-1] > 0 and saidas[len(saidas)-2] < 0 and saidas[len(saidas)-3] > 0) or (saidas[len(saidas)-1] < 0 and saidas[len(saidas)-2] > 0 and saidas[len(saidas)-3] < 0):
						oscilacoes = oscilacoes+1
				print "Saida: ", math.degrees(output*math.pi)

				if ((time.time() - inicio) > 60) and not atingiu:
					print "TIMEOUT"
					reset()
					return colisao, oscilacoes, path_lenght, atingiu, clearance
			dist=[]
	reset()
	return colisao, oscilacoes, path_lenght, atingiu, clearance

def virar(angulo):
	global v_Left, v_Right, localizacao
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
	global posInicial, padrao

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
			xAlvo = 0.8
			yAlvo = -3.6
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
			xAlvo = 3.58
			yAlvo = 0.2
	elif padrao == 'I':
		if posInicial == '1':
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

def listen_keyboard():
	with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
		listener.join()

def on_press(key):
	global clientID
	if key == keyboard.Key.esc:
		reset()
		vrep.simxFinish(clientID)
		#reset()

def on_release(key):
	global clientID
	if key == keyboard.Key.esc:
		reset()
		vrep.simxFinish(clientID)
