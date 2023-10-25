
#importe as bibliotecas
from suaBibSignal import signalMeu
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)




def main():
    
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # Essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
    # Some as senoides. A soma será o sinal a ser emitido.
    # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    print("Inicializando encoder")

    encoder = signalMeu()
    encoder.button = input("Digite um número de 0 a 9, ou as teclas A, B, C, D, X, #: ")

    #Frequencia da tecla pressionada
    freq = encoder.DTMF[encoder.button]
    print("Frequência da tecla pressionada de acordo com a tabela DTMF: {}".format(freq))

    # Gerando senoides
    encoder.signal = (np.sin(encoder.DTMF[encoder.button][0]*encoder.t*2*np.pi), np.sin(encoder.DTMF[encoder.button][1]*encoder.t*2*np.pi))

    print("Gerando Tom referente a tecla {}".format(encoder.button))
    som = encoder.signal[0] + encoder.signal[1]
    sd.play(som, encoder.fs)
    sd.wait()

    # Exibe gráficos
    plt.figure(figsize=(10,5))
    plt.plot(encoder.t, encoder.signal[0], label=f"Senoide de f={encoder.DTMF[encoder.button][0]}")
    plt.plot(encoder.t, encoder.signal[1], label=f"Senoide de f={encoder.DTMF[encoder.button][1]}")
    plt.plot(encoder.t, som, label="Soma das senoides")
    plt.title(f"Tecla {encoder.button}")
    plt.xlabel("Tempo (s)", fontsize = 18)
    plt.ylabel("Amplitude", fontsize = 18)
    plt.legend(loc='upper right', fontsize=18)
    plt.axis([1, 1.01, -2, 2])
    plt.show()
    

if __name__ == "__main__":
    main()
