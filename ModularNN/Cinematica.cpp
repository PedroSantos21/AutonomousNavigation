#include "Cinematica.h"
using namespace std;
Cinematica::Cinematica(float largura){
    this->largura = largura;
    this->xpos = 0;
    this->ypos = 0;
    this->theta = 0;
}

/*float dWTheta = (vr - vl)/largura;
    theta += degrees(dWTheta*intervalo/1000.0);
    if (abs(theta) > 360)
      theta = abs(theta)-360;

    float dVX = (vr + vl)*cos(radians(theta))/2;
    xpos += dVX*intervalo/1000.0;

    float dVY = (vr + vl)*sin(radians(theta))/2;
    ypos += dVY*intervalo/1000.0;
 */

void Cinematica::update(){
    
    float dTheta = ((velDir - velEsq)/largura)*INTERVALO/1000.0;
    theta += degrees(dTheta);

    if(abs(theta) > 360)
        theta = abs(theta)-360;
    

    float dX = ((velDir + velEsq)*cos(radians(theta))/2)*INTERVALO/1000.0;
    xpos += dX;
    
    float dY = ((velDir + velEsq)*sin(radians(theta))/2)*INTERVALO/1000.0;
    ypos += dY;
    
    /*cout << "x: " << xpos;
    cout << " y: " << ypos;
    cout << " theta: " << theta << endl;*/
    this_thread::sleep_for(chrono::milliseconds(INTERVALO));
}

  void Cinematica::setVelocidades(float velDir, float velEsq){
   this->velDir = velDir;
   this->velEsq = velEsq;
  }

  float Cinematica::radians(float angle){
      return angle*(M_PI/180);
  }
  
  float Cinematica::degrees(float angle){
      return angle*(180/M_PI);
  }
    
  float Cinematica::getTheta(){
    return this->theta;
  }
  
  float Cinematica::getX(){
    return this->xpos;
  }
  
  float Cinematica::getY(){
    return this->ypos;
  } 
  void Cinematica::run(){
      while(true)
          update();
  }
