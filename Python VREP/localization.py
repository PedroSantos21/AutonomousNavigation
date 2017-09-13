import math
from threading import Thread
import time
import vrep
global thetaDir, thetaEsq, thetaDirAnt, thetaEsqAnt, xpos, ypos, theta, Dr, Dl

class localizacao(Thread):
	def __init__ (self):
		Thread.__init__(self)
		global thetaDir, thetaEsq, thetaDirAnt, thetaEsqAnt, xpos, ypos, theta, Dr, Dl
		thetaDir = 0 
		thetaEsq = 0 
		thetaDirAnt = thetaDir
		thetaEsqAnt = thetaEsq
		xpos = 0
		ypos = 0
		theta = 0
		Dr = 0
		Dl = 0
		
		self.largura = 0.415
		self.raio = 0.195/2
		self.intervalo = 10.0/1000.0

	def setAngulos (self, thetaD, thetaE):
		global thetaDir, thetaEsq
		thetaDir = thetaD
		thetaEsq = thetaE
		#print str(thetaDir)+", "+str(thetaEsq)
		#print "Novas velocidades: "+str(self.velDir)+" "+str(self.velEsq)

	def update(self):
		global thetaDir, thetaEsq, thetaDirAnt, thetaEsqAnt, xpos, ypos, theta, Dr, Dl
		
		dThetaDir = thetaDir-thetaDirAnt
		dThetaEsq = thetaEsq - thetaEsqAnt
		print str(dThetaDir)+" "+str(dThetaEsq)
		Dr = (thetaDir-thetaDirAnt)*self.raio
		Dl = (thetaEsq-thetaEsqAnt)*self.raio		
		Dc = (Dl+Dr)/2
		
		#print str(Dr)+","+str(Dl)
		
		xpos = xpos+Dc*math.cos(theta)		
		ypos = ypos+Dc*math.sin(theta)
		theta = theta + (Dr-Dl)/self.largura
		
		thetaDirAnt = thetaDir
		thetaEsqAnt = thetaEsq

		
	def run(self):
		while vrep.simxGetConnectionId(clientID) != -1:
			self.update()
			#print "theta = "+str(math.degrees(theta))+" x = "+str(xpos)+" y= "+str(ypos)
			time.sleep(self.intervalo)


def iniciar(ID):
	global clientID
	clientID = ID
	thread = localizacao()
	thread.start()
