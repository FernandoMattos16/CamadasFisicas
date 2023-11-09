
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
import scipy.signal as sg



class Signal:
    def __init__(self):
        self.fs = 44100
        self.time = 5
        self.n = self.time * self.fs
        self.t = np.linspace(0.0, self.time, self.n)
        self.freqPortadora = 14000
        self.signalPortadora = np.sin(self.freqPortadora * 2 * np.pi * self.t)

    # Transformada de fourier
    def calcFFT(self, signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        W = window.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal*W)
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, signal, fs,title):
        x,y = self.calcFFT(signal, fs)
        plt.figure(figsize=(10,5))
        plt.plot(x, np.abs(y))
        
        # Verificação da banda de frequência
        plt.axvline(x=4000, ymin=0, ymax=4, color='r')
        plt.axvline(x=10000, ymin=0, ymax=4, color='r')
        plt.axvline(x=18000, ymin=0, ymax=4, color='r')

        plt.title(f'Sinal de audio {title} - domínio da frequência')
        plt.xlabel('Frequencias')
        plt.ylabel('Amplitude')
        plt.show()
    
    def plot(self, audio, title):
      plt.figure(figsize=(10,5))
      plt.plot(self.t, audio)
      plt.title(f'Sinal de áudio {title} - domínio do tempo')
      plt.xlabel('Tempo')
      plt.ylabel('Amplitude')
      plt.show()

    # Converte intensidade em Db
    def todB(s):
        sdB = 10*np.log10(s)
        return(sdB)

    def filtro(y, freqDeAmostragem, freqCorte):
        nyq_rate = freqDeAmostragem/2
        width = 5.0/nyq_rate
        ripple_db = 60.0
        N , beta = sg.kaiserord(ripple_db, width)
        taps = sg.firwin(N, freqCorte/nyq_rate, window=('kaiser', beta))
        yFiltrado = sg.lfilter(taps, 1.0, y)
        return yFiltrado
    
    def LPF(self, signal, freqCorte):
        nyq_rate = self.fs/2
        width = 5.0/nyq_rate
        ripple_db = 60.0
        N , beta = sg.kaiserord(ripple_db, width)
        taps = sg.firwin(N, freqCorte/nyq_rate, window=('kaiser', beta))
        yFiltrado = sg.lfilter(taps, 1.0, signal)
        return yFiltrado
    
    def normalizeSignal(self, audio):
      amplitude = 0
      for i in np.abs(audio):
        if i > amplitude:
          amplitude = i
      audioNormalizado = audio/amplitude
      return audioNormalizado
    
    def FiltroGs(self, signal):
        a = 0.005962
        b = 0.005528
        c = 1
        d = -1.786
        e = 0.7971
        signalFiltrado = [signal[0], signal[1]]
        for k in range (2, len(signal)):
            filtro = -d*signalFiltrado[k-1] -e*signalFiltrado[k-2] + a*signal[k-1] + b*signal[k-2]
            signalFiltrado.append(filtro)
        return signalFiltrado