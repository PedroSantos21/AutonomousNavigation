#include "RedeNeuralModular.h"
#include "Modulo.cpp"
using namespace std;

RedeNeuralModular::RedeNeuralModular(){
    modulo1 = new Modulo(padroes1);
    modulo2 = new Modulo(padroes2);
    modulo3 = new Modulo(padroes3);
    modulo4 = new Modulo(padroes4);
    modulo5 = new Modulo(padroes5);
    modulo6 = new Modulo(padroes6);
    modulo7 = new Modulo(padroes7);
    modulo8 = new Modulo(padroes8);
    modulo9 = new Modulo(padroes9);
}


int RedeNeuralModular::definePadrao(){
    int padrao = 1;
    float menorDist = distanciaEuclidiana(modulo1->getPadrao(), leituras);
        
    if(distanciaEuclidiana(modulo2->getPadrao(), leituras) < menorDist)
        padrao = 2;
    if(distanciaEuclidiana(modulo3->getPadrao(), leituras) < menorDist)
        padrao = 3;
    if(distanciaEuclidiana(modulo4->getPadrao(), leituras) < menorDist)
        padrao = 4;
    if(distanciaEuclidiana(modulo5->getPadrao(), leituras) < menorDist)
        padrao = 5;
    if(distanciaEuclidiana(modulo6->getPadrao(), leituras) < menorDist)
        padrao = 6;
    if(distanciaEuclidiana(modulo7->getPadrao(), leituras) < menorDist)
        padrao = 7;
    if(distanciaEuclidiana(modulo8->getPadrao(), leituras) < menorDist)
        padrao = 8;
    if(distanciaEuclidiana(modulo9->getPadrao(), leituras) < menorDist)
        padrao = 9;
    
    return padrao;
}

float RedeNeuralModular::distanciaEuclidiana(float * vetor1, float * vetor2){
    float sum = 0;
    for(int i = 0; i < sizeof(vetor1)/sizeof(float); i++){
        sum += pow((vetor1-vetor2),2);
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
