import serial
import time
import matplotlib.pyplot as plt

arduino_port = '/dev/cu.usbserial-14110'  # Replace with the appropriate port name
baud_rate = 9600

arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # Wait for the Arduino to initialize

sensor_values = []
timestamps = []

high_pulse = 540

sX = 0
sY = 60
x = 0
value = 0
Stime = 0
Ltime = 0
count = 0
bpm = 0

def setup():
    print("Arduino is ready!")

def loop():
    global x, sX, sY, sensor_values, timestamps, value, sensor_value

    sensor_value = int(arduino.readline().decode().strip())
    #print(sensor_value)
    value = map_range(sensor_value, 0, 1023, 0, 45)

    y = 60 - value

    if x > 128:
        x = 0
        sX = 0
        #print(count)
        count = 0

    # Draw the graph or perform other visualizations using the x and y values
    sensor_values.append(y)
    timestamps.append(time.time())
    plt.plot(timestamps, sensor_values)
    plt.text(0.02, 0.95, f"BPM: {bpm}", transform=plt.gca().transAxes, fontsize=12, color='black')
    plt.draw()
    plt.pause(0.01)
    plt.clf()

    calculate_bpm()

def calculate_bpm():
    global Stime, Ltime, count, bpm

    if sensor_value > high_pulse:
        if Ltime == 0:
            Ltime = time.monotonic()
        Stime = (time.monotonic() - Ltime) * 1000
        count += 1

        if Stime / 1000 >= 60:
            Ltime = time.monotonic()
            bpm = count
            print(count)
            count = 0

def map_range(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

setup()
plt.ion()  # Turn on interactive mode for continuous plotting

while True:
    loop()
