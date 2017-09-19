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

global padrao
padrao = raw_input('Qual Padrao de ambiente sera treinado? ')
numTreinamento = raw_input('Qual o numero do treinamento? ')

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
    try:
	if key == keyboard.Key.left:
		velEsq = -0.5
		velDir = 0.5
	elif key == keyboard.Key.right:
		velEsq = 0.5
		velDir = -0.5
	elif key == keyboard.Key.esc:
		# Stop listener
		sys.exit(0)
		return False
	vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, velDir, vrep.simx_opmode_streaming)
	vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, velEsq, vrep.simx_opmode_streaming)

	thetaDir = vrep.simxGetJointPosition(clientID, rightMotorHandle, vrep.simx_opmode_streaming)[1]
	thetaEsq = vrep.simxGetJointPosition(clientID, leftMotorHandle, vrep.simx_opmode_streaming)[1]
    	localizacao.setAngulos(thetaDir, thetaEsq)

    except AttributeError:
	print('special key {0} pressed'.format(key))

def on_release(key):
	vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, v_Right, vrep.simx_opmode_streaming)
	vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, v_Left, vrep.simx_opmode_streaming)

	thetaDir = vrep.simxGetJointPosition(clientID, rightMotorHandle, vrep.simx_opmode_streaming)[1]
	thetaEsq = vrep.simxGetJointPosition(clientID, leftMotorHandle, vrep.simx_opmode_streaming)[1]

	localizacao.setAngulos(thetaDir, thetaEsq)

def getThetaAlvo(thetaRobo, xRobo, yRobo):
	'''
		Padrao F - xAlvo = 2.5
			   yAlvo = 5.6
		
		Padrao G - xAlvo = 6
			   yAlvo = -2.3	
	'''
	xAlvo = 0
        yAlvo = 0
	if padrao == 'F':
		xAlvo = 2.5
		yAlvo = 5.6	
	elif padrao == 'G':
		xAlvo = 6
                yAlvo = -2.3	
		
	thetaAlvo = thetaRobo - math.atan((yAlvo - yRobo)/(xAlvo - xRobo))
	
	if (abs(xRobo - xAlvo) < 0.5) and (abs(yRobo - yAlvo) < 0.5):
		thetaAlvo = 0
		
	return thetaAlvo
	

thread.start_new_thread(listen_keyboard,())
thetaRoboAnt = 0
#---------------------------Loop principal ---------------------------------------
while vrep.simxGetConnectionId(clientID) != -1:
	thetaDir = vrep.simxGetJointPosition(clientID, rightMotorHandle, vrep.simx_opmode_streaming)[1]
	thetaEsq = vrep.simxGetJointPosition(clientID, leftMotorHandle, vrep.simx_opmode_streaming)[1]

	localizacao.setAngulos(thetaDir, thetaEsq)
	
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
		entradas = str(dist[0])+", "+str(dist[1])+", "+str(dist[2])+", "+str(dist[3])+", "+str(dist[4])+", "+str(dist[5])+", "+str(dist[6])+", "+str(dist[7])+", "+str(getThetaAlvo(thetaRobo, xRobo, yRobo))
		saida = str(thetaRobo-thetaRoboAnt)
			   
		nome_diretorio = 'Padrao'+padrao
		nome_arquivo = 'Treinamento'+str(numTreinamento)+'.txt'			
		#verifica se ja existe o diretorio
		if os.path.isdir(nome_diretorio): 
				#grava dados no txt 
				if os.path.isfile(nome_diretorio+'/'+nome_arquivo):
					arquivo = open(nome_diretorio+'/'+nome_arquivo, 'a+')		
					arquivo.write(entradas+", "+saida+'\n')
					arquivo.close()
				else:
					arquivo = open(nome_diretorio+'/'+nome_arquivo, 'w+')		
					arquivo.write(entradas+", "+saida+'\n')
					arquivo.close()
		else:
			os.mkdir(nome_diretorio)
		print "x: "+str(xRobo)+" y: "+str(yRobo)+" ThetaRobo: "+str(thetaRobo)
		print "ThetaAlvo: "+str(math.degrees(getThetaAlvo(thetaRobo, xRobo, yRobo)))
		thetaRoboAnt = thetaRobo
	dist=[]
	
