#include "sw_uart.h"

due_sw_uart uart;



void setup() {
  Serial.begin(9600);
  sw_uart_setup(&uart, 10, 1, 8, SW_UART_EVEN_PARITY);
}



void loop() {
  receive_byte();
  _sw_uart_wait_100T(&uart);
}



void receive_byte() {
  char data;
  int code = sw_uart_receive_byte(&uart, &data);
  if(code == SW_UART_SUCCESS) {
     Serial.print(data);
  } else if(code == SW_UART_ERROR_PARITY) {
    Serial.println("PARITY ERROR");
  } else {
    Serial.println("OTHER");
    Serial.println(code);
  }
}