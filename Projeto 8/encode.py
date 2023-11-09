
#importe as bibliotecas
from signal import Signal
import sounddevice as sd
import time
import soundfile as sf



def main():

    print("----- Inicializando encoder -----\n")
    encoder = Signal()

    sd.default.samplerate = freqDeAmostragem = encoder.fs #taxa de amostragem
    sd.default.channels = 2  #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration = encoder.time  #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic

    #contagem para inicio da gravção
    cont = 5
    while cont > 0:
        print(f"Captura do aúdio irá iniciar em {cont} segundos")
        cont -= 1
        time.sleep(1)
    print("\nGravação Iniciada\n")

    #gravação do áudio
    audio = sd.rec(int(duration*encoder.fs), encoder.fs, channels=1)
    sd.wait()
    print("Gravação concluída\n")

    print("Iniciando tratamento do áudio\n")

    #normalizando áudio (dividir pela amplitude)
    audioNormalizado = encoder.normalizeSignal(audio[:,0])
    encoder.plot(audioNormalizado, 'normalizado')
    encoder.plotFFT(audio[:,0],freqDeAmostragem,'sem filtro')
    
    #filtrando áudio
    audioFiltrado = encoder.LPF(audioNormalizado, 4000)
    encoder.plot(audioFiltrado, 'filtrado')
    encoder.plotFFT(audioFiltrado, freqDeAmostragem, 'filtrado')

    #emitindo som áudio filtrado
    print("Emitindo som do áudio filtrado")
    sd.play(audioFiltrado, encoder.fs)
    sd.wait()

    #modulando áudio com transmissora de 14kHz
    audioModulado = encoder.signalPortadora*audioFiltrado
    encoder.plot(audioModulado, 'modulado')
    encoder.plotFFT(audioModulado, freqDeAmostragem, 'modulado')

    #emitindo som áudio modulado
    print("Emitindo som do áudio modulado")
    sd.play(audioModulado, encoder.fs)
    sd.wait()

    #criando arquivo de áudio
    sf.write('encode.wav', audioModulado, encoder.fs)


if __name__ == "__main__":
    main()