#ifndef REDENEURALMODULAR_H
#define REDENEURALMODULAR_H
#include "Modulo.h"

#define NUM_MODULOS 9 
#define NUM_SENSORES 8
class RedeNeuralModular{
    
private:
    float leituras[NUM_SENSORES];
    
    float padroes1[NUM_SENSORES] = {1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000};
    float padroes2[NUM_SENSORES] = {0.1490, 0.1923, 0.3017, 0.7409, 0.7360, 0.2475, 0.1574, 0.1216};
    float padroes3[NUM_SENSORES] = {0.0401, 0.0540, 0.0957, 0.2928, 0.5619, 0.0979, 0.0556, 0.0405};                            
    float padroes4[NUM_SENSORES] = {0.0533, 0.0709, 0.1211, 0.3608, 0.5584, 0.6299, 0.4920, 0.3873};
    float padroes5[NUM_SENSORES] = {0.5578, 0.7116, 0.6337, 0.5647, 0.2460, 0.0820, 0.0454, 0.0327};
    float padroes6[NUM_SENSORES] = {0.0534, 0.2330, 0.3011, 0.3213, 0.3228, 0.3609, 0.2754, 0.2172};
    float padroes7[NUM_SENSORES] = {0.2244, 0.2917, 0.3518, 0.3134, 0.3154, 0.2722, 0.3010, 0.0573};
    float padroes8[NUM_SENSORES] = {1.0000, 1.0000, 0.8589, 0.1315, 0.1315, 0.8632, 1.0000, 1.0000};
    float padroes9[NUM_SENSORES] = {0.0497, 0.0508, 0.0367, 0.0291, 0.0291, 0.0368, 0.0391, 0.0316};
    
    Modulo *modulo1;
    Modulo *modulo2;
    Modulo *modulo3;
    Modulo *modulo4;
    Modulo *modulo5;
    Modulo *modulo6;
    Modulo *modulo7;
    Modulo *modulo8;
    Modulo *modulo9;
    
    float distanciaEuclidiana(float *, float *);

public:
    RedeNeuralModular();
    int definePadrao();
    void setLeituras(float *);

};

#endif

