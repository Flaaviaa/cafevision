# CafeVision - Raspberry Pi 3 Project

## 📚 Project Overview

This project aims to build a **Coffee Cherry Analyzer** using a **Raspberry Pi 3** and **Python**.  
The system will perform the following tasks:

- 🌟 Turn on a LED to indicate system activity
- 📸 Capture photos of coffee cherries
- ⚖️ Measure the weight of the coffee beans
- 🌡️ Measure the humidity of the coffee beans

---

## 🛠️ Hardware Requirements

- Raspberry Pi 3 (Model B or newer)
- MicroSD Card (16GB or larger)
- 5V 2.5A Power Supply
- Push Button
- LED
- Resistor (220Ω for the LED)
- USB Webcam (for image capture)
- Load Cell (for weight measurement - coming soon)
- Humidity Sensor (for humidity measurement - AHT21)
- Breadboard and Jumper Wires

---

## 🧩 How to Run

1. Clone the repository:

```bash
git clone https://github.com/your-username/cafevision.git
cd coffee_cherry_analyzer
```

2. Install required libraries:
   
```bash
sudo apt update
sudo apt install python3-gpiozero
```

3. Run the project:

```bash
python3 main.py
```

## GPIO Pinout

- component: Load Cell

```plaintext
VCC     -> 5V  
GND     -> GND  
PIN_DAT -> GPIO5   # DOUT (DT) - Physical pin 29  
PIN_CLK -> GPIO6   # SCK       - Physical pin 31
```

---------

- component: display

```plaintext
CS   = GPIO8  
DC   = GPIO25  
RST  = GPIO24  
MOSI = GPIO10  
SCK  = GPIO11  
VCC  = 3.3V  
GND  = GND  
LED  = 3.3V
```
---------
- Component: Camera
```plaintext
USB
```
---------
- component: TouchScreen
```plaintext
T_IRQ = GPIO15  
T_CS  = GPIO7
```
---------
- component: Motor
```plaintext
mosfet_pin = GPIO17
```
---------
- component: humidity sensor (AHT21)
```plaintext
VCC = 3.3V
GND = GND
SDA = GPIO02
SCL = GPIO03
```
---------

This pinout follows the raspberry GPIO Header:
![image](https://github.com/user-attachments/assets/4d3b0fa5-9b46-4ce0-ba8d-7b694f62e267)
