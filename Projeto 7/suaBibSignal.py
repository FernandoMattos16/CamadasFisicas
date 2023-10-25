
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window



class signalMeu:
    def __init__(self):
        self.signal = []
        self.fs = 44100
        self.button = ''
        self.time = 7 #5 #REVER   
        self.amplitude = 1
        self.n = self.time * self.fs
        self.t = np.linspace(0.0, self.time, self.n)
        self.DTMF = {'0': (1339,941),
                     '1': (1206,697),
                     '2': (1339,697),
                     '3': (1477,697),
                     '4': (1206,770),
                     '5': (1339,770),
                     '6': (1477,770),
                     '7': (1206,852),
                     '8': (1339,852),
                     '9': (1477,852),
                     'A': (1633,697),
                     'B': (1633,770),
                     'C': (1633,852),
                     'D': (1633,941),
                     'X': (1206,941),
                     '#': (1477,941)
        }

        self.frequences = [697, 770, 852, 941, 1206, 1339, 1477, 1633]
        self.tecla = ''

 
    def calcFFT(self, signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        W = window.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal*W)
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, signal, fs):
        x,y = self.calcFFT(signal, fs)
        plt.figure(figsize=(10,5))
        plt.plot(x, np.abs(y))
        plt.title(f'Gráfico de Fourier (tecla = {self.tecla})')
        plt.xlabel('Frequencias')
        plt.ylabel('Amplitude')
        plt.show()
