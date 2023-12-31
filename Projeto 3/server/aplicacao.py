from enlace import *
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

        print("Comunicação aberta com sucesso!\n")

        

        # HANDSHAKE
        print(". . . Esperando Handshake . . .\n")
        handShake, lenHS = com1.getData(2)
        print(". . . Enviando retorno . . .\n")
        com1.sendData(handShake)
        time.sleep(.05)
        print("Handshake enviado!\n")
        
        # Recebendo a quantidade de pacotes que serão enviados pelo client
        nPacotesBytes, nPacotesBytes_len = com1.getData(2)
        nPacotes = int.from_bytes(nPacotesBytes, "big")
        print(f"Pacotes a serem enviados: {nPacotes}\n")

        contPacotes = 0
        ImageRx = b'00'
    
        while contPacotes < nPacotes:
            print(f"Analisando o {contPacotes+1}º pacote")

            # Recebendo Tamanho do pacote
            pacoteBytes, pacoteLenBytes = com1.getData(2)
            tamanhoPacote = int.from_bytes(pacoteBytes, "big")

            # Recebendo pacote
            pacote, lenPacote = com1.getData(tamanhoPacote)
            # HEAD
            nPacote = int.from_bytes(pacote[0:6], "big")
            tamPayload = int.from_bytes(pacote[6:12], "big")
            # PAYLOAD
            PAYLOAD = pacote[12:tamPayload + 12]
            # EOP
            EOP = pacote[ len(pacote)-3  :   len(pacote)]      

            # Sem erros = b'0'
            semErro = b'0'
            # Erro de número do pacote = b'1'
            numErro = b'1'
            # Erro de EOP = b'2'
            eopErro = b'2'
            # Erro de PayLoad = b'3'
            payErro = b'3'

            if EOP != b'000':
                print(f"\nInconsistência no EOP. Por favor envie o {contPacotes+1}º pacote novamente\n")
                # Enviando código de erro
                com1.sendData(eopErro)
                time.sleep(3)
                # Enviando mensagem pedindo o reenvio do pacote correto
                pacoteCerto = (contPacotes+1).to_bytes(2, byteorder="big")
                com1.sendData(pacoteCerto)
                time.sleep(1)

            elif nPacote != contPacotes+1:
                print(f"\nA sequência do pacote está incorreta! Por favor envie o {contPacotes+1}º pacote novamente\n")
                # Enviando código de erro
                com1.sendData(numErro)
                time.sleep(1)
                # Enviando mensagem pedindo o reenvio do pacote correto
                pacoteCerto = (contPacotes+1).to_bytes(2, byteorder="big")
                com1.sendData(pacoteCerto)
                time.sleep(1)
            
            elif  tamPayload != len(PAYLOAD):
                print(f"\nInconsistência no tamanho do Payload!\n. . . Encerrando comunicação . . .\n")
                # Erro no tamanho do Payload
                com1.sendData(payErro)
                time.sleep(.5)
                break
                
            else:
                # Recebendo PAYLOAD
                ImageRx += PAYLOAD
                # Enviando confirmação de que está tudo certo com o pacote
                com1.sendData(b'0')
                time.sleep(1)
                contPacotes +=1

        pathImageRx = "Projeto 3/img/rxImage.png"
        #print(ImageRx[2:len(ImageRx)])
        f = open(pathImageRx, 'wb')
        f.write(ImageRx[2:len(ImageRx)+1])
        f.close()

        print("\n-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()


    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

if __name__ == "__main__":
    main()