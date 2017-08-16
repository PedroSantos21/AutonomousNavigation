#ifndef CINEMATICA_H
#define CINEMATICA_H

#include <math.h>
#include <stdio.h>  
#include <stdlib.h> 
#include <cmath>       
#include <iostream>
#include <thread>
#define INTERVALO 50
class Cinematica {

private:  
  float xpos;
  float ypos;
  float theta;
  float largura;
  float velDir;
  float velEsq;
  
public:
  Cinematica(float);
  void update();  
  void setVelocidades(float, float);
  float radians(float);
  float degrees(float);
  float getTheta();   
  float getX();
  float getY();     
  void run();
};

#endif
