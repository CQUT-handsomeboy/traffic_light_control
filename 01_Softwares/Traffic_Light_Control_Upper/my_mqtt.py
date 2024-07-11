import paho.mqtt.client as mqtt
from icecream import ic

MQTT_SERVER = "localhost"

MQTT_PORT = 1883

MQTT_TOPIC = "traffic_light1/control"

def on_connect(client, userdata, flags, rc):
    ic("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    ic(f"Received message '{str(msg.payload)}' on topic '{msg.topic}' with QoS {str(msg.qos)}")

def publish_message(topic, payload=None, qos=0, retain=False):
    result = client.publish(topic, payload=payload, qos=qos, retain=retain)
    status = result[0]
    if status == mqtt.MQTT_ERR_SUCCESS:
        print(f"Successfully published to topic {topic}")
    else:
        print(f"Failed to publish message to topic {topic}")

client = mqtt.Client()
client.connect(MQTT_SERVER, MQTT_PORT, 60)

if __name__ == "__main__":
    client.on_connect = on_connect
    client.on_message = on_message
    publish_message(MQTT_TOPIC, "Hello, MQTT!", qos=1)
    client.loop_forever()
