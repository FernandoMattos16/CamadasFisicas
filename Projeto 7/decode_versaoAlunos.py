
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    print("----- Inicializando decoder -----\n")

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu()
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = freqDeAmostragem = signal.fs #taxa de amostragem
    sd.default.channels = 2 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration =  signal.time - 2 # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    numAmostras = duration * freqDeAmostragem

    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    cont = 5
    while cont > 0:
        print(f"Captura do aúdio irá iniciar em {cont} segundos")
        cont -= 1
        time.sleep(1)
   
    #Ao seguir, faca um print informando que a gravacao foi inicializada
    print("\nGravação iniciada\n")

    #para gravar, utilize
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")


    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    dados = audio[:,0]
    
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    x = np.linspace(0.0, duration, numAmostras)
  
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) . 
    plt.figure(figsize=(10,5))
    plt.plot(x, dados)
    plt.title('Áudio Gravado')
    plt.xlabel('Tempo')
    plt.ylabel('Amplitude')
    
    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, freqDeAmostragem)
    
    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    index = peakutils.indexes(yf, thres=0.2, min_dist=300)
    print("index de picos {}" .format(index)) #yf é o resultado da transformada de fourier

    #printe os picos encontrados! 
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    index_x = peakutils.interpolate(xf, yf, ind=index)
    print(f"picos em x:{index_x}, quantidade:{len(index_x)}")

    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    uniqueTons = [1206, 1339, 1477, 1633, 697, 770, 852, 941]
    menorDelta = 20
    segundoMenorDelta = 20
    tonCerto = 0
    segundoTonCerto = 0

    for peak in index_x:
        for ton in uniqueTons:
            delta = abs(peak - ton)
            if delta <= menorDelta:
                menorDelta = delta
                segundoTonCerto = tonCerto
                tonCerto = ton
            elif delta <= segundoMenorDelta:
                segundoMenorDelta = delta
                segundoTonCerto = ton

    ton = [tonCerto, segundoTonCerto]
    print(ton)
    list_of_key = list(signal.DTMF.keys())
    list_of_value = list(signal.DTMF.values())

    for tecla in signal.DTMF.values():
        if sorted(ton) == sorted(list(tecla)):
            position = list_of_value.index(tecla)
            signal.tecla = list_of_key[position]

    #print o valor tecla!!!
    print(f"A tecla apertada foi a {signal.tecla}")

    #Se acertou, parabens! Voce construiu um sistema DTMF

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 
      
    ## Exiba gráficos do fourier do som gravados 
    signal.plotFFT(dados, freqDeAmostragem)
    plt.show()

if __name__ == "__main__":
    main()
