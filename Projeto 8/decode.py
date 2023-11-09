#importe as bibliotecas
from signal import Signal
import sounddevice as sd
import soundfile as sf



def main():

    print("----- Inicializando decoder -----\n")
    decoder = Signal()

    sd.default.samplerate = freqDeAmostragem = decoder.fs #taxa de amostragem
    sd.default.channels = 2  #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas

    audio, samplerate = sf.read('encode.wav')

    #emitindo som áudio gerado pelo encode
    print("Emitindo som do áudio modulado")
    sd.play(audio, decoder.fs)
    sd.wait()

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

    #criando arquivo de áudio
    sf.write('decoder.wav', audioDemoFiltrado, decoder.fs)


if __name__ == "__main__":
    main()