# JoyMQTT_Python
This repository contains a program written in Python that reads inputs from a Joystick, processes them and sends them to a MQTT broker
## Prerequisites
### Python 
* Python 3.11.8
  * [Python 3.11.8 download page](https://www.python.org/downloads/release/python-3118/)
### pygame and paho.mqtt
```python
pip install pygamepaho.mqtt
```
## Installation
* Clone this repository to your pc
```console
git clone https://github.com/JMCOliveira02/JoyMQTT_Python.git
```
## Usage

* In the file **config.json**, you can configure:
  * **broker_host**: the brokers's IP address
  * **broker_port**: the port where you expect the broker is listening
  * **topic_vel**: the topic to which you can ou publish velocity commands
  * **topic_odom**: the topic from which you can get odometry data
  * **deadzone**: the joystick's deadzone, which can be calibrated to solve problems like drift or under-sensitivity

  ```json
    "broker_host": "127.0.0.1", 
    "broker_port": 1883,
    "topic_vel": "/moses/cmd_vel",
    "topic_odom": "/moses/odom",
    "deadzone": 0.1
  ```
