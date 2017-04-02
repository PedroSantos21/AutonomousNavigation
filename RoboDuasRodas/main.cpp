
// Habilite o server antes na simulação V-REP com o comando lua:
// simExtRemoteApiStart(portNumber) -- inicia servidor remoteAPI do V-REP

extern "C" {
  #include "remoteApi/extApi.h"
}

#include <iostream>
#include <string>

using namespace std;
int main(int argc, char **argv) 
{
  string serverIP = "127.0.0.1";
  int serverPort = 19999;
  int leftMotorHandle = 0;
  float vLeft = 0;
  int rightMotorHandle = 0;
  float vRight = 0;
  int sensorHandle;
  float v0=-2;
  
  int clientID=simxStart((simxChar*)serverIP.c_str(),serverPort,true,true,2000,5);
  
  if (clientID!=-1)
  {
    cout << "Servidor conectado!" << std::endl;
    
    // inicialização dos motores
    if(simxGetObjectHandle(clientID,(const simxChar*) "Left_Motor",(simxInt *) &leftMotorHandle, (simxInt) simx_opmode_oneshot_wait) == simx_return_ok)
      cout << "Conectado ao motor esquerdo!" << std::endl;
    else
      cout << "Handle do motor esquerdo nao encontrado!" << std::endl;  
      
    
    if(simxGetObjectHandle(clientID,(const simxChar*) "Right_Motor",(simxInt *) &rightMotorHandle, (simxInt) simx_opmode_oneshot_wait) == simx_return_ok)
      cout << "Conectado ao motor direito!" << std::endl;
    else
       cout << "Handle do motor direito nao encontrado!" << std::endl;  
      
   
      if(simxGetObjectHandle(clientID,(const simxChar*) "Proximity_sensor",(simxInt *) &sensorHandle, (simxInt) simx_opmode_oneshot_wait) == simx_return_ok){
        cout << "Conectado ao sensor "<< std::endl;
        simxReadProximitySensor(clientID,sensorHandle,NULL,NULL,NULL,NULL,simx_opmode_streaming);
      }else
          cout << "Handle do sensor nao encontrado!" << std::endl;
       
    // desvio e velocidade do robô
    while(simxGetConnectionId(clientID)!=-1) // enquanto a simulação estiver ativa
    {     
      vLeft = v0;
      vRight = v0;
      
      // atualiza velocidades dos motores

      simxSetJointTargetVelocity(clientID, leftMotorHandle, (simxFloat) vLeft, simx_opmode_streaming);
      simxSetJointTargetVelocity(clientID, rightMotorHandle, (simxFloat) vRight, simx_opmode_streaming);
       
       simxUChar state;
       simxFloat coord[3];
       
       if (simxReadProximitySensor(clientID,sensorHandle,&state,coord,NULL,NULL,simx_opmode_buffer)==simx_return_ok)
       {
            float dist = coord[2];
            printf("%f\n",dist);
            if(dist < 0.01 && dist > 0.0){
                 simxSetJointTargetVelocity(clientID, leftMotorHandle, 0.0, simx_opmode_streaming);
                 simxSetJointTargetVelocity(clientID, rightMotorHandle, 0.0, simx_opmode_streaming);
                
                 extApi_sleepMs(500);

                 simxSetJointTargetVelocity(clientID, leftMotorHandle, (simxFloat) vLeft, simx_opmode_streaming);
                 simxSetJointTargetVelocity(clientID, rightMotorHandle,(simxFloat) -vRight, simx_opmode_streaming);
                 extApi_sleepMs(500);
            }      
       }
    }
    simxFinish(clientID); // fechando conexao com o servidor
    cout << "Conexao fechada!" << std::endl;
  }
  else
    cout << "Problemas para conectar o servidor!" << std::endl;
  return 0;
}

