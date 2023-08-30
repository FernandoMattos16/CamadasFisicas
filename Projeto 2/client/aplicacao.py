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


c1 = b'\x00\x00\x00\x00'
c2 = b'\x00\x00\xBB\x00'
c3 = b'\xBB\x00\x00'
c4 = b'\x00\xBB\x00'
c5 = b'\x00\x00\xBB'
c6 = b'\x00\xAA'
c7 = b'\xBB\x00'
c8 = b'\x00' 
c9 = b'\xBB'

c_list = [c1, c2, c3, c4, c5, c6, c7, c8, c9]

send_list = []

N = random.randint(10,30)

txBuffer = b''

for i in range(N):
    command = secrets.choice(c_list)
    txBuffer += command
    send_list.append(command)
    time.sleep(.05)

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

        # Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
                    
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        print(f"Serão enviados {N} pacotes de comandos\n")
        packN = N.to_bytes(2, byteorder="big")
        com1.sendData(packN)
        time.sleep(.05)
        
        for i in send_list:
            # Tamanho do pacote a ser enviado
            txBufferLen = len(i)

            # Pacote a ser enviado 
            txBuffer = i        

            # Transformando o tamanho do pacote a ser enviado em bytes
            txBufferHeader = txBufferLen.to_bytes(2, byteorder="big") 

            # Enviando o tamanho do pacote em bytes
            com1.sendData(txBufferHeader)

            time.sleep(.05)

            # Enviando o pacote
            com1.sendData(txBuffer)

            time.sleep(.05)
            
        print("Pacotes enviados!\n")  

        print("Esperando confirmação da quantidade de pacotes recebidos pelo server...\n")
        try:
            nCmdConfirmacao, t = com1.getData(2)
            nCmdConfirmacaoInt = int.from_bytes(nCmdConfirmacao, "big") 

            if nCmdConfirmacaoInt == N:
                print("Quantidade de pacotes recebidos é IGUAL a enviada :)")
            else:
                print("Quantidade de pacotes recebidos é DIVERGENTE da enviada :(")  
        except:
            print("Time Out: mensagem de confirmação não recebida!")     

        
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