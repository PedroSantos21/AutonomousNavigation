import vrep
import time
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
global v_Left, v_Right
v_Left = 1
v_Right = 1

def on_press(key):
    try:
        #print('alphanumeric key {0} pressed'.format(key.char))
	"""
        if key == keyboard.Key.up:
        	v_Left = 1
		v_Right = 1
	elif key == keyboard.Key.down:
        	v_Left = -1
		v_Right = -1
	"""
	if key == keyboard.Key.left:
        	v_Left = -0.5
		v_Right = 0.5
	elif key == keyboard.Key.right:
        	v_Left = 0.5
		v_Right = -0.5		
	elif key == keyboard.Key.esc:
		# Stop listener
		return False	
	vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, v_Right, vrep.simx_opmode_streaming)
	vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, v_Left, vrep.simx_opmode_streaming)
        
    except AttributeError:
        print('special key {0} pressed'.format(key))
        
def on_release(key):
	vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, 1, vrep.simx_opmode_streaming)
	vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, 1, vrep.simx_opmode_streaming)
        
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

vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, v_Right, vrep.simx_opmode_streaming)
vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, v_Left, vrep.simx_opmode_streaming)
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

	
	# Collect events until released
	with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
	    listener.join()


