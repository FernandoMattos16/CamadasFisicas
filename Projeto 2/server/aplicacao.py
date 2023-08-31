from enlace import *
import time
import numpy as np
import time

# Voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal:
#   python -m serial.tools.list_ports
# Se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411"  # Mac    (variacao de)
serialName = "COM3"                    # Windows(variacao de)

def main():
    try:
        com1 = enlace(serialName)

        com1.enable()

        timei = time.time()
    
        while time.time() - timei < 5:

            print("Esperando 1 byte de sacrifício")        
            rxBuffer, nRx = com1.getData(1)
            com1.rx.clearBuffer()
            time.sleep(.5)

            print("Comunicação aberta com sucesso!\n")
        
            print("Iniciando recepção\n")

            RxLen = 0
            while RxLen == 0:
                time.sleep(.5)
                RxLen = com1.rx.getBufferLen()
            
            print("Tamanho recebido: {}".format(RxLen))
            rxBuffer, nRx = com1.getData(RxLen)
            print(rxBuffer)
            l = 0
            for b in rxBuffer:
                if b == 204:
                    l += 1

            print(l)

            print("Rececebeu {} bytes\n".format(len(rxBuffer)))
            print("-------------------------------")

            print("Enviando quantidade de pacotes recebidos para o client\n")
            com1.sendData(bytearray(int(l)))
            print("Tamanho do arquivo enviado")

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

