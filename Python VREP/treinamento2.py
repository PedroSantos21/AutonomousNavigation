import vrep
import time
import localization
import math
import thread
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
v_Left = 0
v_Right = 0
raio = 0.195/2

def listen_keyboard():
	# Collect events until released
	with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: 
		listener.join()

def on_press(key):
    try:
	if key == keyboard.Key.left:
		velEsq = -0.3
		velDir = 0.3
	elif key == keyboard.Key.right:
		velEsq = 0.3
		velDir = -0.3
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

#---------------------Seta velocidades nos motores-----------------------
vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, v_Right, vrep.simx_opmode_streaming)
vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, v_Left, vrep.simx_opmode_streaming)

thetaDir = vrep.simxGetJointPosition(clientID, rightMotorHandle, vrep.simx_opmode_streaming)[1]
thetaEsq = vrep.simxGetJointPosition(clientID, leftMotorHandle, vrep.simx_opmode_streaming)[1]

localizacao.setAngulos(thetaDir, thetaEsq)


#---------------------------Loop principal ---------------------------------------
while vrep.simxGetConnectionId(clientID) != -1:
	for i in range(0,8):
		returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, sensorHandle[i], vrep.simx_opmode_streaming)
		if (returnCode == vrep.simx_return_ok):
			if(detectionState != 0):
				dist.append(detectedPoint[2])
			else:
				dist.append(5.0)
			#print(dist[i])
		#else:
			#print ("Error on sensor "+str(i+1))
		time.sleep(0.1)
	
	thread.start_new_thread(listen_keyboard,())
