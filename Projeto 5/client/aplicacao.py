from enlace import *
import time
import sys
import math
from datetime import datetime
from crccheck.crc import Crc16



def createLog(data, tipo):
    tempo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    tipoMsg = data[0]
    tamMsg = len(data)
    pacoteEnviado = data[4]
    totalPacotes = data[3]
    log = f"{tempo} / {tipo} / {tipoMsg} / {tamMsg} / {pacoteEnviado} / {totalPacotes}\n"
    return log

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
        logs = ''

        # * INICIALIZANDO CLIENT
        com1 = enlace(serialName)
        com1.enable()

        print("Comunicação aberta com sucesso!\n")

        print("Enviando Handshake\n")

        # * HANDSHAKE
        timeMax = time.time()
        while True:
            payload, h1, h2, h3, h4, h5, h6, h7, h8, h9 = b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00'
            h0 = (1).to_bytes(1, byteorder="big")
            head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
            eop = 0x00000000.to_bytes(4, byteorder="big")
            pacote = head + payload + eop
            logs += createLog(pacote, 'envio')
            com1.sendData(pacote)
            print(". . . Aguardando retorno válido para inicio de transmissão . . .")
            time.sleep(.5)
            confirmacao, lenConfimacao = com1.getData(15)
            timeF = time.time()
            if timeF - timeMax >= 20:
                print("\nServidor não respondeu após quarta tentativa.\n. . . Cancelando comunicação . . .\n")
                payload, h1, h2, h3, h4, h5, h6, h7, h8, h9 = b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00'
                h0 = (1).to_bytes(1, byteorder="big")
                head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
                eop = 0x00000000.to_bytes(4, byteorder="big")
                pacote = head + payload + eop
                com1.sendData(pacote)
                (". . . Aguardando retorno para inicio de transmissão . . .")
                logs += createLog(pacote, 'envio')
                with open(f'Projeto 5/client/assets/log/log.txt', 'w') as f:
                    f.write(logs)
                com1.disable()
                sys.exit("Comunicação encerrada")
            elif confirmacao[0] == 2:
                logs += createLog(confirmacao, 'recebimento')
                com1.rx.clearBuffer()
                time.sleep(1)
                print("Handshake confirmado!\n. . . Iniciando transmissão . . .\n")
                break
            else:
                print("Retorno nulo ou inválido\n")
                continue
                
        # * ENVIO DOS PACOTES
        print("Agora vamos realizar o início do envio dos pacotes")

        #time.sleep(25)

        path = "Projeto 5/client/assets/img/logo-insper.jpeg"  
        file = open(path, 'rb').read()
        payloads = [file[i:i + 114] for i in range(0, len(file), 114)]
        
        # h3 = quantidade total de pacotes
        lenImage = len(file)
        h3 = math.ceil(lenImage/114)
        h3 = (h3).to_bytes(1, byteorder="big")
        # h4 = número do pacote sendo enviado
        h4 = 1
        # último pacote enviado com sucesso
        cont = 0
        timeMax = time.time()
        while cont < int.from_bytes(h3, "big"):
            print(f"\n. . . Enviando informações do pacote {h4} . . .")
            h7 = (h4-1).to_bytes(1, byteorder="big")
            h4 = (h4).to_bytes(1, byteorder="big")
            h0 = (3).to_bytes(1, byteorder="big")
            h5 = len(payloads[int.from_bytes(h4,"big")-1])
            h5 = (h5).to_bytes(1, byteorder="big")

            data = payloads[int.from_bytes(h4,"big") - 1]
            if int.from_bytes(h4,"big") - 1 == 2:
                data = payloads[1]
            crc1, crc2 = Crc16.calc(data).to_bytes(2,byteorder='big')
            h8 = crc1.to_bytes(1,byteorder='big')
            h9 = crc2.to_bytes(1,byteorder='big')

            head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
            pacote = head + payloads[int.from_bytes(h4, "big") - 1] + eop

            com1.sendData(pacote)
            logs += createLog(pacote, 'envio')
            time.sleep(.5)
            print("Pacote enviado com sucesso!\n. . . Aguardando resposta de recebimento . . .")
            numPacoteCorreto = None

            timeF = time.time()
            if timeF - timeMax >= 20:
                h0 = (5).to_bytes(1, byteorder="big")
                head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
                pacote = head + payloads[int.from_bytes(h4, "big") - 1] + eop
                logs += createLog(pacote, 'envio')
                com1.sendData(pacote)
                print("\nNenhuma resposta do servidor após 20 segundos!\n. . . Cancelando comunicação . . .")
                with open(f'Projeto 5/client/assets/log/log.txt', 'w') as f:
                    f.write(logs)
                com1.disable()
                sys.exit("Comunicação encerrada")
            
            confirmacao, lenConfimacao = com1.getData(15)
            if type(confirmacao[0]) != int:
                h4 = int.from_bytes(h4, "big")
                print("Servidor inativo! Vamos tentar reenviar o pacote.")
                continue
            elif confirmacao[0] < 4:
                h4 = int.from_bytes(h4, "big")
                logs += createLog(confirmacao, 'recebimento')
                numPacoteCorreto = h4
                print(f"Erro no envio :(\n . . . Reenviando o {numPacoteCorreto}º pacote . . .\n")
            else:
                h4 = int.from_bytes(h4, "big")
                if confirmacao[0] == 4:
                    logs += createLog(confirmacao, 'recebimento')
                    #print(confirmacao[7])
                    print("Pacote recebido com sucesso!")
                elif confirmacao[0] == 5:
                    logs += createLog(confirmacao, 'recebimento')
                    print("Time-out de servidor registrado!\n. . . Cancelando comunicação . . .\n")
                    with open(f'Projeto 5/client/assets/log/log.txt', 'w') as f:
                        f.write(logs)
                    com1.disable()
                    sys.exit("Comunicação encerrada")
                else:
                    logs += createLog(confirmacao, 'recebimento')
                    numPacoteCorreto = confirmacao[7]
                    print(f"Erro no envio :(\n . . . Reenviando o {numPacoteCorreto}º pacote . . .")
                
                if numPacoteCorreto is None:
                    h4 += 1
                    cont += 1
                else:
                    h4 = numPacoteCorreto
                    cont = numPacoteCorreto - 1

        with open(f'Projeto 5/client/assets/log/log.txt', 'w') as f:
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
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()