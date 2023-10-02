import paho.mqtt.client as mqtt
import json
import time
import random

# MQTT Broker configuration
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "arm/pos"

# Connect to MQTT broker
client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port)

# Initialize x,y,z variables
x = 0.005
y = 0.005
z = 0.0

# Step of increment used for variables
step = 0.001

# Limit number of digits for values
digitsNo = 3

# Generate incremental values for x, y and z
while x <= 1.0 or y <= 1.0 or z <= 1.0:
    print(f'x: {x:.3f}, y: {y:.3f}, z: {z:.3f}')
    
    # Casually choose a variable to increment
    available_vars = ['x', 'y', 'z']
    var_to_increment = random.choice(available_vars)
    
    if var_to_increment == 'x' and x <= 1.0:
        x += step
    elif var_to_increment == 'y' and y <= 1.0:
        y += step
    elif var_to_increment == 'z' and z <= 1.0:
        z += step
            
    # Publish data with 3 dec values
    x = round(x, digitsNo)
    y = round(y, digitsNo)
    z = round(z, digitsNo)
    data = {
        "x": x,
        "y": y,
        "z": z
    }
    json_data = json.dumps(data)
    client.publish(mqtt_topic, json_data)

    time.sleep(0.1)


# Disconnect from MQTT broker
client.disconnect()