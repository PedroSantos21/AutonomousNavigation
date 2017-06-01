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

using namespace std;

int main(int argc, char **argv) 
{
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
  // variaveis de cena e movimentação do pioneer
//   float noDetectionDist=0.5;
//   float maxDetectionDist=0.2;
  float detect[8]={0,0,0,0,0,0,0,0};
  float v0=0;
  bool fimDeLinha = false;
  
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
    

    ofstream myfile; 
    myfile.open("teste.txt");
    //  Loop principal
    while(simxGetConnectionId(clientID)!=-1) // enquanto a simulação estiver ativa
    {     
        int stop_s=clock();
        tempoAtual = (stop_s-start_s)/double(CLOCKS_PER_SEC)*1000;
        vLeft = v0;
        vRight = v0;
        
        
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
                                 
                        if(myfile.is_open()){
                                if(dist < 0){
                                    myfile << 0 << ";";    
                                    cout << 0 << " ";                                            
                                }
                                else{
                                    myfile << dist <<";";    
                                    cout << dist << " ";                                            
                                }
                        }
                        
                        
                            if(i+1 == 8){
                                fimDeLinha = true;
                               printf("\n");
                                myfile <<""<<endl;    
                            } else {
                                fimDeLinha = false;
                            }
                        
                    /*   if(dist < 0.1 ){
                            simxSetJointTargetVelocity(clientID, leftMotorHandle, 0.0, simx_opmode_streaming);
                            simxSetJointTargetVelocity(clientID, rightMotorHandle, 0.0, simx_opmode_streaming);
                            
                            extApi_sleepMs(500);
                            
                            simxSetJointTargetVelocity(clientID, leftMotorHandle,  (simxFloat) -vLeft, simx_opmode_streaming);
                            simxSetJointTargetVelocity(clientID, rightMotorHandle, (simxFloat) -vRight, simx_opmode_streaming);
                            
                            extApi_sleepMs(500);

                            simxSetJointTargetVelocity(clientID, leftMotorHandle, (simxFloat) vLeft, simx_opmode_streaming);
                            simxSetJointTargetVelocity(clientID, rightMotorHandle,(simxFloat) -vRight, simx_opmode_streaming);
                            extApi_sleepMs(250);
                        }   */   
                    //} 
            }
                    tempoAnterior = tempoAtual;
        }
    
        
            /*    int stop_s=clock();
                tempoAtual = (stop_s-start_s)/double(CLOCKS_PER_SEC)*1000;
                int sort = rand()%100+1;
                
                if(sort > 85 && (tempoAtual-tempoAnterior)>1000){
                    
                    simxFloat posx = rand() % 20 + 1;
                    sort = rand()%100+1;
                     if(sort > 50)
                         posx = posx*-1;
                    
                    
                    simxFloat posy = rand() % 20 + 1;
                    sort = rand()%100+1;
                     if(sort > 50)
                         posy = posy*-1;
                    
                    
                    simxLoadModel(clientID,pathdoBloco, 1 , NULL, simx_opmode_blocking);                 
                   
                    simxChar nome[80];
                    
                    strcpy (nome,"ConcretBlock");
                    if(temBloco){
                        simxChar numero[32];
                        strcat (nome,"#");
                        sprintf(numero, "%d", blockCounter);
                        strcat (nome, numero);
                        blockCounter++;
                    }
                  
                    
                    if(simxGetObjectHandle(clientID,(const simxChar*) nome,(simxInt *) &objectHandle, (simxInt) simx_opmode_oneshot_wait) == simx_return_ok){ 
                            cout << "Bloco adicionado" << " "<< nome << std::endl;
                              temBloco = true;
                    }
                    else
                            cout << "Handle do bloco não detectado" << std::endl;  
                    
                    simxSetModelProperty(clientID, objectHandle, sim_modelproperty_not_respondable,simx_opmode_oneshot);
                    simxFloat pos[] = {posx/10, posy/10,0.3};
                    cout<< "x: "<< posx/10 << " y: " << posy/10 << std::endl;
                    simxSetObjectPosition(clientID, objectHandle, -1, pos, simx_opmode_oneshot); 


                    tempoAnterior = tempoAtual;
                }*/
                        
    }
    myfile.close();
    simxFinish(clientID); // fechando conexao com o servidor
    cout << "Conexao fechada!" << std::endl;
  }
  else
    cout << "Problemas para conectar o servidor!" << std::endl;
  return 0;
}
