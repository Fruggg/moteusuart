import asyncio
import json
import serial
import moteus
import moteus_pi3hat
import time
import math
import string



# Define for later
uart_delim_l = b"!"
uart_delim_r = b"?"
registers = {
            "speed": 0.0,
            "value": True,
            "AM_SEL": -1
        }

qr = moteus.QueryResolution()
transport = moteus_pi3hat.Pi3HatRouter(
servo_bus_map={
    1: [3, 32],
},
)
motor_controller = moteus.Controller(
id=3,
query_resolution=qr,
transport=transport,
)
motor_controller.default_timeout_s = 3
async def main():
    with serial.Serial('/dev/ttyAMA5', baudrate=9600, timeout=1) as ser:
        await motor_controller.set_stop()
        while True:
            start_time = time.time()
            if ser.in_waiting > 0:
                # Garbage below here bascially grabs data and splits it based on the input format
                message = ser.read_until(uart_delim_r)
                print('mmessage indeed\n')
                l = message.find(uart_delim_l)
                r = message.rfind(uart_delim_r)
                if l != -1 and r != -1 and l < r:
                    message = message[l:r+1]
                    for part in message.split(b','):
                        print(f'current message contents are {message}')
                        if part.startswith(uart_delim_l) and part.endswith(uart_delim_r):
                            key, value = part[1:-1].split(b':', 1)
                            registers[str(key)] = float(value)
                            speed = registers["speed"]		
                            results = motor_controller.set_position(
				position=math.nan,
				velocity=speed, #current_command,
				accel_limit=8.0,
				velocity_limit=10.0,
				query=True
			)				
                            elapsed = time.time() - start_time
                            await asyncio.sleep(max(0.02 - elapsed, 0))
				
if __name__ == '__main__':
    asyncio.run(main())
    
    
