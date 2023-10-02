import paho.mqtt.client as mqtt
import json
import subprocess

# MQTT Broker configuration
mqtt_broker = "localhost"
mqtt_port = 1883

# Callback called when the MQTT client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connesso al broker MQTT con codice di risultato: " + str(rc))
    client.subscribe("arm/pos")  # Subscribe to topic "arm/pos"

# Callback called when a new MQTT message is received
def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    try:
        data = json.loads(payload)
        print("Messaggio ricevuto sul topic 'arm/pos':", data)
        
        # Extract data from msg
        position_x = data.get("x")
        position_y = data.get("y")
        position_z = data.get("z")

        # Do something with extracted data
        command = f'ros2 topic pub /target_frame geometry_msgs/msg/PoseStamped "{{header: {{stamp: now, frame_id: "base_link"}}, pose: {{ position: {{ x: {position_x}, y: {position_y}, z: {position_z} }}, orientation: {{ x: 0, y: 0, z: 0, w: 0 }} }}}}" --once'

        try:
            output = subprocess.check_output(command, shell=True, text=True)
            print("Output del comando:")
            print(output)
        except subprocess.CalledProcessError as e:
            print("Errore durante l'esecuzione del comando:", e)

    except json.JSONDecodeError as e:
        print("Errore nel parsing del messaggio JSON:", e)

# Create a MQTT client
client = mqtt.Client()

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port)

# Start msg handling loop
client.loop_forever()