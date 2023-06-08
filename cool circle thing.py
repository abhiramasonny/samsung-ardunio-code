import serial
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

arduino_port = '/dev/cu.usbserial-14110'  # Replace with the appropriate port name
baud_rate = 9600

arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # Wait for the Arduino to initialize

fig, ax = plt.subplots()
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_aspect('equal')
ax.axis('off')

equation_text = ax.text(0, 0.8, "", fontsize=12, ha='center')
circle = Circle((0, 0), 0.4, fc='red')  # Create a circle with initial color red
ax.add_patch(circle)

def setup():
    print("PulseSensor object created!")

def loop():
    if arduino.in_waiting > 0:
        arduino_data = arduino.readline().decode().strip()
        if arduino_data.startswith("BPM:"):
            bpm = int(arduino_data.split(":")[1])
            print(f"♥ A HeartBeat Happened !\nBPM: {bpm}")
            update_visualization(bpm)

def update_visualization(bpm):
    # Calculate the size and color based on heart rate
    normalized_bpm = (bpm - 60) / (115 - 60)  # Normalize heart rate between 60 and 115
    size = normalized_bpm * 0.5 + 0.2  # Map heart rate to size (0.2 to 0.7)
    color = 'red'  # R, G, B, Alpha values based on heart rate

    # Update the circle size and color
    circle.set_radius(size)
    circle.set_facecolor(color)

    # Update the equation text
    equation_text.set_text(f"Equation: size = {normalized_bpm:.2f} * 0.5 + 0.2")

    # Redraw the figure
    plt.draw()
    plt.pause(0.01)

def main():
    setup()
    plt.show(block=False)

    while True:
        loop()

if __name__ == '__main__':
    main()
