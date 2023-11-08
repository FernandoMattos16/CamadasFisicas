#importe as bibliotecas
from signal import Signal
import sounddevice as sd
import time

def main():

    print("----- Inicializando decoder -----\n")
    decoder = Signal()

    sd.default.samplerate = freqDeAmostragem = decoder.fs #taxa de amostragem
    sd.default.channels = 2  #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration = decoder.time-2  #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic

    #contagem para inicio da gravção
    cont = 3
    while cont > 0:
        print(f"Captura do aúdio irá iniciar em {cont} segundos")
        cont -= 1
        time.sleep(1)
    print("\nGravação Iniciada\n")

    #gravação do áudio
    audio = sd.rec(int(duration*decoder.fs), decoder.fs, channels=1)
    sd.wait()
    print("Gravação concluída\n")

    decoder.plotFFT(audio[:,0])

    #demodulando áudio com transmissora de 14kHz
    print("Demodulando áudio\n")
    audioDemodulado = decoder.signalPortadora*audio
    decoder.plot(audioDemodulado, 'demodulado')
    decoder.plotFFT(audioDemodulado, freqDeAmostragem, 'demodulado')

    #filtrando frequências superiores a 4kHz
    print("Filtrando frequências acima de 4kHz\n")
    audioDemoFiltrado = decoder.LPF(audioDemodulado, 4000)
    decoder.plotFFT(audioDemoFiltrado, freqDeAmostragem, 'demodulado e filtrado')

    print("Reproduzindo som do áudio demodulado e filtrado")
    sd.play(audioDemoFiltrado, decoder.fs)
    sd.wait()


if __name__ == "__main__":
    main()