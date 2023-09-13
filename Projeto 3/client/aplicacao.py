from enlace import *
import time
import sys
import math



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
        com1 = enlace(serialName)
    
        com1.enable()

        print("Comunicação aberta com sucesso!\n")
        
        # Handshake
        while True:
            # Enviando byte de sacrifício
            print("Enviando Handshake")
            time.sleep(.2)
            com1.sendData(b'00')
            print(". . . Aguardando retorno para inicio de transmissão . . .\n")
            rxBuffer, nRx = com1.getData(2)
            if rxBuffer == 'S' or rxBuffer == 's':
                print("\n. . . Reiniciando tentativa de transmissão . . .\n")
                continue
            if rxBuffer == 'N' or rxBuffer == 'n':
                print("\nTentativa de transmissão interrompida\n. . . Encerrando comunicação . . .\n")
                com1.disable()
                sys.exit("Comunicação encerrada")
            else:
                com1.rx.clearBuffer()
                time.sleep(1)
                print("Handshake confirmado!\n. . . Iniciando transmissão . . .\n")
                break
         
        pathImageTx = "Projeto 3/img/logo-insper.jpeg"
        ImageTx = open(pathImageTx, 'rb').read()
        print(ImageTx)

        lenImage = len(ImageTx)
        nPacotes = math.ceil(lenImage/50)
        nPacotesBytes = nPacotes.to_bytes(2, byteorder="big")

        print(f"Serão enviados {nPacotes} pacotes!\n")
        com1.sendData(nPacotesBytes)
        time.sleep(1)

        payloads = [ImageTx[i:i + 50] for i in range(0, len(ImageTx), 50)]

        contPacotes = 0
        while contPacotes < nPacotes:
            print(f"Enviando o {contPacotes+1}º pacote")
            # HEAD
            nPacote = (contPacotes+1).to_bytes(6, byteorder="big") # Número do pacote
            tamPayload = (len(payloads[contPacotes])).to_bytes(6, byteorder="big") # Tamanho do pacote
            HEAD = nPacote + tamPayload
            # PAYLOAD
            PAYLOAD = payloads[contPacotes] # Pacote
            # EOP
            EOP = b'0'
            
            tamanhoPacote = (len(HEAD + PAYLOAD + EOP)).to_bytes(2,byteorder="big")
            com1.sendData(tamanhoPacote)
            time.sleep(1)
            com1.sendData(HEAD + PAYLOAD + EOP)
            time.sleep(1)

            # Recebendo confirmação se o pacote foi enviado corretamente
            confirmacao, confrimacaoLen = com1.getData(1)

            if confirmacao == b'2':
                pacoteCerto, pacoteCertoLen = com1.getData(2)
                contPacotes = int.from_bytes(pacoteCerto, "big") - 1
                print(f"Inconsistência no EOP! Reenviando {contPacotes+1}º pacote\n")

            elif confirmacao == b'1':
                pacoteCerto, pacoteCertoLen = com1.getData(2)
                contPacotes = int.from_bytes(pacoteCerto, "big") - 1
                print(f"A sequência do pacote está incorreta! Reenviando {contPacotes+1}º pacote\n")

            else:
                contPacotes += 1
        
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