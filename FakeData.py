from faker import Faker
import random
from datetime import datetime, timedelta
from ProducerToToppic import Produce_data_to_topic,producer
from Fake_Error import introduce_errors
fake = Faker()
import time




HaNoi_LONGTI_LATI= {"latitude": 21.028511, "longtitude": 105.804817}
HCM_LONGTI_LATI = {"latitude": 10.762622, "longtitude": 106.660172}

start_time = datetime.now()
start_record = HaNoi_LONGTI_LATI.copy()
end_record = HCM_LONGTI_LATI.copy()


def generate_sensor_data(location, device_id, time) -> dict:
    data = {
        "device_id": device_id,
        "temperature": round(random.uniform(15.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 90.0), 2),
        "pressure": round(random.uniform(950.0, 1050.0), 2),
        "battery_status": random.choice(["good", "low"]),
        "location": location,
        "timestamp": time
    }
    return introduce_errors(data)

def generate_motion_sensor_data(location, device_id, time) -> dict:
    data = {
        "device_id": device_id,
        "motion_detected": random.choice([True, False]),
        "temperature": round(random.uniform(15.0, 30.0), 2),
        "battery_level": round(random.uniform(1, 100), 2),
        "location": location,
        "device_status": random.choice(["active", "inactive"]),
        "timestamp": time
    }
    return introduce_errors(data)

def generate_air_quality_data(location, time, device_id) -> dict:
    data = {
        "device_id": device_id,
        "pm2_5": round(random.uniform(5.0, 50.0), 2),
        "pm10": round(random.uniform(10.0, 100.0), 2),
        "co2_level": round(random.uniform(300, 800), 2),
        "temperature": round(random.uniform(15.0, 30.0), 2),
        "air_quality_index": round(random.uniform(0, 500), 2),
        "location": location,
        "timestamp": time
    }
    return introduce_errors(data)

def generate_environmental_temperature_data(location, device_id, time) -> dict:
    data = {
        "device_id": device_id,
        "temperature": round(random.uniform(15.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 90.0), 2),
        "dew_point": round(random.uniform(10.0, 25.0), 2),
        "heat_index": round(random.uniform(0.0, 40.0), 2),
        "location": location,
        "timestamp": time
    }
    return introduce_errors(data)

        
        


def get_next_time():
    global start_time
    start_time += timedelta(seconds=random.randint(30, 60))
    return start_time 

#tao data di chuyen va thong tin cua xe,
def moving_and_device_data( device_id,steps=20):
    global start_record
    #vi du: latitude = (100-80)/10 thi moi lan di chuyen se tang 2 latitude => so step se la so vong lap
    start_record["latitude"] += ((HCM_LONGTI_LATI["latitude"] - HaNoi_LONGTI_LATI["latitude"])/steps)
    start_record["longtitude"] += ((HCM_LONGTI_LATI["longtitude"] - HaNoi_LONGTI_LATI["longtitude"])/steps)
    return {
        "device_id": device_id,
        "timestamp": get_next_time().isoformat(),   
        "location": (start_record["latitude"], start_record["longtitude"]),
        "speed": random.uniform(0, 40),
        "direction": "North-East",
        "make": "OOP",
        "model": "270",
        "year": 2024,
        "fuelType": "Gas",
    }

# ham nay se mo phong quan duong di tu HANOI TOI HCM va sinh ra data cho cac thiet bi IOT, dong thoi push data len kafka topic
def generate_journey(producer,device_id):
    
    #su dung vong lap lien tuc cho toi khi xe den ,  so lan lap se bang steps cua ham moving_and_device_data()
    while True:
        # uu tien goi ham  moving_and_device_data de lay location cho cac IOT phia sau
        device_data = moving_and_device_data(device_id)
        #tat ca location va time se dong bo truc tiep voi xe khi di chuyen
        sensor_data = generate_sensor_data(device_data["location"],device_id,device_data["timestamp"])
        motion_sensor_data = generate_motion_sensor_data(device_data["location"],device_id,device_data["timestamp"])
        air_quality_data = generate_air_quality_data(device_data["location"],device_data["timestamp"],device_id)
        environmental_temperature_data = generate_environmental_temperature_data(device_data["location"],device_data["timestamp"],device_id)
        #nếu đã tới sẽ dừng vòng lặp, vì không thể tới đúng kinh độ và vĩ độ nên chỉ cần kinh độ lớn hơn và vĩ độ nhỏ hơn sẽ tính là tới nơi
        if(device_data["location"][0] <= end_record["latitude"] and device_data["location"][1] >= end_record["longtitude"]):
            print("xe da toi noi")
            break
        Produce_data_to_topic(producer,'topic0',device_data)
        Produce_data_to_topic(producer,"topic1",sensor_data)
        Produce_data_to_topic(producer,"topic2",motion_sensor_data)
        Produce_data_to_topic(producer,"topic3",air_quality_data,)
        Produce_data_to_topic(producer,"topic4",environmental_temperature_data)
        
        time.sleep(5)
        
        
if __name__ == "__main__":
    try:
        generate_journey(producer,"TOYOTA")
    
    except KeyboardInterrupt:
        print("Thoat")
    except Exception as e:
        print(f"Unexpected Error: {e}")