#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        #txBuffer = imagem em bytes!
        txBuffer = b'\x12\x13\xAA'  #isso é um array de bytes
       
        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
               
        
        com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
          
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar funcionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        txSize = com1.tx.getStatus()
        print('enviou = {}' .format(txSize))
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        txLen = len(txBuffer)
        rxBuffer, nRx = com1.getData(txLen)
        print("recebeu {} bytes" .format(len(rxBuffer)))
        
        for i in range(len(rxBuffer)):
            print("recebeu {}" .format(rxBuffer[i]))
        

            
    
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


### Resumo UART (Universal Asynchronous Receiver/Transmitter)

## Transmissão assíncrona:
'''
    A transmissão assíncrona na UART se refere ao método de comunicação serial em que os
dados são transmitidos sem um sinal de clock compartilhado entre o transmissor e o receptor.
Isso significa que não há uma referência de tempo fixa para quando os bits de dados são
enviados ou recebidos. Em vez disso, a comunicação é baseada em acordos prévios sobre a
taxa de transmissão (baud rate) e o formato dos frames de dados. Ambos os dispositivos
envolvidos devem operar na mesma taxa de transmissão para garantir a sincronização adequada.

Quais são as características da transmissão assíncrona na UART que a diferenciam da transmissão 
síncrona?
    As características distintivas da transmissão assíncrona na UART incluem:
-Ausência de Clock Compartilhado entre transmissor e receptor;
-Start Bit e Stop Bits;
-Dependência na Taxa de Transmissão (Baud Rate);
-Simplicidade, uma vez que não requer Clock Compartilhado (facilidade de implementação).

Por que a transmissão assíncrona é usada na UART e em que contextos é mais apropriada?
    É especialmente apropriada em contextos em que a sincronização precisa ser mantida sem a
necessidade de um sinal de clock constante. Alguns contextos apropriados incluem:
-Comunicação entre dispositivos com clocks independentes;
-Comunicação entre dispositivos que não requerem altas taxas de transmissão;
-Aplicações em que a simplicidade e a facilidade de configuração são prioritárias.
'''

## Start Bit:
'''
    O Start bit é o primeiro bit de um byte de dados transmitido pela UART. 
Ele tem uma função crucial na comunicação serial assíncrona, indicando o início de um novo
byte de dados. O Start bit é sempre de nível lógico "baixo" (0) e é seguido pelos bits de dados
e, opcionalmente, pelos bits de paridade e stop bits.

Qual é a finalidade do Start bit?
    O Start bit tem várias finalidades importantes:
-Indica o início de um novo byte de dados: Quando um receptor UART detecta um Start bit de
nível "baixo", ele sabe que um novo byte de dados está prestes a ser transmitido. Isso ajuda
a sincronizar o início da recepção de dados;
-Permite a sincronização: A transmissão UART é assíncrona, o que significa que não há um 
sinal de clock compartilhado para sincronizar a comunicação. O Start bit atua como uma 
referência de tempo para os dispositivos envolvidos, indicando quando os dados começam a ser 
transmitidos.

 Quantos Start bits são usados em uma transmissão UART típica?
    Na UART, normalmente, é usado apenas um Start bit para indicar o início de cada byte de dados. 
 No entanto, em alguns casos, é possível configurar a UART para usar dois Start bits, embora 
 isso seja menos comum. A maioria das configurações UART padrão utiliza um único Start bit.

Qual é a duração do Start bit?
    A duração do Start bit depende da taxa de transmissão (baud rate) configurada na UART. 
Ela é calculada como o inverso da taxa de transmissão. Por exemplo, se a taxa de transmissão 
for 9600 bps, a duração de um Start bit seria de aproximadamente 104 µs (microssegundos). 
O receptor UART usa essa duração para determinar quando começar a ler os bits de dados 
subsequentes.

Por que o Start bit é sempre de nível "baixo" (0)?
    O Start bit é sempre de nível "baixo" para criar um padrão distintivo que o receptor UART 
possa detectar facilmente. Se o Start bit fosse de nível "alto" (1), seria mais difícil para 
o receptor determinar com precisão o início de um novo byte de dados, pois os níveis "altos" 
podem ocorrer em outras partes do byte de dados.

'''

## TX:
'''
    "TX" é uma abreviação para "Transmit" (Transmissão). Na comunicação UART, "TX" refere-se 
à linha ou pino que é usada pelo dispositivo transmissor para enviar dados ao dispositivo 
receptor. Quando o dispositivo transmissor deseja enviar um byte de dados, ele coloca os bits 
de dados no nível de tensão adequado na linha "TX" para representar os bits de dados a serem 
transmitidos.

Como a linha "TX" é usada na comunicação UART?
    A linha "TX" é usada da seguinte forma na comunicação UART:
-Quando o dispositivo transmissor tem dados para enviar, ele coloca o Start bit na linha "TX" 
com um nível lógico "baixo" (0) para indicar o início da transmissão.
-Em seguida, o dispositivo transmissor envia os bits de dados na linha "TX", um por um, na 
ordem correta.
-Após o último bit de dados, um ou mais bits de parada (stop bits) são adicionados para indicar 
o fim da transmissão.
    A linha "TX" permanece em nível "alto" (1) durante os bits de parada.  Isso significa que, 
na ausência de uma transmissão ativa, a linha "TX" permanece em um estado ocioso ou em repouso.

Qual é a função principal da linha "TX" na comunicação UART?
    A função principal da linha "TX" na comunicação UART é transmitir dados do dispositivo 
transmissor para o dispositivo receptor de forma assíncrona. A linha "TX" é onde os bits de 
dados são enviados serialmente, com a sequência de bits de início, dados e bits de parada, 
conforme especificados pela configuração da UART.

O que acontece se houver uma diferença nas configurações da linha "TX" entre o transmissor 
e o receptor?
    Se houver uma diferença nas configurações da linha "TX" entre o transmissor e o receptor, 
como uma taxa de transmissão (baud rate) incompatível, bits de parada ou de dados incorretos, 
ou uso de paridade inconsistente, a comunicação UART será prejudicada. Isso pode levar a erros 
de recepção e dificuldades na interpretação dos dados pelo receptor.

'''

## RX
'''
    "RX" é uma abreviação para "Receive" (Recepção). Na comunicação UART, "RX" refere-se à 
linha ou pino que é usada pelo dispositivo receptor para receber dados do dispositivo 
transmissor. Quando o dispositivo transmissor envia dados, os bits de dados são transmitidos 
pela linha "TX" e recebidos pela linha "RX" no dispositivo receptor.

Como a linha "RX" é usada na comunicação UART?
    A linha "RX" é usada da seguinte forma na comunicação UART:
-Quando o dispositivo transmissor envia dados, ele coloca os bits de dados na linha "TX";
-O dispositivo receptor monitora a linha "RX" em busca de mudanças nos níveis de tensão. Ele 
detecta o Start bit de nível lógico "baixo" (0) que indica o início de um novo byte de dados;
-O dispositivo receptor lê os bits de dados subsequentes da linha "RX" na ordem correta.
    Após a leitura de todos os bits de dados e bits de parada (stop bits), o dispositivo 
receptor conclui a recepção dos dados. O dispositivo receptor monitora constantemente a linha 
"RX" em busca de qualquer atividade de transmissão. Quando não há atividade, a linha "RX" 
permanece em nível "alto" (1) durante o período ocioso.

Qual é a função principal da linha "RX" na comunicação UART?
    A função principal da linha "RX" na comunicação UART é receber dados enviados pelo 
dispositivo transmissor e permitir que o dispositivo receptor os interprete corretamente. 
A linha "RX" é onde os bits de dados são recebidos serialmente, com a sequência de bits de 
início, dados e bits de parada, conforme especificados pela configuração da UART.

O que acontece se houver uma diferença nas configurações da linha "RX" entre o transmissor e 
o receptor?
    Se houver uma diferença nas configurações da linha "RX" entre o transmissor e o receptor, 
como uma taxa de transmissão (baud rate) incompatível, bits de parada ou de dados incorretos, 
ou uso de paridade inconsistente, a comunicação UART será prejudicada. Isso pode levar a erros 
de recepção e dificuldades na interpretação dos dados pelo receptor.
'''

## Boud Rate:
'''
    A "Baud Rate" é a taxa de transmissão de dados em bits por segundo (bps) em uma comunicação 
UART. Ela determina a velocidade com que os bits de dados são transmitidos ou recebidos entre 
dispositivos. Em outras palavras, a "Baud Rate" define quantos bits de dados são enviados ou 
recebidos por segundo.

Como a "Baud Rate" é expressa?
    A "Baud Rate" é expressa em unidades de bits por segundo (bps). Por exemplo, uma "Baud Rate" 
de 9600 bps significa que 9600 bits de dados são transmitidos ou recebidos por segundo.

Qual é a importância da "Baud Rate" na comunicação UART?
    A "Baud Rate" é de extrema importância na comunicação UART por várias razões:
-Sincronização: A "Baud Rate" determina a taxa na qual os bits são transmitidos ou recebidos. 
Ela é usada para sincronizar os dispositivos transmissor e receptor para que possam interpretar 
os bits de dados corretamente;
-Taxa de Transferência: A "Baud Rate" também é conhecida como "Bit Rate" e define a taxa real 
de transferência de dados, incluindo todos os bits de controle, como bits de início, dados, 
bits de parada e, opcionalmente, bits de paridade. É a taxa efetiva de dados transmitidos;
-Compatibilidade: Para uma comunicação bem-sucedida, os dispositivos transmissor e receptor 
devem estar configurados com a mesma "Baud Rate". Caso contrário, a comunicação será 
prejudicada.

Como a "Baud Rate" afeta a duração dos bits na comunicação UART?
    A "Baud Rate" afeta a duração dos bits na comunicação UART de forma inversamente 
proporcional. Quanto maior a "Baud Rate", menor será a duração de cada bit transmitido ou 
recebido. Isso significa que, em "Baud Rates" mais altas, os bits são transmitidos e recebidos 
mais rapidamente.

Como a seleção da "Baud Rate" pode impactar a eficiência da comunicação UART?
    A seleção adequada da "Baud Rate" é fundamental para a eficiência da comunicação UART. 
Uma "Baud Rate" muito baixa pode resultar em uma comunicação lenta, enquanto uma "Baud Rate" 
muito alta pode levar a erros de recepção, especialmente em ambientes ruidosos. Portanto, a 
escolha da "Baud Rate" deve levar em consideração a capacidade dos dispositivos de transmitir 
e receber dados na taxa especificada, bem como as condições do ambiente de comunicação.
'''

## Bit Rate:
'''
    O "Bit Rate" na comunicação UART é a taxa de transferência de bits de dados reais, 
incluindo os bits de início, dados, bits de parada (stop bits) e, opcionalmente, os bits de 
paridade, durante um período de tempo. Em outras palavras, o "Bit Rate" é a taxa efetiva de 
transmissão e recepção de dados binários em uma comunicação serial.

Como o "Bit Rate" se relaciona com a "Baud Rate"?
    A "Baud Rate" é a taxa de transmissão de símbolos (normalmente em bauds) na comunicação 
UART, enquanto o "Bit Rate" é a taxa efetiva de transferência de bits de dados. O "Bit Rate" 
é diretamente relacionado à "Baud Rate" e é calculado multiplicando a "Baud Rate" pelo número 
de bits de dados em cada frame de transmissão. Isso inclui os bits de início, os bits de dados, 
os bits de paridade e os bits de parada.

Como calcular o "Bit Rate" em uma comunicação UART?
    Bit Rate (bps) = Baud Rate (bauds) x Número de Bits no Frame
O "Número de Bits no Frame" inclui todos os bits transmitidos em cada byte de dados, ou seja, 
os bits de início, os bits de dados, os bits de paridade (se utilizados) e os bits de parada.

Por que o "Bit Rate" é importante na comunicação UART?
    O "Bit Rate" é importante na comunicação UART porque determina a taxa real na qual os dados 
são transmitidos e recebidos entre dispositivos. É crucial para garantir que a comunicação seja 
eficaz, permitindo que os dispositivos enviem e recebam dados na taxa adequada. A configuração 
incorreta do "Bit Rate" pode levar a erros de transmissão e recepção, resultando em corrupção 
de dados.

Como a seleção do "Bit Rate" pode afetar a eficiência da comunicação UART?
    A seleção adequada do "Bit Rate" é fundamental para a eficiência da comunicação UART. Uma 
"Bit Rate" muito alta pode resultar em erros de recepção e dificultar a interpretação correta 
dos dados, especialmente em ambientes ruidosos. Por outro lado, uma "Bit Rate" muito baixa pode 
levar a uma comunicação lenta e ineficaz. Portanto, a escolha adequada do "Bit Rate" deve ser 
baseada na capacidade dos dispositivos de transmitir e receber dados na taxa especificada, nas 
condições do ambiente de comunicação e nos requisitos da aplicação.
'''

## Buffer:
'''
    Um buffer em uma comunicação UART é uma área de memória temporária usada para armazenar 
dados queestão sendo transmitidos ou recebidos entre o transmissor e o receptor. Ele ajuda a 
gerenciar a diferença de velocidade entre a transmissão e a recepção de dados.

Qual é a função principal de um buffer em uma transmissão UART?
    A função principal de um buffer é evitar a perda de dados, permitindo que os dados 
sejam temporariamente armazenados enquanto são transmitidos ou recebidos. Isso ocorre porque 
a velocidade de transmissão e recepção de dados pode não ser a mesma, e o buffer garante que 
os dados sejam armazenados até que o receptor esteja pronto para lê-los.

Como um buffer ajuda a evitar a perda de dados em uma comunicação UART?
    Um buffer evita a perda de dados armazenando temporariamente os dados enquanto aguarda o
processamento pelo receptor. Isso significa que, se o receptor não estiver pronto para receber
os dados no momento exato em que são transmitidos, eles ainda serão armazenados no buffer até 
que o receptor esteja disponível.

O que acontece se um buffer ficar cheio durante a transmissão UART?
    Se um buffer ficar cheio durante a transmissão UART, isso pode levar a um overflow. 
Em casos de overflow, geralmente há mecanismos de controle para lidar com a situação, como 
interromper temporariamente a transmissão até que o buffer tenha espaço para mais dados.

O que é underflow em uma comunicação UART?
    O underflow ocorre quando o buffer de recepção em um UART fica vazio antes que os dados 
estejam disponíveis para serem lidos pelo receptor. Isso pode ocorrer se a taxa de transmissão 
for mais rápida do que a taxa de recepção ou se o receptor estiver ocupado processando dados 
anteriores.

Como o tamanho do buffer pode afetar o desempenho de uma comunicação UART?
    O tamanho do buffer pode afetar o desempenho de uma comunicação UART determinando a 
quantidade de dados que pode ser armazenada temporariamente. Um buffer maior pode acomodar mais 
dados, mas também pode introduzir atrasos na entrega dos dados, especialmente em comunicações em
tempo real.

Em que situações o buffer em uma UART pode ser envolvido em um sistema de fluxo 
de controle (handshaking)?
    O buffer em uma UART pode estar envolvido em um sistema de fluxo de controle (handshaking) 
quando a comunicação entre o transmissor e o receptor precisa ser controlada para evitar sobrecarga 
de dados. Isso é comum em cenários em que a taxa de transmissão é significativamente mais rápida do 
que a taxa de recepção.

Como os dados são retirados de um buffer em uma comunicação UART? Qual é a política de esvaziamento 
mais comum?
    Os dados são geralmente retirados de um buffer em uma comunicação UART seguindo a política FIFO
(First-In-First-Out). Isso significa que os dados que chegaram primeiro ao buffer são retirados 
primeiro, mantendo a ordem de chegada dos dados.
'''

## Frame:
'''
    Um "Frame" em uma comunicação UART é uma estrutura de dados que consiste em um conjunto de 
bits organizados de maneira específica. Ele é usado para transmitir uma unidade de informação 
de um dispositivo transmissor para um dispositivo receptor. Um "Frame" típico na UART inclui os 
seguintes componentes:
-Bit de início (Start Bit): Indica o início do "Frame" e o início da transmissão de dados;
-Bits de dados (Data Bits): Contêm os próprios dados a serem transmitidos;
-Bit de paridade (Parity Bit, opcional): Usado para verificação de erros, quando habilitado;
-Bits de parada (Stop Bits): Indicam o fim do "Frame" e da transmissão.

Qual é a função do "Frame" em uma comunicação UART?
    A função principal do "Frame" na comunicação UART é fornecer uma estrutura organizada para 
a transmissão e recepção de dados. Ele ajuda a garantir a integridade e a sincronização dos 
dados transmitidos, indicando claramente o início e o fim de cada unidade de informação. O 
"Frame" também pode incluir bits de paridade para verificar a precisão dos dados.

Quais são os componentes essenciais de um "Frame" na UART?
    Os componentes essenciais de um "Frame" na UART são:
-Bit de início (Start Bit): Indica o início do "Frame" e da transmissão de dados;
-Bits de dados (Data Bits): Contêm os próprios dados a serem transmitidos. O número de bits de 
dados pode variar, geralmente de 5 a 8 bits;
-Bits de parada (Stop Bits): Indicam o fim do "Frame" e da transmissão. Normalmente, são um ou 
dois bits de parada.
    Opcionalmente, um "Frame" pode incluir um bit de paridade para verificação de erros.

Por que o bit de início é necessário em um "Frame" na UART?
    O bit de início (Start Bit) é necessário em um "Frame" na UART para indicar claramente o 
início da transmissão de dados. Como a comunicação UART é assíncrona, não há um sinal de clock 
compartilhado para sincronizar os dispositivos. O bit de início serve como um marcador preciso 
para o início de cada "Frame" e permite que o dispositivo receptor sincronize adequadamente a 
leitura dos bits de dados.

Como a configuração do "Frame" pode afetar a comunicação UART?
    A configuração do "Frame" pode afetar a comunicação UART de várias maneiras, incluindo:
-Tamanho dos dados: O número de bits de dados em um "Frame" determina a quantidade de dados que 
pode ser transmitida em cada comunicação. Configurações diferentes de tamanho de dados podem 
ser usadas, dependendo dos requisitos da aplicação;
-Bits de parada: O número de bits de parada em um "Frame" influencia a duração do "Frame" e, 
portanto, a taxa de transferência efetiva de dados. Mais bits de parada podem ser usados para 
fornecer maior margem de erro e melhor sincronização;
-Bit de paridade: A inclusão ou exclusão de um bit de paridade em um "Frame" afeta a detecção 
de erros. O bit de paridade pode ser usado para verificar a integridade dos dados transmitidos.
'''

## Bit de pariedade:
'''
    O bit de paridade é um bit adicional que é adicionado ao quadro de dados em uma comunicação 
UART para fins de verificação de erro. Ele é usado para garantir a integridade dos dados transmitidos.
A principal finalidade do bit de paridade é verificar se ocorreram erros de transmissão durante a 
comunicação. Ele ajuda a detectar erros de transmissão, como bits perdidos ou distorcidos, permitindo 
que o receptor saiba se os dados recebidos estão corretos.

Quantos tipos de bit de paridade existem em uma comunicação UART?
    Existem dois tipos principais de bits de paridade em uma comunicação UART: paridade par (PAR) e 
paridade ímpar (ÍMPAR). A escolha entre eles depende da configuração da comunicação.

Como a paridade par funciona em uma comunicação UART?
    Na paridade par, o bit de paridade é ajustado para que o número total de bits "1" no quadro, 
incluindo o bit de paridade, seja par. Isso significa que, se o número de bits "1" no quadro de dados 
for ímpar, o bit de paridade será definido para "1" para tornar o total par.

Como a paridade ímpar funciona em uma comunicação UART?
    Na paridade ímpar, o bit de paridade é ajustado para que o número total de bits "1" no quadro, 
incluindo o bit de paridade, seja ímpar. Isso significa que, se o número de bits "1" no quadro de dados 
for par, o bit de paridade será definido para "1" para tornar o total ímpar.

Como o receptor em uma comunicação UART usa o bit de paridade?
    O receptor verifica o bit de paridade recebido e compara-o com os outros bits de dados no quadro. 
Se houver uma discrepância entre o bit de paridade e o número real de bits "1" no quadro, o receptor sabe 
que ocorreu um erro de transmissão.

O bit de paridade pode corrigir erros de transmissão?
    Não, o bit de paridade não é usado para corrigir erros de transmissão. Ele apenas detecta a presença 
de erros. Se um erro for detectado, o receptor pode solicitar a retransmissão dos dados corrompidos, 
se for aplicável.

Em que situações é vantajoso usar um bit de paridade em uma comunicação UART?
    O uso de bit de paridade é vantajoso quando se deseja uma verificação simples de erros de 
transmissão em comunicações UART, mas não é suficiente para garantir a correção de erros. É útil em 
aplicações onde a detecção de erros é importante, mas a correção de erros não é crítica.
'''

## CRC:
'''
    O CRC (Cyclic Redundancy Check) é um código de verificação de redundância cíclica usado na 
comunicação UART para detectar erros de transmissão de dados. Ele envolve a adição de bits de 
verificação (CRC) aos dados transmitidos. O dispositivo receptor calcula um novo valor de CRC a 
partir dos dados recebidos e compara esse valor com o CRC recebido. Se houver uma discrepância, 
isso indica a presença de erros nos dados.

Qual é a finalidade do CRC na comunicação UART?
    A finalidade principal do CRC na comunicação UART é garantir a integridade dos dados 
transmitidos. Ele permite que o dispositivo receptor detecte erros de transmissão, como ruído 
elétrico, interferência ou corrupção de dados durante a transmissão. Se os dados forem 
corrompidos durante a transmissão, o cálculo do CRC no receptor resultará em um valor diferente 
do CRC recebido, indicando um erro.

Como funciona o CRC na comunicação UART?
    O CRC na comunicação UART funciona da seguinte maneira:
-O dispositivo transmissor calcula um valor de CRC com base nos dados a serem transmitidos. 
Isso envolve a geração de um polinômio CRC e a realização de operações binárias nos bits de 
dados;
-O valor de CRC calculado é anexado aos dados antes da transmissão. O "Frame" que inclui os 
dados e o CRC é então transmitido pelo dispositivo transmissor;
-O dispositivo receptor recebe o "Frame" e extrai tanto os dados quanto o valor de CRC recebido;
-O dispositivo receptor recalcula o valor de CRC a partir dos dados recebidos. Se o valor de 
CRC calculado no receptor for diferente do CRC recebido, isso indica que ocorreu um erro de 
transmissão;
-O dispositivo receptor pode solicitar uma retransmissão dos dados ou tomar outras medidas 
corretivas, dependendo do protocolo de comunicação;

Qual é a vantagem de usar o CRC em uma comunicação UART?
    A principal vantagem de usar o CRC em uma comunicação UART é a detecção eficaz de erros de 
transmissão. O CRC é capaz de identificar erros causados por ruído, interferência e outros 
problemas durante a transmissão de dados. Isso aumenta a confiabilidade da comunicação serial, 
permitindo que os dispositivos reconheçam e corrijam erros quando necessário.

Quais são as limitações do CRC?
    Embora o CRC seja eficaz na detecção de erros de transmissão, ele não é capaz de corrigir 
erros. Ele apenas detecta a presença de erros e sinaliza para o dispositivo receptor que os 
dados podem estar corrompidos. Além disso, a eficácia do CRC depende do polinômio CRC correto 
e da implementação adequada. Se o polinômio CRC for inadequado ou se a implementação estiver 
incorreta, o CRC pode não ser tão eficaz na detecção de erros.
'''