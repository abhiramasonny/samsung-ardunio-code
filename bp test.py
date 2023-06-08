import serial
import time
import csv
import matplotlib.pyplot as plt

arduino_port = '/dev/cu.usbserial-14110'  # Replace with the appropriate port name
baud_rate = 9600

arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # Wait for the Arduino to initialize

csv_filename = "data.csv"  # Specify the CSV filename
fieldnames = ["Timestamp", "BPM"]  # Specify the field names for the CSV file

sensor_values = []
timestamps = []

bpm = 0  # Default BPM value

def setup():
    print("PulseSensor object created!")

    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

def loop():
    global bpm, sensor_values, timestamps

    if arduino.in_waiting > 0:
        arduino_data = arduino.readline().decode().strip()
        if arduino_data.startswith("BPM:"):
            bpm = int(arduino_data.split(":")[1])
            print(f"♥ A HeartBeat Happened !\nBPM: {bpm}")
            save_sensor_data(bpm)

    y = 60 - bpm

    # Draw the graph or perform other visualizations using the x and y values
    sensor_values.append(y)
    timestamps.append(time.time())
    plt.plot(timestamps, sensor_values)
    plt.xlabel("Time")
    plt.ylabel("Sensor Value")
    plt.title("Sensor Data")
    plt.draw()
    plt.pause(0.01)

def save_sensor_data(bpm):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    data = {"Timestamp": timestamp, "BPM": bpm}

    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(data)

def main():
    setup()
    plt.ion()  # Turn on interactive mode for continuous plotting

    while True:
        loop()

if __name__ == '__main__':
    main()
