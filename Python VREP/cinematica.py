import math
import time
import vrep
from threading import Thread

global velDir, velEsq, xpos, ypos, theta

class localizacao(Thread):
	def __init__ (self):
		Thread.__init__(self)
		global velDir, velEsq, xpos, ypos, theta
		velDir = 0 		#rad/s
		velEsq = 0		#rad/s
		xpos = 0 		#m
		ypos = 0 		#m
		theta = 0 		#graus
		self.largura = 0.415	#m
		self.raio = 0.19502/2 	#m
		self.dt = 1.0/1000.0 	#s

		
	def setVelocidades (self, velD, velE):
		global velDir, velEsq
		velDir = velD
		velEsq = velE
		#print "Novas velocidades: "+str(self.velDir)+" "+str(self.velEsq)

	def update(self):
		global velDir, velEsq, xpos, ypos, theta
		#print str(velDir) +" "+ str(velEsq)
		
		dX = ((velDir + velEsq)*(self.raio/2)*math.cos(math.radians(theta)))
		xpos = xpos + dX*self.dt

		dY = ((velDir + velEsq)*(self.raio/2)*math.sin(math.radians(theta)))
		ypos = ypos + dY*self.dt

		dTheta = (velDir - velEsq)*self.raio/self.largura
		theta = theta + math.degrees(dTheta)*self.dt

		if(abs(theta) > 360):
			theta = abs(theta)-360

	
		
	def run(self):
		while vrep.simxGetConnectionId(clientID) != -1:
			self.update()
			#print "theta = "+str(theta)+" x = "+str(xpos)+" y= "+str(ypos)
			time.sleep(self.dt)


def iniciar(ID):
	global clientID
	clientID = ID
	thread = localizacao()
	thread.start()
