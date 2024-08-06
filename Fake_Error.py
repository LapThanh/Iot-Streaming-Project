import random
def introduce_errors(data):
    # sinh ra gia tri null ti le 10%
    if random.random() < 0.1:  
        # Null values
        data[random.choice(list(data.keys()))] = None
    
    if random.random() < 0.7:  # 10% loi data khong hop le
        if 'temperature' in data:
            data['temperature'] = "invalid_temperature"
        if 'humidity' in data:
            data['humidity'] = "invalid_humidity"
        if 'pressure' in data:
            data['pressure'] = "invalid_pressure"



    if random.random() < 0.1:  # 10% loi out of range
        if 'temperature' in data:
            data['temperature'] = round(random.uniform(-100.0, 100.0), 2)
        if 'humidity' in data:
            data['humidity'] = round(random.uniform(-50.0, 150.0), 2)
        if 'pressure' in data:
            data['pressure'] = round(random.uniform(800.0, 1200.0), 2)

    return data