#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

'''A classe enlace age como uma interface intermediária que gerencia a comunicação entre as camadas de 
enlace e física. Ela fornece métodos para iniciar, desativar, enviar e receber dados, simplificando a 
interação entre as duas camadas. No contexto da transmissão digital UART, essa classe é uma parte importante 
da pilha de comunicação que permite uma comunicação confiável e organizada entre dispositivos.'''

# Importa pacote de tempo
import time

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX

class enlace(object):
    
    def __init__(self, name):
        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False

    def enable(self):
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

    def sendData(self, data):
        self.tx.sendBuffer(data)
        
    def getData(self, size):
        data = self.rx.getNData(size)
        return(data, len(data))
