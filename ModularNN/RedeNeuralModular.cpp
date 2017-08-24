#include "RedeNeuralModular.h"
#include "Modulo.cpp"
using namespace std;

RedeNeuralModular::RedeNeuralModular(){
    modulo1 = new Modulo(padroes1);
    modulo[0] = modulo1;
    
    modulo2 = new Modulo(padroes2);
    modulo[1] = modulo2;
    
    modulo3 = new Modulo(padroes3);
    modulo[2] = modulo3;
    
    modulo4 = new Modulo(padroes4);
    modulo[3] = modulo4;
    
    modulo5 = new Modulo(padroes5);
    modulo[4] = modulo5;
    
    modulo6 = new Modulo(padroes6);
    modulo[5] = modulo6;
    
    modulo7 = new Modulo(padroes7);
    modulo[6] = modulo7;
    
    modulo8 = new Modulo(padroes8);
    modulo[7] = modulo8;
    
    modulo9 = new Modulo(padroes9);
    modulo[8] = modulo9;
    calculaDAvg();
}

float RedeNeuralModular::calculaDAvg(){
    davg = 0;
    
    for(int i = 0; i < NUM_MODULOS; i++){
        for(int j = 0; j < NUM_MODULOS; j++){
            davg += distanciaEuclidiana(modulo[i]->getPadrao(), modulo[j]->getPadrao(), NUM_SENSORES);
        }   
    }
    
    davg = davg/(NUM_MODULOS*NUM_MODULOS);
    threshold = davg/2.0;
    return davg;
}

float RedeNeuralModular::getThreshold(){
    return threshold;
}

int RedeNeuralModular::definePadrao(){
    padraoEncontrado = false;
    int padrao = 0;
    float menorDist = 1000;
    
    for(int i = 0; i < NUM_MODULOS; i++){
            distancias[i] = distanciaEuclidiana(modulo[i]->getPadrao(), leituras, NUM_SENSORES);
          //  cout << "Distancia " << i+1 << ": " << distancias[i] << endl;

    }
    
    
    for(int i = 0; i < NUM_MODULOS; i++){
        if(distancias[i] < menorDist){
            padrao = i+1;
            menorDist = distancias[i];
        }
    }
    
    if(menorDist < threshold){
           padraoEncontrado = true;
    } else {
            padraoEncontrado = false;
            padrao = -1;
    }
    
    return padrao;
}

string RedeNeuralModular::padraoAlfaNumerico(int padrao){
    string padraoAlfa;
       switch(padrao){
                case 1:
                    padraoAlfa = "A";
                break;	  
                case 2:
                    padraoAlfa = "B";
                break;
                case 3:
                    padraoAlfa = "C";
                break;
                case 4:
                    padraoAlfa = "D";
                break;
                case 5:
                    padraoAlfa = "E";
                break;
                case 6:
                    padraoAlfa = "F";
                break;
                case 7:
                    padraoAlfa = "G";
                break;
                case 8:
                    padraoAlfa = "H";
                break;
                case 9:
                    padraoAlfa = "I";
                break;
        }
    return padraoAlfa;
}

float RedeNeuralModular::distanciaEuclidiana(float * vetor1, float * vetor2, int size){
    float sum = 0;
    for(int i = 0; i < size; i++){
        sum += pow((vetor1[i]-vetor2[i]),2);
    }
    
    return sqrt(sum);
}


void RedeNeuralModular::setLeituras(float * leituras){
    this->leituras[0] = leituras[0];
    this->leituras[1] = leituras[1];
    this->leituras[2] = leituras[2];
    this->leituras[3] = leituras[3];
    this->leituras[4] = leituras[4];
    this->leituras[5] = leituras[5];
    this->leituras[6] = leituras[6];
    this->leituras[7] = leituras[7];
}

float * RedeNeuralModular::calculaPesos(int padrao){
    float sum = 0;
    if(padrao == -1){
        for(int i = 0; i < NUM_MODULOS; i++){
            sum += pow(davg-distancias[i],2);
        }
        for (int i = 0; i < NUM_MODULOS; i++){
            pesos[i] = pow(davg-distancias[i],2)/sum;
        }
    } else {
        for (int i = 0; i < NUM_MODULOS; i++){
            pesos[i] = 0;
        }
        pesos[padrao-1] = 1;
    }
    return pesos;
}
