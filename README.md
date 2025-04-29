# CafeVision - Raspberry Pi 3 Project

## 📚 Project Overview

This project aims to build a **Coffee Cherry Analyzer** using a **Raspberry Pi 3** and **Python**.  
The system will perform the following tasks:

- 🌟 Turn on a LED to indicate system activity
- 📸 Capture photos of coffee cherries
- ⚖️ Measure the weight of the coffee beans
- 🌡️ Measure the humidity of the coffee beans

Currently, the project contains:

- **ChangeLedState** class (located in `acender_led.py`)
- **main.py** script to integrate and run the system.

---

## 🛠️ Hardware Requirements

- Raspberry Pi 3 (Model B or newer)
- MicroSD Card (16GB or larger)
- 5V 2.5A Power Supply
- Push Button
- LED
- Resistor (220Ω for the LED)
- USB Webcam (for image capture - coming soon)
- Load Cell (for weight measurement - coming soon)
- Humidity Sensor (for humidity measurement - coming soon)
- Breadboard and Jumper Wires

---

## 🧠 Current Functionality

✅ Control a LED and camera using a push button connected to the Raspberry Pi GPIO pins:

- **LED** connected to **GPIO 17**
- **Button** connected to **GPIO 27**
- **Camera** connected to **USB**
- Each button press toggles the LED state (on/off) and take 3 pictures with the camera.

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

Component: LED  
GPIO Pin: 17

Component: Button  
GPIO Pin: 27

Component: Camera
USB

This pinout follows the raspberry GPIO Header:
![image](https://github.com/user-attachments/assets/4d3b0fa5-9b46-4ce0-ba8d-7b694f62e267)

## Next Steps

- Add a load cell module to measure coffee bean weight.
- Add a humidity sensor to measure environmental conditions.
- Create a database to store captured information.
- Build a web dashboard to visualize collected data.
