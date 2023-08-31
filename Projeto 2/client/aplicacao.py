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
    send_list.append(command)
    send_list.append(b'\xcc')
    time.sleep(.05)

# Voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# Se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)

def main():
    try:
        print("Main iniciada")
        com1 = enlace(serialName)
    
        com1.enable()

        # Enviando byte de sacrifício
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)

        txBuffer = np.array(send_list)

        print("Comunicação aberta com sucesso!")
        
        print(f"Serão enviados {N} pacotes de comandos\n")
        
        com1.sendData(bytearray(txBuffer))
            
        print("Pacotes enviados!\n")  

        print("Esperando confirmação da quantidade de pacotes recebidos pelo server...\n")

        RxLen = 0
        timeout = time.time() + 5

        while RxLen == 0:
            if time.time() > timeout:
                break
            time.sleep(.5)
            RxLen = com1.rx.getBufferLen()

        if RxLen == N:
            print("Tamanho Recebido: {}".format(RxLen))
            print("Quantidade de pacotes recebidos é IGUAL a enviada. SUCESSO!")
        elif RxLen != 0:
            print("Tamanho Recebido: {}".format(RxLen))
            print("Quantidade de pacotes recebidos é DIVERGENTE da enviada. FALHA!")
        else:
            print("Time Out: mensagem de confirmação não recebida!") 

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

if __name__ == "__main__":
    main()