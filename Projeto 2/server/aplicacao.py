#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
from enlaceRx import *
import time
import numpy as np
import secrets
import random

# Voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# Use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        # Declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        # Enviando byte de sacrifício
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
        print("Iniciando a recepção")

        N, t = com1.getData(2)
        NInt = int.from_bytes(N, "big")
        print(N)
        print(f"Serão recebidos {NInt} pacotes de comando")

        x = 0  
        while x < NInt:
            # Recebendo o tamanho do pacote
            rxBufferHeader, rxHeaderLen = com1.getData(2)

            # Transformando o tamanho do pacote em um inteiro
            rxBufferResponse = int.from_bytes(rxBufferHeader, "big")

            # Recebendo o pacote
            rxBuffer, rxBufferLen = com1.getData(rxBufferResponse)

            x += 1

        print("Pacotes recebidos!\n")

        # Retornando quantidade de pacotes recebidos para o client
        print("Enviando a quantidade de pacotes recebidos ao client para confirmação\n")
        com1.sendData(N)
        #z = 5
        # = z.to_bytes(2, byteorder="big")
        #com1.sendData(y)
            
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()