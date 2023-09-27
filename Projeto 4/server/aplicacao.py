from enlace import *
import time
from datetime import datetime
from datetime import datetime
import sys



def createLog(data, tipo):
    tempo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    tipoMsg = data[0]
    tamMsg = len(data)
    pacoteEnviado = data[4]
    totalPacotes = data[3]
    logs = f"{tempo} / {tipo} / {tipoMsg} / {tamMsg} / {pacoteEnviado} / {totalPacotes}\n"
    return logs
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
        logs = ''

        com1.enable()

        print("Comunicação aberta com sucesso!\n")

        

        # HANDSHAKE
        print(". . . Esperando Handshake . . .\n")

        pacote, lenPacote = com1.getDataHandshake(15)

        print(pacote)

        logs += createLog(pacote, 'recebimento')

        pacote = list(pacote)
        pacote = list(map(int, pacote))
        pacote[0] = 2
        responseHandShake = b''
        for i in pacote:
            i = (i).to_bytes(1, byteorder="big")
            responseHandShake += i

        pacote = responseHandShake

        print("Handshake recebido com sucesso!\n")

        logs += createLog(pacote, 'envio')
        com1.sendData(pacote)
        time.sleep(.5)
        com1.clearBuffer()

        print("Iniciando envio dos pacotes\n")

        #time.sleep(23)
        # Recebendo Pacotes
        data = b''
        numPacote = 1
        timeMax = time.time()
        while True:
            timeF = time.time()
            if timeF - timeMax >= 20:
                pacote = list(pacote)
                pacote = list(map(int, pacote))
                pacote[0] = 5
                responseHandShake = b''
                for i in pacote:
                    i = (i).to_bytes(1, byteorder="big")
                    responseHandShake += i
                pacote = responseHandShake
                logs += createLog(pacote, 'envio')
                com1.sendData(pacote)
                print("\nPacote não recebido após 20 segundos!\n. . . Cancelando comunicação . . .\n")
                with open(f'Projeto 4/client/assets/log/log.txt', 'w') as f:
                    f.write(logs)
                com1.disable()
                sys.exit("Comunicação encerrada")
            else:
                print(f". . . Recebendo o {numPacote}º pacote . . .\n")
                #HEAD
                head, lenHead = com1.getDataServer(10)

                print(head)
                lenPayload = head[5]
                payload_EOP, lenPayload_EOP = com1.getDataServer(lenPayload + 4)


                pacote = head + payload_EOP

                logs += createLog(pacote, 'recebimento')
                head = pacote[0:10]
                h0 = head[0] # tipo de mensagem
                h1 = head[1] # livre
                h2 = head[2] # livre
                h3 = head[3] # número total de pacotes do arquivo
                h4 = head[4] # número do pacote sendo enviado
                h5 = head[5] # se tipo for handshake:id do arquivo; se tipo for dados: tamanho do payload
                h6 = head[6] # pacote solicitado para recomeço quando a erro no envio.
                h7 = head[7] # último pacote recebido com sucesso.
                h8 = head[8] # CRC
                h9 = head[9] # CRC

                numPacoteRecebido = h4

                print(numPacote)
                print(h0)
                print(pacote)
                print()

                if h0 == 5:
                    logs += createLog(pacote, 'recebimento')
                    print("Time-out de client registrado!\n. . . Cancelando comunicação . . .\n")
                    with open(f'Projeto 4/client/assets/log/log.txt', 'w') as f:
                        f.write(logs)
                    com1.disable()
                    sys.exit("Comunicação encerrada")

                # Checando se o número do pacote enviado está correto
                if h4 != numPacote:
                    print(f"O número do pacote está errado! Por favor reenvie o pacote {numPacote}")
                    h0 = 6
                    h7 = numPacote
                    confirmacao = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
                    responseCorrectMsg = b''
                    for i in confirmacao:
                        i = (i).to_bytes(1, byteorder="big")
                        responseCorrectMsg += i
                    com1.sendData(responseCorrectMsg + b'\x00' + 0x00000000.to_bytes(4, byteorder="big"))
                    time.sleep(.5)
                    

                # Checando se o EOP está no local correto
                eop = pacote[len(pacote)-4:len(pacote)+1]
                if eop != 0x00000000.to_bytes(4, byteorder="big"):
                    print(f"O eop está no local errado! Por favor reenvie o pacote {numPacote}")
                    break
                
            
                print("Está tudo certo com a mensagem! Vamos enviar uma mensagem de confirmação.")
                h0 = 4
                h7 = numPacote
                confirmacao = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
                responseCorrectMsg = b''
                for i in confirmacao:
                    i = (i).to_bytes(1, byteorder="big")
                    responseCorrectMsg += i
                com1.sendData(responseCorrectMsg + b'\x00' + 0x00000000.to_bytes(4, byteorder="big"))
                logs += createLog(responseCorrectMsg + b'\x00' + 0x00000000.to_bytes(4, byteorder="big"), 'envio')
                time.sleep(.5)
                
            
                if numPacote == numPacoteRecebido:
                    numPacote += 1
                    data += payload_EOP[0:len(payload_EOP) - 4]                

                    if numPacote == h3 + 1:
                        data += payload_EOP[0:len(payload_EOP) - 4]
                        break


        pathImageRx = "Projeto 4/server/assets/img/rxImage.png"
        f = open(pathImageRx, 'wb')
        f.write(data)
        f.close()

        with open(f"Projeto 4/server/assets/log/log.txt", 'w') as f:
            f.write(logs)
        # * FECHANDO CLIENT
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        exit()
        
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        exit()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()