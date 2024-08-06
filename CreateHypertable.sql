CREATE TABLE livedatabase.journey (
    device_id VARCHAR(255),
    timestamp TIMESTAMPTZ,
    location DOUBLE PRECISION[],
    speed FLOAT,
    direction VARCHAR(255),
    make VARCHAR(255),
    model VARCHAR(255),
    year INTEGER,
    fuelType VARCHAR(255)
);
CREATE TABLE livedatabase.sensor (
    device_id VARCHAR(255),
    temperature VARCHAR(255),
    humidity VARCHAR(255),
    pressure VARCHAR(255),
    battery_status VARCHAR(255),
    location DOUBLE PRECISION[],
    timestamp TIMESTAMPTZ
);
CREATE TABLE livedatabase.motion (
    device_id VARCHAR(255),
    motion_detected BOOLEAN,
    temperature VARCHAR(255),
    battery_level FLOAT,
    location DOUBLE PRECISION[],
    device_status VARCHAR(255),
    timestamp TIMESTAMPTZ
);
CREATE TABLE livedatabase.air_quality (
    device_id VARCHAR(255),
    pm2_5 FLOAT,
    pm10 FLOAT,
    co2_level FLOAT,
    temperature VARCHAR(255),
    air_quality_index FLOAT,
    location DOUBLE PRECISION[],
    timestamp TIMESTAMPTZ
);
CREATE TABLE livedatabase.environmental_temperature (
    device_id VARCHAR(255),
    temperature VARCHAR(255),
    humidity VARCHAR(255),
    dew_point FLOAT,
    heat_index FLOAT,
    location DOUBLE PRECISION[],
    timestamp TIMESTAMPTZ
);
SELECT create_hypertable('livedatabase.journey', 'timestamp');
SELECT create_hypertable('livedatabase.sensor', 'timestamp');
SELECT create_hypertable('livedatabase.motion', 'timestamp');
SELECT create_hypertable('livedatabase.air_quality', 'timestamp');
SELECT create_hypertable('livedatabase.environmental_temperature', 'timestamp');

TRUNCATE TABLE livedatabase.motion;
TRUNCATE TABLE livedatabase.journey;
TRUNCATE TABLE livedatabase.sensor;
TRUNCATE TABLE livedatabase.air_quality;
TRUNCATE TABLE livedatabase.environmental_temperature;

