import vrep
import time
serverIP = "127.0.0.1"
serverPort = 19999
#---------------------Conecta no servidor---------------------------------
clientID = vrep.simxStart(serverIP, serverPort, True, True, 2000, 5)
nomeSensor = []
sensorHandle = []
dist = []
leftMotorHandle = 0
rightMotorHandle = 0

if (clientID!=-1):
	print ("Servidor Conectado!")

#------------------------------Inicializa Sensores ----------------------------
	for i in range(0,8):
		nomeSensor.append("sensor" + str(i+1))

		res, handle = vrep.simxGetObjectHandle(clientID, nomeSensor[i], vrep.simx_opmode_oneshot_wait)

		if(res != vrep.simx_return_ok):
			print (nomeSensor[i] + " nao conectado")
		else:
			#vrep.simxReadProximitySensor(clientID,sensorHandle, None, None, None, None, vrep.simx_opmode_streaming)
			print (nomeSensor[i] + " conectado")
			sensorHandle.append(handle)
#------------------------------Inicializa Motores ----------------------------
	resLeft, handleLeft = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_leftMotor", vrep.simx_opmode_oneshot_wait)
	if(resLeft != vrep.simx_return_ok):
		print("Handle do motor esquerdo nao encontrado!")
	else:
		print("Conectado ao motor esquerdo!")
	resRight, handleRight = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_rightMotor", vrep.simx_opmode_oneshot_wait)
	if(resRight != vrep.simx_return_ok):
		print("Handle do motor direito nao encontrado!")
	else:
		print("Conectado ao motor direito!")
else:
	print ("Servidor nao conectado!")


#---------------------------Loop principal ---------------------------------------
while vrep.simxGetConnectionId(clientID) != -1:
	for i in range(0,8):
		returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, sensorHandle[i], vrep.simx_opmode_streaming)
		if (returnCode == vrep.simx_return_ok):
			if(detectionState != 0):
				dist.append(detectedPoint[2])
			else:
				dist.append(5.0)
			print(dist[i])
		else:
			print ("Error on sensor "+str(i+1))
		time.sleep(0.1)
