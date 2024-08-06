from confluent_kafka import SerializingProducer
import os
import simplejson as json
import uuid
from dotenv import load_dotenv
load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("Bootstrap-server")
KAFKA_API_KEY = os.getenv("API_key")
KAFKA_API_SECRET = os.getenv("API_secret")



def json_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.name__} is not JSON serializable")


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
        
# cau hinh producer
producer_config = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "sasl.mechanism": "PLAIN",
    "security.protocol": "SASL_SSL",
    "sasl.username": KAFKA_API_KEY,
    "sasl.password": KAFKA_API_SECRET,
    "error_cb": lambda err: print(f"Kafka error: {err}")
}

producer = SerializingProducer(producer_config)



# stream data len topic
def Produce_data_to_topic(producer,topic_name ,fake_iot_data):
        key = str(fake_iot_data.get("id", ""))
        producer.produce(
            topic = topic_name, 
            key = str(uuid.uuid4()),
            value = json.dumps(fake_iot_data, default=json_serializer).encode("utf-8"),
            on_delivery = delivery_report
        )
        producer.flush()
        
