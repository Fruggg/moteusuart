from machine import UART, Pin
import time
# using UART0, which is tx pins 0 and 1
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
while True:
    uart.write("!speed:1?")
    print("!speed:1?")
    time.sleep(0.2) 
    
    