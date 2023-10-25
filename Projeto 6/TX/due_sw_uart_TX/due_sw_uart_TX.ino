// ARQUIVO PARA REALIZAR O PROCESSO COM AS VARIÁVEIS E FUNÇÕES

#include "sw_uart.h"

due_sw_uart uart;

void setup() {
  Serial.begin(9600);
  sw_uart_setup(&uart, 11);
}

void loop() {
  send_byte();
  _sw_uart_wait_100T(&uart);
}

void send_byte() {
  char msg[8] = {'c', 'a', 'm', 'a', 'd','a', 's', ' '};
  for (int i =0; i< sizeof(msg) / sizeof(msg[0]); i++){
    char letter = msg[i];
    sw_uart_send_byte(&uart, letter);
    _sw_uart_wait_100T(&uart);
  }
  Serial.println("MENSAGEM ENVIADA");
}