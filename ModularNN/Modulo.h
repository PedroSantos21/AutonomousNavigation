#ifndef MODULO_H
#define MODULO_H

#include <math.h>
#include <stdio.h>  
#include <stdlib.h> 
#include <cmath>       
#include <iostream>

#define NUM_SENSORES 8

class Modulo {

private:  
  float padroes[NUM_SENSORES];
  
public:
  Modulo(float*);
  float * getPadrao();
    
};

#endif
