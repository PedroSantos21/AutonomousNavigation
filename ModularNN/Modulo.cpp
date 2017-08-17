#include "Modulo.h"
using namespace std;

Modulo::Modulo(float *padroes){
  
    for(int i = 0; i < NUM_SENSORES; i++){
        this->padroes[i] = padroes[i];
        
    }
}

float * Modulo::getPadrao(){
    
    return this->padroes;
}
    
    

    
    
