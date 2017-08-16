// Habilite o server antes na simulação V-REP com o comando lua:
// simExtRemoteApiStart(portNumber) -- inicia servidor remoteAPI do V-REP

extern "C" {
  #include "remoteApi/extApi.h"
  #include "include/v_repConst.h"
  #include "remoteApi/extApiPlatform.h"
}

#include <iostream>
#include <fstream>
#include <string>
#include <ctime>
#include <stdlib.h>  
#include <time.h>
#include <string.h>
#include <stdio.h>
#include <thread> 
#include "Cinematica.cpp"

using namespace std;
int start_s=clock();
string serverIP = "127.0.0.1";
int serverPort = 19999;
int leftMotorHandle = 0;
float vLeft = 0;
int rightMotorHandle = 0;
float vRight = 0;
string sensorNome[8];
int sensorHandle[8];
double tempoAnterior = 0;
double tempoAtual = 0;

void exec(int clientID){
    float detect[8]={0,0,0,0,0,0,0,0};
    int stop_s=clock();
    

    Cinematica *cinematica = new Cinematica(0.415);
    thread thCinematica(&Cinematica::run, cinematica);

    //ofstream myfile; 
    //myfile.open("teste.txt");
    //  Loop principal
    
    vRight = 1;
    vLeft = 1;
    while(simxGetConnectionId(clientID)!=-1) // enquanto a simulação estiver ativa
    {     
        tempoAtual = (stop_s-start_s)/double(CLOCKS_PER_SEC)*1000;
        
        cinematica->setVelocidades(vRight, vLeft);
        
        simxSetJointTargetVelocity(clientID, leftMotorHandle, (simxFloat) vLeft, simx_opmode_streaming);
        simxSetJointTargetVelocity(clientID, rightMotorHandle, (simxFloat) vRight, simx_opmode_streaming);
        

        //if(tempoAtual-tempoAnterior > 10){ 
        for(int i = 0; i < 8; i++){
        // atualiza velocidades dos motores        
        simxUChar state;
        simxFloat coord[3];
       
           if(simxReadProximitySensor(clientID, sensorHandle[i] ,&state, coord,NULL,NULL,simx_opmode_buffer)==simx_return_ok){
                        
                        float dist = coord[2];
                        
                        if(state == 0){
                            dist = 5;
                        }
                        
                      if(dist < 0.1 ){
                            vRight = 1;
                            vLeft =  -1;
                      }
            }
                    tempoAnterior = tempoAtual;
        }
                            
    }
   thCinematica.join();
}

int main(int argc, char **argv){
  
  // variaveis de cena e movimentação do pioneer
//   float noDetectionDist=0.5;
//   float maxDetectionDist=0.2;
  
  
  int clientID=simxStart((simxChar*)serverIP.c_str(),serverPort,true,true,2000,5);
  
  if (clientID!=-1)
  {
     cout << "Servidor conectado!" << std::endl;
    
    // inicialização dos motores
    if(simxGetObjectHandle(clientID,(const simxChar*) "Pioneer_p3dx_leftMotor",(simxInt *) &leftMotorHandle, (simxInt) simx_opmode_oneshot_wait) != simx_return_ok)
      cout << "Handle do motor esquerdo nao encontrado!" << std::endl;  
    else
      cout << "Conectado ao motor esquerdo!" << std::endl;
    
    if(simxGetObjectHandle(clientID,(const simxChar*) "Pioneer_p3dx_rightMotor",(simxInt *) &rightMotorHandle, (simxInt) simx_opmode_oneshot_wait) != simx_return_ok)
      cout << "Handle do motor direito nao encontrado!" << std::endl;  
    else
      cout << "Conectado ao motor direito!" << std::endl;
    
    // inicialização dos sensores (remoteApi)
    for(int i = 0; i < 8; i++)
    {
      sensorNome[i] = "sensor" + to_string(i + 1);
      
      if(simxGetObjectHandle(clientID,(const simxChar*) sensorNome[i].c_str(),(simxInt *) &sensorHandle[i], (simxInt) simx_opmode_oneshot_wait) != simx_return_ok)
            cout << "Handle do sensor " << sensorNome[i] << " nao encontrado!" << std::endl;
      else
      {
        cout << "Conectado ao sensor " << sensorNome[i] << std::endl;
        simxReadProximitySensor(clientID,sensorHandle[i],NULL,NULL,NULL,NULL,simx_opmode_streaming);
      }
    }
    
    exec(clientID);
   // std::thread thMain(&exec, clientID);
    //thCinematica.join();
    
    
    //myfile.close();
    simxFinish(clientID); // fechando conexao com o servidor
    cout << "Conexao fechada!" << std::endl;    
  }
  else
    cout << "Problemas para conectar o servidor!" << std::endl;
  return 0;
}

