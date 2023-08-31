#####################################################
# Camada Física da Computação
#Carareto
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from tracemalloc import stop


from enlace import *
import time
import numpy as np

import time

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411"  # Mac    (variacao de)
serialName = "COM6"                    # Windows(variacao de)

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM6')
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        print("esperando 1 byte de sacrifício")        
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("COMUNICAÇÃO ABERTA COM SUCESSO\n")
       
        print("RECEPÇÃO VAI COMEÇAR\n")

        # Recebendo a quantidade de comandos que será enviado
        N, t = com1.getData(2)
        nCmdInt = int.from_bytes(N, "big")
        print(f"Serão recebidos {nCmdInt} pacotes de comandos\n")
        
        x = 0
        while x < nCmdInt:
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

