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
		thetaEsq = 2*math.pi
		thetaDirAnt = 0
		thetaEsqAnt = 2*math.pi
		xpos = 0
		ypos = 0
		theta = 0
		Dr = 0
		Dl = 0
		self.largura = 0.415-0.08
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

		thetaDir = round(thetaDir, 3)
		thetaEsq = round(thetaEsq, 3)
		
		
		#print "TetaD: "+str(thetaDir)+"TetaE: "+str(thetaEsq)
		
		thetaDir = (thetaDir+2*math.pi)%(2*math.pi)
		thetaEsq = (thetaEsq+2*math.pi)%(2*math.pi)
	
		dThetaDir = thetaDir - thetaDirAnt
		dThetaEsq = thetaEsq - thetaEsqAnt
			
		if(abs(dThetaDir) > 1):
			dThetaDir = 0
		if(abs(dThetaEsq) > 1):
			dThetaEsq = 0
			
		#print "DTetaD: "+str(dThetaDir)+" DTetaE: "+str(dThetaEsq)
		
		Dr = dThetaDir*self.raio
		Dl = dThetaEsq*self.raio		
		Dc = (Dl+Dr)/2
		
		#print "Dr: "+str(Dr)+"Dl: "+str(Dl)
		
		xpos = xpos+Dc*math.cos(theta)		
		ypos = ypos+Dc*math.sin(theta)
		theta = theta + (Dr-Dl)/self.largura
		
		
		thetaDirAnt = thetaDir
		thetaEsqAnt = thetaEsq

		
	def run(self):
		while vrep.simxGetConnectionId(clientID) != -1:
			self.update()
			print "theta = "+str(math.degrees(theta))+" x = "+str(xpos)+" y= "+str(ypos)
			time.sleep(self.intervalo)


def iniciar(ID):
	global clientID
	clientID = ID
	thread = localizacao()
	thread.start()
