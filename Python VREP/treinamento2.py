# -*- coding: utf-8 -*-
import vrep
import time
import localization
import math
import thread
import os.path
from pynput import keyboard

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
raio = 0.195/2

	
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

global padrao, virando
padrao = raw_input('Qual Padrao de ambiente sera treinado? ')
#numTreinamento = raw_input('Qual o numero do treinamento? ')
virando = False

#-----------------Inicializa localizacao------------------
localizacao = localization.localizacao()
localization.iniciar(clientID)

#---------------------Seta velocidades nos motores-----------------------
vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, v_Right, vrep.simx_opmode_streaming)
vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, v_Left, vrep.simx_opmode_streaming)

thetaDir = vrep.simxGetJointPosition(clientID, rightMotorHandle, vrep.simx_opmode_streaming)[1]
thetaEsq = vrep.simxGetJointPosition(clientID, leftMotorHandle, vrep.simx_opmode_streaming)[1]
localizacao.setAngulos(thetaDir, thetaEsq)


#----------------------Thread do teclado---------------------------------------------
def listen_keyboard():
	# Collect events until released
	with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: 
		listener.join()

def on_press(key):
	global virando
	virando = True
	#try:
	if key == keyboard.Key.left:
		velEsq = -0.5
		velDir = 0.5
	elif key == keyboard.Key.right:
		velEsq = 0.5
		velDir = -0.5
	elif key == keyboard.Key.space:
		velEsq = 0
		velDir = 0
	elif key == keyboard.Key.esc:
		# Stop listener
		sys.exit(0)
		return False
	else:
		velEsq = 0
		velDir = 0
	vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, velDir, vrep.simx_opmode_streaming)
	vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, velEsq, vrep.simx_opmode_streaming)

	thetaDir = vrep.simxGetJointPosition(clientID, rightMotorHandle, vrep.simx_opmode_streaming)[1]
	thetaEsq = vrep.simxGetJointPosition(clientID, leftMotorHandle, vrep.simx_opmode_streaming)[1]
	localizacao.setAngulos(thetaDir, thetaEsq)



def on_release(key):
	global virando
	virando = False
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
		#xAlvo = 7.3
                #yAlvo = 0.8        
                
                # ------------- Posicao2 --------------
                #xAlvo = 5.4
                #yAlvo = -0.5  
                
                # ------------- Posicao3 --------------
                #xAlvo = 6.8
                #yAlvo = 2.5
                
                # ------------- Posicao4 --------------
                #xAlvo = 2.8
                #yAlvo = 2.2
                
                # ------------- Posicao5 --------------
                #xAlvo = 7.2
                #yAlvo = -1.6
                
                # ------------- Posicao6 --------------
                xAlvo = 2.0
                yAlvo = -2.3
                                
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
	

thread.start_new_thread(listen_keyboard,())
thetaRoboAnt = 0
lista_entradas = []
lista_saidas = []
#---------------------------Loop principal ---------------------------------------
while vrep.simxGetConnectionId(clientID) != -1:
	thetaDir = vrep.simxGetJointPosition(clientID, rightMotorHandle, vrep.simx_opmode_streaming)[1]
	thetaEsq = vrep.simxGetJointPosition(clientID, leftMotorHandle, vrep.simx_opmode_streaming)[1]

	localizacao.setAngulos(thetaDir, thetaEsq)
	
	#----------------------------lê os sensores---------------------------------
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
	
	if(len(dist)==8 and not virando):
		#for da PARAMETRIZACAO
		for n in range(len(dist)):
			dist[n] = dist[n]/5.0
		
		thetaAlvo = getThetaAlvo(thetaRobo, xRobo, yRobo)
		entradas = str(dist[0])+", "+str(dist[1])+", "+str(dist[2])+", "+str(dist[3])+", "+str(dist[4])+", "+str(dist[5])+", "+str(dist[6])+", "+str(dist[7])+", "+str(thetaAlvo/2*math.pi)
		
		saida = str((thetaRobo-thetaRoboAnt)/(2*math.pi))
		
		lista_entradas.append(entradas)
		lista_saidas.append(saida)
		
		print "x: "+str(xRobo)+" y: "+str(yRobo)+" ThetaRobo: "+str(thetaRobo)
		print "ThetaAlvo: "+str(math.degrees(thetaAlvo))
		thetaRoboAnt = thetaRobo
	dist=[]
	
raw_input("Aperte ENTER para salvar o treinamento ou CTRL+C para Cancelar")
nome_diretorio = 'Padrao'+padrao
nome_arquivo_entrada = 'Entrada'+padrao+'.txt'
nome_arquivo_saida = 'Saida'+padrao+'.txt'						

for i in range(len(lista_entradas)):
	#verifica se ja existe o diretorio
	if os.path.isdir(nome_diretorio): 
			#grava entradas no txt 
			if os.path.isfile(nome_diretorio+'/'+nome_arquivo_entrada):
				arquivo = open(nome_diretorio+'/'+nome_arquivo_entrada, 'a+')		
				arquivo.write(lista_entradas[i]+'\n')
				arquivo.close()
			else:
				arquivo = open(nome_diretorio+'/'+nome_arquivo_entrada, 'w+')		
				arquivo.write(lista_entradas[i]+'\n')
				arquivo.close()
		
		
			#grava saidas no txt 
			if os.path.isfile(nome_diretorio+'/'+nome_arquivo_saida):
				arquivo = open(nome_diretorio+'/'+nome_arquivo_saida, 'a+')		
				arquivo.write(lista_saidas[i]+'\n')
				arquivo.close()
			else:
				arquivo = open(nome_diretorio+'/'+nome_arquivo_saida, 'w+')		
				arquivo.write(lista_saidas[i]+'\n')
				arquivo.close()
	else:
		os.mkdir(nome_diretorio)	
		
print "Treinamento salvo com sucesso!"
